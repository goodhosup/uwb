# 레퍼런스

본문을 읽다가 빠르게 찾아볼 표와 도구를 모았습니다.

| 페이지 | 내용 |
|---|---|
| [UWB vs BLE CS vs Wi-Fi RTT vs 5G](positioning-comparison.md) | 정밀 측거·측위 기술 비교 — 정확도, 전력, 보안, 생태계 |
| [802.15.4 개정판 인덱스](amendment-index.md) | UWB와 관련된 802.15.4 통합본·개정판 목록과 이 핸드북 위치 |
| [채널·PHY 파라미터 표](parameter-table.md) | HRP 채널 주파수, 칩·타임스탬프 단위 (스크립트로 생성) |
| [약어 사전](glossary.md) | 사이트 전체 약어 툴팁의 원본 |
| [계산기](calculators.md) | 거리 분해능, TWR 클럭 드리프트 오차, 링크 버짓과 도달 거리, 채널 ↔ 주파수 |
| [참고 자료](resources.md) | 표준 원문, 산업 단체, 규제, 개발 자료 |

!!! tip "수치 검산"
    이 핸드북의 채널 주파수·시간 단위·측거 오차·링크 버짓 값은 `tools/uwb_numbers.py`가 계산한 값입니다. `python tools/uwb_numbers.py --check`를 실행하면 본문에 쓰인 대표 값들을 다시 검산합니다.
