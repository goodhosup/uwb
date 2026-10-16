"""공통 기초 그림: 펄스와 스펙트럼, 대역폭과 경로 구분, 다중 경로 CIR."""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from style import DL, INK2, MUTED, RS, SPECIAL, SYNC, UL, save, setup

FC = 6.4896e9   # Ch5 중심
BW = 499.2e6


def pulse(t, bw):
    """가우시안 포락선 펄스 (−10 dB 대역폭 ≈ bw)."""
    sigma = np.sqrt(np.log(10)) / (np.pi * bw)  # 포락선 시간 표준편차
    return np.exp(-t ** 2 / (2 * sigma ** 2))


def pulse_time_freq() -> None:
    t = np.linspace(-4e-9, 4e-9, 4000)
    env = pulse(t, BW)
    rf = env * np.cos(2 * np.pi * FC * t)
    f = np.linspace(4e9, 9e9, 2000)
    sigma = np.sqrt(np.log(10)) / (np.pi * BW)
    spec_db = 10 * np.log10(np.exp(-(2 * np.pi * (f - FC) * sigma) ** 2))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.0))
    a1.plot(t * 1e9, rf, color=DL, lw=0.8)
    a1.plot(t * 1e9, env, color=UL, lw=1.4, ls="--")
    a1.plot(t * 1e9, -env, color=UL, lw=1.4, ls="--")
    a1.set_xlabel("time (ns)")
    a1.set_title("one UWB pulse at Ch5 (~2 ns long)", fontsize=10)
    a1.set_yticks([])
    a2.plot(f / 1e9, spec_db, color=DL, lw=1.6)
    a2.axhline(-10, color=MUTED, lw=0.8, ls=":")
    a2.axvspan((FC - BW / 2) / 1e9, (FC + BW / 2) / 1e9, color=SPECIAL, alpha=0.25, lw=0)
    a2.text(FC / 1e9 + 0.45, -4, "499.2 MHz", ha="left", fontsize=9, color=INK2)
    a2.set_ylim(-40, 2)
    a2.set_xlabel("frequency (GHz)")
    a2.set_ylabel("relative PSD (dB)")
    a2.set_title("its spectrum: short in time = wide in frequency", fontsize=10)
    for a in (a1, a2):
        a.spines[["top", "right"]].set_visible(False)
    save(fig, "pulse_time_freq")


def path_separation() -> None:
    """경로 차 1 m인 두 경로를 20 MHz와 499.2 MHz 펄스로 볼 때."""
    t = np.linspace(-60e-9, 80e-9, 6000)
    d = 1.0 / 3e8  # 1 m 경로 차 ≈ 3.3 ns
    fig, axes = plt.subplots(1, 2, figsize=(10, 2.8), sharey=True)
    for ax, bw, name in ((axes[0], 20e6, "20 MHz (Wi-Fi channel)"), (axes[1], BW, "499.2 MHz (UWB)")):
        p1 = pulse(t, bw)
        p2 = 0.7 * pulse(t - d, bw)
        ax.plot(t * 1e9, p1, color=SYNC, lw=1, ls="--")
        ax.plot(t * 1e9, p2, color=UL, lw=1, ls="--")
        ax.plot(t * 1e9, p1 + p2, color=DL, lw=1.8)
        ax.set_title(f"{name}: two paths 1 m apart", fontsize=10)
        ax.set_xlabel("time (ns)")
        ax.set_xlim(-60, 80) if bw < 1e8 else ax.set_xlim(-6, 10)
        ax.set_yticks([])
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].text(28, 1.2, "merged into one blob", fontsize=9, color=INK2)
    axes[1].text(4.2, 0.85, "two separate peaks", fontsize=9, color=INK2)
    save(fig, "path_separation")


def cir_first_path() -> None:
    """NLoS에 가까운 CIR: 첫 경로가 가장 센 경로가 아니다."""
    rng = np.random.default_rng(7)
    t = np.linspace(0, 120e-9, 6000)
    taps = [(20e-9, 0.35)]  # 첫 경로 (약함)
    taps += [(26e-9, 1.0), (31e-9, 0.6)]
    for _ in range(25):
        tau = 24e-9 + rng.exponential(25e-9)
        taps.append((tau, 0.45 * np.exp(-(tau - 24e-9) / 30e-9) * rng.uniform(0.2, 1)))
    h = sum(a * pulse(t - tau, BW) for tau, a in taps)
    h = h / h.max()
    h += 0.02 * np.abs(rng.standard_normal(t.size))
    fig, ax = plt.subplots(figsize=(10, 3.0))
    ax.plot(t * 1e9, h, color=DL, lw=1.1)
    ax.annotate("first path\n(this sets the distance)", xy=(20, 0.3), xytext=(2, 0.75),
                arrowprops=dict(arrowstyle="->", color=RS), color=RS, fontsize=9)
    ax.annotate("strongest path\n(reflection, arrives later)", xy=(26.3, 1.0), xytext=(42, 1.0),
                arrowprops=dict(arrowstyle="->", color=INK2), color=INK2, fontsize=9)
    ax.set_xlabel("delay (ns)")
    ax.set_ylabel("|CIR|")
    ax.set_yticks([])
    ax.set_ylim(0, 1.3)
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "cir_first_path")


if __name__ == "__main__":
    setup()
    pulse_time_freq()
    path_separation()
    cir_first_path()
