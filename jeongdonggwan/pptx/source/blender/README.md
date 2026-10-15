# Blender 장면 스크립트

- 환경: Blender 5.2.2(Windows), Cycles(GPU HIP 또는 CPU), Poly Haven 자산(`dl_ph.py`로 내려받음)
- 입력: 저장소 `build/render/design.json`, `context.json`, `views4.json`(환경변수 `JD_ROOT`), `fillers.json`, `rooms.json`(`JD_FILL`)
- 주요 환경변수: `JD_ROOT`, `JD_PH`(Poly Haven 폴더), `JD_FILL`, `JD_VIEWS`, `JD_VARIANT`(외피 변형), `JD_MASSING`(형태 대안 매싱 JSON), `JD_NOPEOPLE`, `JD_EXPO`, `JD_DUSK`, `JD_NIGHT`

| 파일 | 설명 |
|---|---|
| `build_scene.py` | 첫 세대(v02): 목재 슬랫을 투명 마스크로 표현한 장면 |
| `build_scene2.py` | 매싱 · 사례 변형(`JD_MASSING`, `JD_VARIANT`) 지원 |
| `build_scene3.py` | 실제 기울어진 슬랫 · 슬랫 뒤 주차 데크 · 상세 계단 · 아스팔트 · 인도 · 가로수 |
| `build_scene4.py` | scene3 + 사례 변형 · 매싱(최종 외피 · 형태 대안 렌더) |
| `render_steps2.py` | 볼륨 도출 축측 렌더(Cycles + Freestyle) |
| `run_*.sh` | 렌더 실행 스크립트(`run_v3.sh <view> <name> <samples> <res>` 등) |
| `massing_A/B/C.json` | 형태 대안 매싱 |
| `tools/` | 점검 · 시험용 보조 스크립트 |
