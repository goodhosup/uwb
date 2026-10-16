---
hide:
  - navigation
---

# UWB Handbook

**임펄스 라디오의 원리부터 IEEE 802.15.4z 보안 측거, FiRa·CCC 생태계, 802.15.4ab 차세대 UWB까지.**
처음 공부하는 사람은 개념부터, 현업 엔지니어는 표준 디테일까지 한 페이지 안에서 단계적으로 읽을 수 있도록 만든 한글 UWB 핸드북입니다.

Wi-Fi와 셀룰러가 "더 많이, 더 빨리 보내는" 무선이라면, UWB는 **"시간을 정밀하게 재는"** 무선입니다. 이 책도 그 축을 따라 PHY·MAC 다음에 측거와 측위를 독립된 큰 섹션으로 다룹니다.

## 이 핸드북을 읽는 법

모든 페이지는 같은 틀을 따르고, 난이도를 신호 막대 아이콘으로 구분합니다.

| 표시 | 대상 | 내용 |
|---|---|---|
| <span class="lv lv1">기초</span> | 처음 공부하는 사람, 비전공자 | 개념, 비유, "왜 이렇게 만들었나" — 수식 없이 |
| <span class="lv lv2">중급</span> | 전공자, 신입 엔지니어 | 구조, 파라미터 표, 그림, 동작 순서 |
| <span class="lv lv3">전문가</span> | PHY·MAC·펌웨어·측위 엔지니어 | 표준 수식, 예외 처리, 개정판별 변화, 실무 팁 (접힌 상자) |

!!! spec "스펙 박스"
    각 페이지 맨 위의 이 상자에는 관련 IEEE 802.15.4 절(Clause)과 개정판(4a·4z·4ab), 해당하면 FiRa·CCC 규격 이름이 적혀 있습니다.

    본문을 읽다가 원문을 확인하고 싶을 때 바로 찾아갈 수 있습니다.

약어 위에 마우스를 올리면 풀네임이 툴팁으로 나옵니다. 예: HRP, STS, DS-TWR

## 섹션

<div class="grid cards" markdown>

-   :material-flag-checkered: **시작하기**

    ---

    UWB란 무엇인가, 역사, IEEE·FiRa·CCC 표준 지형도, 표준 문서 읽는 법, 학습 로드맵

    [:octicons-arrow-right-24: 시작하기](getting-started/index.md)

-   :material-pulse: **공통 기초**

    ---

    임펄스 라디오, 대역폭과 시간 분해능, 다중 경로, LoS/NLoS, 상관, 링크 버짓, 규제, 안테나 지연

    [:octicons-arrow-right-24: 공통 기초](basics/index.md)

-   :material-waveform: **PHY**

    ---

    HRP·LRP, 채널 0–15, 프레임 구조, 프리앰블 코드, BPRF·HPRF, STS, 첫 경로 검출

    [:octicons-arrow-right-24: PHY](phy/index.md)

-   :material-swap-horizontal: **MAC**

    ---

    802.15.4 MAC, 프레임과 IE, 채널 접근, 측거 블록·라운드·슬롯, 다중 노드 측거, 저전력

    [:octicons-arrow-right-24: MAC](mac/index.md)

-   :material-map-marker-distance: **측거와 측위**

    ---

    ToF, SS-TWR·DS-TWR, UL·DL TDoA, AoA·PDoA, 위치 추정, 오차 보정, 성능 지표

    [:octicons-arrow-right-24: 측거와 측위](ranging/index.md)

-   :material-shield-lock: **보안**

    ---

    릴레이 공격, STS 보안 측거, FiRa 보안 구조, 공개된 공격 연구, 프라이버시

    [:octicons-arrow-right-24: 보안](security/index.md)

-   :material-domain: **생태계**

    ---

    FiRa, UCI, CCC Digital Key 3.0, CSA Aliro, omlox, Android·iOS API, 칩셋

    [:octicons-arrow-right-24: 생태계](ecosystem/index.md)

-   :material-car-key: **응용**

    ---

    디지털 키, 실내 내비게이션, 산업 RTLS, 스마트 태그, UWB 레이더와 센싱

    [:octicons-arrow-right-24: 응용](apps/index.md)

-   :material-telescope: **차세대 UWB**

    ---

    802.15.4ab, NBA-MMS, MMS 측거, 센싱 표준화, 고속·저전력, 공존

    [:octicons-arrow-right-24: 차세대 UWB](next/index.md)

-   :material-book-open-variant: **레퍼런스**

    ---

    UWB vs BLE CS vs Wi-Fi RTT vs 5G 비교, 개정판 인덱스, 파라미터 표, 약어 사전, 계산기

    [:octicons-arrow-right-24: 레퍼런스](reference/index.md)

</div>

## 진행 현황

- [x] 사이트 뼈대, 목차, 그림 파이프라인, 수치 검산 스크립트 (M0)
- [ ] 시작하기 · 공통 기초 (M1)
- [ ] PHY · MAC (M2)
- [ ] 측거와 측위, 계산기 (M3)
- [ ] 보안 · 생태계 · 응용 (M4)
- [ ] 차세대 UWB · 레퍼런스 · 위키독스 내보내기 (M5)

## 자매 핸드북

- [Wi-Fi Handbook](https://goodhosup.github.io/wifi/) — IEEE 802.11 · Wi-Fi 6/7/8
- [Cellular Handbook](https://goodhosup.github.io/cellular/) — LTE · 5G NR · 6G

!!! note "출처와 저작권"
    본문과 그림은 직접 작성했습니다. IEEE 802.15.4 표준과 FiRa·CCC·CSA 규격은 문서 이름과 절 번호만 출처로 인용하며, 원문의 그림이나 표, 문장을 복제하지 않습니다. FiRa·CCC 규격 상세는 회원 전용 문서가 많아 공개 자료 범위에서만 다룹니다.
    절 번호는 판(edition)마다 바뀔 수 있으니 정확한 값은 항상 최신 통합본과 개정판 원문으로 확인하세요.
