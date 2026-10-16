# UWB Handbook — IEEE 802.15.4z/ab · FiRa · Digital Key

임펄스 라디오의 원리부터 IEEE 802.15.4z 보안 측거, FiRa·CCC 생태계, 802.15.4ab 차세대 UWB까지 다루는 한글 UWB 핸드북입니다.
각 페이지는 **기초 → 중급 → 전문가** 순서로 깊어집니다.

- 웹 사이트: https://goodhosup.github.io/uwb/
- 자매 핸드북: [Wi-Fi Handbook](https://goodhosup.github.io/wifi/) (IEEE 802.11) · [Cellular Handbook](https://goodhosup.github.io/cellular/) (LTE · 5G NR · 6G)

## 로컬 실행

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/build_figures.py   # 그림 생성
.venv/bin/mkdocs serve                    # http://127.0.0.1:8000
```

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `mkdocs.yml` | 사이트 설정과 **전체 목차(nav)** — 페이지 추가는 여기서 시작 |
| `docs/` | 본문 마크다운 |
| `docs/assets/figures/` | 스크립트로 생성한 SVG 그림 (직접 수정하지 않음) |
| `diagrams/scripts/` | 그림 생성 스크립트 (matplotlib). 공통 색·스타일은 `style.py` |
| `includes/abbreviations.md` | 사이트 전체 약어 툴팁 (`tools/gen_abbreviations.py`가 약어 사전에서 생성) |
| `tools/uwb_numbers.py` | **수치의 단일 출처** — 채널 주파수, 칩·타임스탬프 시간, 거리 분해능, 링크 버짓, TWR 오차 계산, 본문 검산(`--check`), 파라미터 표 생성(`--param-page`) |
| `tools/scaffold.py` | nav에 있는데 파일이 없는 페이지를 스텁으로 생성 |
| `tools/build_figures.py` | 모든 그림 스크립트 실행 |
| `tools/gen_abbreviations.py` | `docs/reference/glossary.md` 표 → 약어 툴팁 파일 생성 |
| `tools/export_wikidocs.py` | 위키독스 책 형식으로 내보내기 (`--render`로 Mermaid PNG) |
| `tools/publish_wikidocs.py` | 위키독스 API로 업로드 (`WIKIDOCS_TOKEN` 환경 변수) |
| `docs/javascripts/diagrams.mjs` | Mermaid 렌더러 (큰 다이어그램 가독성, 다크 모드, 전체 화면) |
| `docs/javascripts/calculators.js` | 레퍼런스 > 계산기 페이지 스크립트 |

## 페이지 작성 규칙

1. 맨 위에 `!!! spec` 박스로 관련 IEEE 802.15.4 절(Clause)과 개정판(4a·4z·4ab), 해당하면 FiRa·CCC·CSA 규격을 적습니다.
2. 본문은 세 단계로 씁니다.
    - `!!! basic` — 개념과 비유 (수식 없이)
    - 본문 `## 제목 { .l2 }` (헤딩 옆에 중급 배지) — 구조, 파라미터 표, 그림
    - `??? expert` — 접히는 전문가 노트 (표준 수식, 예외 처리, 개정판별 차이)
3. 절차는 Mermaid 시퀀스 다이어그램으로(라벨에 괄호가 있으면 따옴표로 감쌈), 프레임·채널 그림은 `diagrams/scripts/`의 스크립트로 그립니다.
4. 채널 주파수·시간 단위·측거 오차 같은 수치는 `tools/uwb_numbers.py`로 계산해 넣고 `--check`로 검산합니다.
5. 진행 중인 개정판(802.15.4ab 등)은 "논의 중"으로 쓰고 단정하지 않습니다.
6. IEEE 표준이나 FiRa·CCC 문서의 그림·문장을 복사하지 않습니다. 표준은 문서 이름과 절 번호만 인용합니다.

## 배포

`main` 브랜치에 push하면 GitHub Actions(`.github/workflows/deploy.yml`)가 그림을 생성하고 사이트를 빌드해 GitHub Pages에 올립니다.
저장소의 **Settings → Pages → Source**를 `GitHub Actions`로 설정하세요.
