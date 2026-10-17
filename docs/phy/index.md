# PHY

이 섹션은 UWB 신호가 공중에서 실제로 어떤 모양인지를 다룹니다. 채널과 대역, 프레임을 이루는 필드, 프리앰블 코드와 변조 방식, 802.15.4z가 추가한 BPRF·HPRF와 STS, 그리고 수신기가 그 신호에서 "첫 경로가 도착한 시각"을 뽑아내는 과정까지 차례로 살펴봅니다. [공통 기초](../basics/index.md)의 펄스·상관·다중 경로 개념을 알고 읽으면 훨씬 수월합니다.

| 페이지 | 핵심 질문 |
|---|---|
| [UWB PHY 개요 (HRP·LRP)](overview.md) | 802.15.4에는 UWB PHY가 왜 두 종류이고, 무엇이 다른가? |
| [채널 번호와 대역](channels.md) | 채널 0–15는 어디에 있고, 왜 Ch5·Ch9가 주로 쓰이나? |
| [HRP 프레임 구조](hrp-frame.md) | 프리앰블·SFD·PHR·페이로드·STS는 각각 무슨 일을 하나? |
| [프리앰블 코드](preamble-codes.md) | 길이 31·127·91 코드는 어떻게 다르고, 왜 "완전한 자기상관"이 중요한가? |
| [변조와 부호화](modulation-coding.md) | BPM-BPSK는 한 심볼에 비트를 어떻게 싣고, 어떤 오류 정정 부호를 쓰나? |
| [BPRF와 HPRF](bprf-hprf.md) | 802.15.4z의 두 모드는 PRF·데이터율·옵션에서 어떻게 갈리나? |
| [STS (Scrambled Timestamp Sequence)](sts.md) | 반복되지 않는 펄스열이 어떻게 측거를 위조로부터 지키나? |
| [LRP PHY](lrp.md) | 저속 펄스 PHY는 HRP와 어떤 철학 차이가 있고 어디에 쓰이나? |
| [수신기 구조와 첫 경로 검출](receiver.md) | 수신기는 CIR에서 첫 경로를 어떻게 찾고 타임스탬프를 찍나? |
| [PHY 파라미터 표](parameters.md) | 모드별 PRF·프리앰블 길이·데이터율·STS 옵션을 한 표로 보면? |

!!! basic "이 섹션을 읽는 순서"
    1. **지도부터** — [개요](overview.md)와 [채널](channels.md)에서 HRP·LRP와 대역의 큰 그림을 잡습니다.
    2. **프레임 해부** — [프레임 구조](hrp-frame.md) → [프리앰블 코드](preamble-codes.md) → [변조와 부호화](modulation-coding.md) 순으로 필드 하나하나를 봅니다.
    3. **802.15.4z의 추가분** — [BPRF와 HPRF](bprf-hprf.md), [STS](sts.md)가 보안 측거의 PHY 기반입니다.
    4. **수신 쪽 관점** — [수신기](receiver.md)에서 이 모든 필드가 타임스탬프 하나로 모이는 과정을 확인하고, [파라미터 표](parameters.md)를 레퍼런스로 씁니다.
