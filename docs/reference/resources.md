# 참고 자료

!!! basic "이 페이지의 용도"
    원문을 확인하거나 더 깊이 공부할 때 찾아갈 곳을 모았습니다. 링크는 공식 사이트 위주이며, 주소가 바뀔 수 있으니 사이트 이름으로 검색해도 됩니다.

## 표준 원문 { .l2 }

| 자료 | 어디서 | 비고 |
|---|---|---|
| IEEE Std 802.15.4-2020 및 개정판 (4z-2020 등) | IEEE GET Program (발행 후 일정 기간 뒤 무료), IEEE Xplore | UWB PHY·MAC의 원문 |
| P802.15.4ab 초안 | IEEE 802.15 회원 영역, IEEE SA | 진행 중 개정판 |
| 802.15 기고문 | IEEE 802.15 Mentor (공개) | TG4z·TG4ab 기술 결정의 배경 |
| TG4z·TG4ab 페이지 | IEEE 802.15 웹사이트 | 일정, 진행 단계, 초안 번호 |
| 802.15.4a 채널 모델 보고서 | IEEE 802.15 Mentor (문서 15-04-0662) | CM1–CM9 채널 모델 |
| ISO/IEC 24730-62 | ISO | 802.15.4 UWB 기반 RTLS 공중 인터페이스 |

## 산업 단체 { .l2 }

| 단체 | 자료 |
|---|---|
| FiRa Consortium | 백서, 공개 규격 개요, 인증 제품 목록 (상세 규격은 회원 전용) |
| Car Connectivity Consortium | Digital Key 개요, 공개 발표 자료 (상세 규격은 회원 전용) |
| Connectivity Standards Alliance | Aliro 개요와 공개 자료 |
| omlox (PI Germany) | 산업용 위치 추적 상호운용 규격 공개 자료 |
| Bluetooth SIG | Core 6.0 Channel Sounding 기술 개요 (비교용) |

## 규제 { .l2 }

| 기관 | 자료 |
|---|---|
| 미국 FCC | 47 CFR Part 15 Subpart F (Ultra-Wideband Operation, 15.501–15.525) |
| 유럽 CEPT·EC | ECC Decision (06)04, EC Decision 2007/131/EC 및 개정 |
| ETSI | EN 302 065-1 (일반), -2 (위치 추적), -3 (차량) |
| 일본 총무성 | UWB 무선 설비 기술기준, ARIB STD-T91 |
| 과학기술정보통신부 · 국립전파연구원 | 신고하지 아니하고 개설할 수 있는 무선국용 무선기기 기술기준 (국내 허용 대역·조건) |
| ITU-R | SM.1755 (UWB 특성), SM.1757 (UWB 영향) |

## 개발 자료 { .l2 }

| 자료 | 내용 |
|---|---|
| Android Developers — UWB 문서 (Jetpack `androidx.core.uwb`) | 측거 세션 API, 지원 기기 조건 |
| AOSP UWB 모듈 소스 | UCI 처리, 세션 관리의 실제 구현 |
| Apple Developer — Nearby Interaction | iOS의 UWB 측거·방향 API, 액세서리 프로토콜 |
| 칩 제조사 사용자 매뉴얼·앱 노트 | 안테나 지연 보정, NLoS 판정, 송신 전력 설정 등 실무 수치 |

## 자매 핸드북 { .l2 }

| 핸드북 | 이 책과 이어지는 부분 |
|---|---|
| [Wi-Fi Handbook](https://goodhosup.github.io/wifi/) | 802.11az 측위, 6 GHz Wi-Fi(Ch5 공존) |
| [Cellular Handbook](https://goodhosup.github.io/cellular/) | NR 포지셔닝, 5G 저대역(UWB 저대역 공존) |

!!! note "인용 원칙"
    이 핸드북은 표준과 산업 규격의 **문서 이름과 절 이름만** 인용하며, 원문의 그림·표·문장을 옮기지 않습니다. 정확한 값은 항상 최신 원문으로 확인하세요.
