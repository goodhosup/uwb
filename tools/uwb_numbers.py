"""본문에 들어가는 UWB 수치를 계산·검산하는 단일 출처.

채널 번호 ↔ 주파수, 칩·타임스탬프 시간, 거리 분해능, 링크 버짓,
TWR 클럭 드리프트 오차를 여기서 계산한다. 본문 표와 계산기
(docs/javascripts/calculators.js)는 이 값과 일치해야 한다.

    python tools/uwb_numbers.py              # 주요 표 출력
    python tools/uwb_numbers.py --check      # 본문에 적힌 대표 값 검산 (불일치 시 종료 코드 1)
    python tools/uwb_numbers.py --param-page # docs/reference/parameter-table.md 생성
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

C = 299_792_458.0              # 빛의 속도 [m/s]
F0 = 499.2e6                   # HRP 기본 칩 레이트 [Hz] (IEEE 802.15.4 HRP UWB PHY)
T_CHIP = 1 / F0                # 칩 시간 ≈ 2.003 ns
T_TS = 1 / (128 * F0)          # 타임스탬프 단위(칩의 1/128) ≈ 15.65 ps

# ---------------------------------------------------------------- HRP 채널
# 채널 번호: (중심 주파수 MHz, 대역폭 MHz, 대역)
# 499.2 MHz 폭 채널의 중심 주파수는 499.2 MHz의 정수배다.
CHANNELS = {
    0: (499.2, 499.2, "sub-GHz"),
    1: (3494.4, 499.2, "low"),
    2: (3993.6, 499.2, "low"),
    3: (4492.8, 499.2, "low"),
    4: (3993.6, 1331.2, "low"),
    5: (6489.6, 499.2, "high"),
    6: (6988.8, 499.2, "high"),
    7: (6489.6, 1081.6, "high"),
    8: (7488.0, 499.2, "high"),
    9: (7987.2, 499.2, "high"),
    10: (8486.4, 499.2, "high"),
    11: (7987.2, 1331.2, "high"),
    12: (8985.6, 499.2, "high"),
    13: (9484.8, 499.2, "high"),
    14: (9984.0, 499.2, "high"),
    15: (9484.8, 1354.97, "high"),
}
MANDATORY = {"sub-GHz": 0, "low": 3, "high": 9}   # 대역별 필수 채널
POPULAR = (5, 9)                                   # 스마트폰·FiRa·CCC에서 주로 쓰는 채널

# ---------------------------------------------------------------- 규제 (FCC Part 15 Subpart F, 실내)
PSD_LIMIT_DBM_PER_MHZ = -41.3


def resolution_m(bw_hz: float) -> float:
    """원시 거리 분해능 c / (2B) [m] — 왕복 측거에서 시간 분해능 1/B를 거리로 환산."""
    return C / (2 * bw_hz)


def time_to_m(t_s: float) -> float:
    """편도 전파 시간 → 거리 [m]."""
    return C * t_s


def eirp_dbm(bw_mhz: float, psd: float = PSD_LIMIT_DBM_PER_MHZ) -> float:
    """PSD 제한을 대역 전체에 채웠을 때의 총 EIRP [dBm]."""
    return psd + 10 * math.log10(bw_mhz)


def fspl_db(d_m: float, f_hz: float) -> float:
    """Friis 자유 공간 경로 손실 [dB]."""
    return 20 * math.log10(4 * math.pi * d_m * f_hz / C)


def ss_twr_error_m(t_reply_s: float, ppm_a: float, ppm_b: float) -> float:
    """SS-TWR 클럭 드리프트에 의한 거리 오차 [m].

    ToF_est − ToF ≈ ½ · T_reply · (e_A − e_B),  e = 클럭 주파수 오프셋(ppm).
    """
    return time_to_m(0.5 * t_reply_s * (ppm_a - ppm_b) * 1e-6)


def ds_twr_tof(ra: float, da: float, rb: float, db: float) -> float:
    """비대칭 DS-TWR ToF 추정식: (Ra·Rb − Da·Db) / (Ra + Rb + Da + Db)."""
    return (ra * rb - da * db) / (ra + rb + da + db)


# ---------------------------------------------------------------- 출력
def channel_rows():
    for ch, (fc, bw, band) in CHANNELS.items():
        lo, hi = fc - bw / 2, fc + bw / 2
        yield ch, fc, bw, lo, hi, band


def print_tables() -> None:
    print(f"칩 시간 {T_CHIP * 1e9:.4f} ns (거리 {time_to_m(T_CHIP):.3f} m), "
          f"타임스탬프 단위 {T_TS * 1e12:.2f} ps (거리 {time_to_m(T_TS) * 1e3:.2f} mm)")
    print(f"원시 거리 분해능: 499.2 MHz → {resolution_m(499.2e6):.3f} m, "
          f"1331.2 MHz → {resolution_m(1331.2e6):.3f} m")
    print(f"총 EIRP 상한 (499.2 MHz) {eirp_dbm(499.2):.1f} dBm")
    print()
    print("ch   fc[MHz]   BW[MHz]   범위[MHz]            대역")
    for ch, fc, bw, lo, hi, band in channel_rows():
        print(f"{ch:>2}  {fc:>8.1f}  {bw:>8.2f}   {lo:>8.1f}–{hi:<8.1f}   {band}")
    print()
    print(f"SS-TWR, T_reply 1 ms, 상대 오프셋 20 ppm → 오차 {ss_twr_error_m(1e-3, 20, 0):.2f} m")


# ---------------------------------------------------------------- 검산
# 본문에 적는 대표 값. 본문을 고치면 여기도 같이 고친다.
EXPECTED = [
    ("칩 시간 [ns]", T_CHIP * 1e9, 2.003, 0.001),
    ("타임스탬프 단위 [ps]", T_TS * 1e12, 15.65, 0.01),
    ("타임스탬프 단위 거리 [mm]", time_to_m(T_TS) * 1e3, 4.69, 0.01),
    ("499.2 MHz 원시 분해능 [m]", resolution_m(499.2e6), 0.30, 0.005),
    ("1 ns 편도 거리 [cm]", time_to_m(1e-9) * 100, 30.0, 0.1),
    ("499.2 MHz 총 EIRP [dBm]", eirp_dbm(499.2), -14.3, 0.05),
    ("Ch5 중심 [MHz]", CHANNELS[5][0], 6489.6, 1e-6),
    ("Ch9 중심 [MHz]", CHANNELS[9][0], 7987.2, 1e-6),
    ("SS-TWR 1 ms·20 ppm 오차 [m]", ss_twr_error_m(1e-3, 20, 0), 3.0, 0.01),
]


def check() -> int:
    bad = 0
    for k in (1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 14):  # 499.2 MHz 폭 채널 = 499.2 MHz 정수배
        fc, bw, _ = CHANNELS[k]
        if bw == 499.2 and abs(fc / 499.2 - round(fc / 499.2)) > 1e-9:
            print(f"✗ Ch{k} 중심 주파수가 499.2 MHz 정수배가 아님: {fc}")
            bad += 1
    for name, got, want, tol in EXPECTED:
        ok = abs(got - want) <= tol
        print(f"{'✓' if ok else '✗'} {name}: {got:.4f} (본문 {want})")
        bad += not ok
    return 1 if bad else 0


def param_page() -> None:
    rows = "\n".join(
        f"| {ch} | {fc:.1f} | {bw:.2f} | {lo:.1f} – {hi:.1f} | {band}"
        f"{' · 필수' if MANDATORY.get(band) == ch else ''}{' · 주 사용' if ch in POPULAR else ''} |"
        for ch, fc, bw, lo, hi, band in channel_rows())
    page = f"""# 채널·PHY 파라미터 표

!!! spec "규격 · 개정판"
    IEEE 802.15.4-2020 HRP UWB PHY 채널 할당 · 802.15.4z-2020

!!! basic "이 페이지의 용도"
    본문에서 쓰는 UWB 채널과 기본 시간 단위를 한곳에 모았습니다. 이 페이지는 `tools/uwb_numbers.py --param-page`로 생성하므로 직접 고치지 않습니다.

## HRP 채널 {{ .l2 }}

<figure markdown>
![UWB 채널 맵](../assets/figures/channel_map.svg)
<figcaption>HRP 채널 위치. 파란색 Ch5·Ch9가 스마트폰·디지털 키에서 주로 쓰는 채널이고, 보라색은 넓은 대역 채널입니다.</figcaption>
</figure>

| 채널 | 중심 주파수 (MHz) | 대역폭 (MHz) | 범위 (MHz) | 대역 |
|---|---|---|---|---|
{rows}

## 기본 시간 단위 {{ .l2 }}

| 항목 | 값 | 거리 환산 |
|---|---|---|
| 칩 레이트 | 499.2 MHz | — |
| 칩 시간 | {T_CHIP * 1e9:.3f} ns | {time_to_m(T_CHIP):.3f} m (편도) |
| 타임스탬프 단위 (칩/128) | {T_TS * 1e12:.2f} ps | {time_to_m(T_TS) * 1e3:.2f} mm |
| 원시 거리 분해능 (499.2 MHz) | c / 2B | {resolution_m(499.2e6):.2f} m |
| 총 EIRP 상한 (499.2 MHz, −41.3 dBm/MHz) | {eirp_dbm(499.2):.1f} dBm | — |
"""
    out = ROOT / "docs" / "reference" / "parameter-table.md"
    out.write_text(page, encoding="utf-8")
    print(f"→ {out.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--param-page", action="store_true")
    a = ap.parse_args()
    if a.check:
        return check()
    if a.param_page:
        param_page()
        return 0
    print_tables()
    return 0


if __name__ == "__main__":
    sys.exit(main())
