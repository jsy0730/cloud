# 소스

| 폴더 | 내용 |
|---|---|
| `deck/` | 덱 빌드 코드(pptxgenjs). 버전별 스냅샷 + 최신본 완전 세트 `v09_complete` |
| `figures/` | 도면 · 분석 그림 · 이미지 가공 스크립트(Python) |
| `history/` | 덱 수정에 쓴 일회성 패치 스크립트(기록용) |
| `blender/` | Blender 장면 생성 · 렌더 실행 스크립트, 매싱 JSON |

## 덱 빌드 (최신본)

`deck/v09_complete`에서 실행합니다. 빌드는 "측정 → 배치" 두 단계를 반복합니다.

```
# 1) 이미지 폴더 지정: JD_WORK 아래에 img/, img2/, dims.json 이 있어야 함
set JD_WORK=C:\path\to\work
# 2) 빌드 (PowerPoint가 설치된 Windows)
node build.js C:\path\to\out\v09.pptx
```

- `deck.js`: 슬라이드 내용 · 배치, `lay.js`: 격자 · 표 · 패널 · 줄바꿈 보정 라이브러리
- `build.js`: deck.js를 실행해 측정이 필요한 텍스트 블록 목록을 만들고(`mk_measure.js`), PowerPoint로 높이를 재서(`measure2.ps1`) `measure_cache.json`에 저장한 뒤 다시 빌드. 마지막에 `fixlang.py`가 모든 글자에 ko-KR을 지정
- `audit.ps1` + `audit_report.py`: 완성 파일의 텍스트 넘침 · 충돌 감사, `orphans.ps1`: 끝줄에 한두 단어만 남는 문단 탐지, `pdfout.ps1`: PDF · 글꼴 포함본 저장

`v09_complete`는 v9 빌드 당시 파일에서 두 곳만 바꾼 것입니다: `lay.js`의 이미지 폴더를 환경변수 `JD_WORK`로 지정할 수 있게 했고, `build.js`가 `fixlang.py`를 같은 폴더에서 찾게 했습니다.

## 완전한 재빌드에 필요한 이미지

저장소에는 직접 만든 도면 · 렌더만 있습니다. 슬라이드에 들어간 사례 사진 · 도면 가공본(`c_*.jpg`, `d_*.jpg`)과 렌더 크롭(`r_*`, `concept_*` 등)은 Google Drive 정리본의 `03_모델_도면/정동관_도면_모델/work_assets`에 있습니다. 렌더 크롭은 `figures/prep_v6.py`가 `renders/*.png`에서 만듭니다.

## 그림 스크립트 (`figures/`)

- `fig_*.py`, `figs_v2.py`, `figs_v3.py`: 그림자 · 태양 경로 · 소음 · 조망 · 단면 · 층별 용도 · 사례 다이어그램
- `vecexport.py`: matplotlib 축을 편집 가능한 도형 좌표(JSON)로 내보냄
- `make_massing.py`, `mass_profiles.py`: 형태 대안 A~C 매싱 JSON과 프로파일
- `prep_imgs.py`, `prep_v6.py`: 렌더 · 사진을 슬라이드 비율로 가공
- 글꼴 Pretendard(`work_assets/fonts`)를 사용하며 `env_common.py`는 `../geo.py`(저장소 `build/`)에 의존
