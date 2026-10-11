#!/usr/bin/env python3
"""Gemini API CLI (표준 라이브러리만 사용).

API 키는 환경의 네트워크 시크릿이 프록시에서 x-goog-api-key 헤더로 주입한다.
로컬에서 실행할 때는 GEMINI_API_KEY 환경변수를 쓴다.

사용 예:
  python3 scripts/gemini.py text "질문"
  python3 scripts/gemini.py text "이 도면 설명해줘" -f plan.png -f spec.pdf
  python3 scripts/gemini.py text "최신 건축법 개정 내용" --search
  python3 scripts/gemini.py image "콘크리트 주택 외관 렌더" -o out/render.png
  python3 scripts/gemini.py image "배경을 저녁으로 바꿔줘" -f photo.jpg -o out/evening.png
  python3 scripts/gemini.py tts "발표 원고 내용" -o out/speech.wav
  python3 scripts/gemini.py models
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import wave
from pathlib import Path

BASE = "https://generativelanguage.googleapis.com/v1beta"

# 앞에서부터 시도하고, 과부하(429/500/503)나 404면 다음 모델로 넘어간다.
MODELS = {
    "text": ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash"],
    "pro": ["gemini-3.1-pro-preview", "gemini-pro-latest", "gemini-3.8-flash"],
    "lite": ["gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-3.8-flash"],
    "image": ["gemini-3-pro-image", "gemini-3.1-flash-image", "gemini-nano-banana-2.1"],
    "tts": ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview"],
}

RETRYABLE = {429, 500, 503}
INLINE_LIMIT = 20 * 1024 * 1024


def _request(method, url, body=None, headers=None, timeout=300):
    headers = dict(headers or {})
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        headers["x-goog-api-key"] = key
    data = None
    if body is not None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, dict(resp.headers), resp.read()


def _upload(path: Path, mime: str) -> dict:
    """20MB 넘는 파일은 Files API로 올리고 file_data 파트를 돌려준다."""
    size = path.stat().st_size
    _, headers, _ = _request(
        "POST",
        "https://generativelanguage.googleapis.com/upload/v1beta/files",
        body={"file": {"display_name": path.name}},
        headers={
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(size),
            "X-Goog-Upload-Header-Content-Type": mime,
        },
    )
    upload_url = {k.lower(): v for k, v in headers.items()}["x-goog-upload-url"]
    _, _, raw = _request(
        "POST",
        upload_url,
        body=path.read_bytes(),
        headers={
            "Content-Length": str(size),
            "X-Goog-Upload-Offset": "0",
            "X-Goog-Upload-Command": "upload, finalize",
        },
        timeout=900,
    )
    info = json.loads(raw)["file"]
    # 영상 등은 처리(PROCESSING)가 끝나야 쓸 수 있다.
    while info.get("state") == "PROCESSING":
        time.sleep(3)
        _, _, raw = _request("GET", f"{BASE}/{info['name']}")
        info = json.loads(raw)
    if info.get("state") == "FAILED":
        sys.exit(f"파일 처리 실패: {path}")
    return {"file_data": {"mime_type": mime, "file_uri": info["uri"]}}


def _file_part(p: str) -> dict:
    path = Path(p)
    if not path.is_file():
        sys.exit(f"파일 없음: {p}")
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    if path.stat().st_size > INLINE_LIMIT:
        return _upload(path, mime)
    return {"inline_data": {"mime_type": mime, "data": base64.b64encode(path.read_bytes()).decode()}}


def generate(models, body):
    """모델 후보를 차례로 시도하며 generateContent를 호출한다."""
    last = None
    for model in models:
        for attempt in range(3):
            try:
                _, _, raw = _request("POST", f"{BASE}/models/{model}:generateContent", body)
                print(f"[gemini] model={model}", file=sys.stderr)
                return json.loads(raw)
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")
                last = f"{model}: HTTP {e.code} {detail[:300]}"
                if e.code == 429 and "free_tier" in detail:
                    # 무료 등급 한도 초과(또는 한도 0)는 재시도해도 소용없다.
                    last = f"{model}: 무료 등급 할당량 초과 (이미지·검색 등은 무료 한도가 0일 수 있음, 결제 등록 필요)"
                    break
                if e.code in RETRYABLE and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                if e.code in RETRYABLE or e.code == 404:
                    break  # 다음 모델
                sys.exit(last)
    sys.exit(f"모든 모델 실패. 마지막 오류: {last}")


def _parts(resp):
    cands = resp.get("candidates") or []
    if not cands:
        sys.exit("응답에 결과가 없음: " + json.dumps(resp.get("promptFeedback", resp), ensure_ascii=False)[:500])
    return cands[0].get("content", {}).get("parts", [])


def _build_body(prompt, files, system=None):
    parts = [_file_part(f) for f in files or []]
    parts.append({"text": prompt})
    body = {"contents": [{"role": "user", "parts": parts}]}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    return body


def _read_prompt(prompt):
    if prompt == "-":
        return sys.stdin.read()
    return prompt


def cmd_text(a):
    body = _build_body(_read_prompt(a.prompt), a.file, a.system)
    if a.search:
        body["tools"] = [{"google_search": {}}]
    if a.json:
        body["generationConfig"] = {"responseMimeType": "application/json"}
    models = [a.model] if a.model else MODELS[a.tier]
    resp = generate(models, body)
    text = "".join(p.get("text", "") for p in _parts(resp) if not p.get("thought"))
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(text, encoding="utf-8")
        print(f"저장: {a.output}")
    else:
        print(text)
    if a.search:
        meta = (resp["candidates"][0].get("groundingMetadata") or {}).get("groundingChunks") or []
        for c in meta:
            web = c.get("web") or {}
            if web:
                print(f"- 출처: {web.get('title')} {web.get('uri')}")


def cmd_image(a):
    body = _build_body(_read_prompt(a.prompt), a.file)
    body["generationConfig"] = {"responseModalities": ["TEXT", "IMAGE"]}
    if a.aspect:
        body["generationConfig"]["imageConfig"] = {"aspectRatio": a.aspect}
    models = [a.model] if a.model else MODELS["image"]
    resp = generate(models, body)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in _parts(resp):
        inline = p.get("inlineData") or p.get("inline_data")
        if inline and not p.get("thought"):
            target = out if n == 0 else out.with_name(f"{out.stem}_{n}{out.suffix}")
            target.write_bytes(base64.b64decode(inline["data"]))
            print(f"저장: {target}")
            n += 1
        elif p.get("text") and not p.get("thought"):
            print(p["text"])
    if n == 0:
        sys.exit("이미지가 생성되지 않았습니다.")


def cmd_tts(a):
    body = _build_body(_read_prompt(a.prompt), None)
    body["generationConfig"] = {
        "responseModalities": ["AUDIO"],
        "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": a.voice}}},
    }
    models = [a.model] if a.model else MODELS["tts"]
    resp = generate(models, body)
    inline = next((p.get("inlineData") for p in _parts(resp) if p.get("inlineData")), None)
    if not inline:
        sys.exit("오디오가 생성되지 않았습니다.")
    pcm = base64.b64decode(inline["data"])
    rate = 24000
    for token in inline.get("mimeType", "").split(";"):
        if token.strip().startswith("rate="):
            rate = int(token.split("=")[1])
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)
    print(f"저장: {out} ({len(pcm) / (rate * 2):.1f}초)")


def cmd_models(a):
    _, _, raw = _request("GET", f"{BASE}/models?pageSize=200")
    for m in json.loads(raw).get("models", []):
        methods = ",".join(m.get("supportedGenerationMethods", []))
        print(f"{m['name'].removeprefix('models/'):45} {methods}")


def main():
    ap = argparse.ArgumentParser(description="Gemini API CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("text", help="텍스트 생성 / 파일(이미지·PDF·오디오·영상) 분석")
    t.add_argument("prompt", help="프롬프트 ('-'면 stdin)")
    t.add_argument("-f", "--file", action="append", help="첨부 파일 (여러 번 가능)")
    t.add_argument("--tier", choices=["text", "pro", "lite"], default="text")
    t.add_argument("-m", "--model")
    t.add_argument("-s", "--system", help="시스템 지시문")
    t.add_argument("--search", action="store_true", help="구글 검색 그라운딩")
    t.add_argument("--json", action="store_true", help="JSON으로 응답")
    t.add_argument("-o", "--output")
    t.set_defaults(func=cmd_text)

    i = sub.add_parser("image", help="이미지 생성/편집")
    i.add_argument("prompt")
    i.add_argument("-f", "--file", action="append", help="편집할/참고할 이미지")
    i.add_argument("-o", "--output", required=True)
    i.add_argument("--aspect", help="예: 16:9, 1:1, 4:3")
    i.add_argument("-m", "--model")
    i.set_defaults(func=cmd_image)

    s = sub.add_parser("tts", help="음성 합성 (WAV)")
    s.add_argument("prompt")
    s.add_argument("-o", "--output", required=True)
    s.add_argument("--voice", default="Kore")
    s.add_argument("-m", "--model")
    s.set_defaults(func=cmd_tts)

    m = sub.add_parser("models", help="사용 가능한 모델 목록")
    m.set_defaults(func=cmd_models)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
