# 802.15.4 개정판 인덱스

!!! spec "규격 · 개정판"
    IEEE Std 802.15.4-2011 / -2015 / -2020 (통합본) · 802.15.4a-2007 · 802.15.4e-2012 · 802.15.4f-2012 · 802.15.4z-2020 · 802.15.4y-2021 · P802.15.4ab (작업 중) · IEEE 802.15.3a (해산)

!!! basic "이 페이지의 용도"
    IEEE 802.15.4에는 Zigbee·Thread·Wi-SUN용 개정판이 훨씬 많습니다. 이 표는 그중 **UWB를 이해하는 데 필요한 것만** 골랐습니다. 통합본과 개정판의 관계는 [표준 문서 읽는 법](../getting-started/reading-standards.md)에 있습니다.

## 통합본 { .l2 }

| 통합본 | UWB 관련 내용 |
|---|---|
| 802.15.4-2006 | UWB 이전. O-QPSK 등 협대역 PHY와 기본 MAC |
| 802.15.4-2011 | **802.15.4a(HRP UWB·CSS)를 통합본에 편입** |
| 802.15.4-2015 | 4e(IE, MAC 개선), 4f 등 편입 |
| 802.15.4-2020 | 당시까지의 개정판 통합. 802.15.4z의 기준 문서 |

## UWB 관련 개정판 { .l2 }

| 개정판 | 이름 (요약) | 내용 | 이 핸드북 |
|---|---|---|---|
| 802.15.3a | 고속 UWB (2006 해산) | MB-OFDM vs DS-UWB 대립으로 표준화 무산 | [UWB의 역사](../getting-started/history.md) |
| **802.15.4a-2007** | Alternate PHYs | **HRP UWB PHY**(펄스, 3진 프리앰블, BPM-BPSK), CSS PHY, 측거 기능 | [UWB PHY 개요](../phy/overview.md) |
| 802.15.4e-2012 | MAC 개선 | **Information Element(IE)** 구조, TSCH 등 MAC 확장 — 4z 측거 IE의 토대 | [MAC 프레임과 IE](../mac/frame-ie.md) |
| 802.15.4f-2012 | Active RFID | RFID용 저 PRF UWB 등 | [LRP PHY](../phy/lrp.md) |
| **802.15.4z-2020** | Enhanced UWB PHYs and Associated Ranging Techniques | **STS**, BPRF·HPRF, LRP 개선, 측거 라운드·측거 IE·SS/DS-TWR·OWR, AoA 보고 | [STS](../phy/sts.md), [측거 라운드 구조](../mac/ranging-rounds.md) |
| 802.15.4y-2021 | 보안 확장 | AES-256 등 MAC 보안 확장 | [보안](../security/index.md) |
| **P802.15.4ab** | 차세대 UWB (작업 중) | 링크 버짓·거리 개선, NBA-MMS, 센싱, 새 데이터 모드 등 — 초안 기준 | [802.15.4ab 개요](../next/4ab-overview.md) |

??? expert "전문가 노트 — 개정판 이름과 진행 상태 읽기"
    IEEE 표준 이름에서 연도가 붙은 것(802.15.4z-2020)은 **승인·발행된 표준**이고, 앞에 P가 붙은 것(P802.15.4ab)은 **프로젝트(작업 중)**입니다. 프로젝트는 PAR(Project Authorization Request)로 범위와 기한이 정해지며, 기한이 연장되기도 합니다. TG4ab는 2025년 문서에서 SA 투표를 2026년 초에 시작해 2026년 12월 RevCom 제출을 목표로 했습니다.

    개정판은 다음 통합본(예: 802.15.4-202x)이 나오면 그 안에 녹아 들어가고, 그때 절 번호가 바뀔 수 있습니다. 실무 문서에서 "802.15.4z 15.x절"처럼 절 번호로 인용할 때는 어느 판 기준인지 함께 적는 습관이 좋습니다.
