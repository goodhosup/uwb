"""PHY 그림: HRP 패킷 구성(SP0–SP3), 프레임 타임라인, BPM-BPSK 심볼."""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from style import CTRL, DL, EMPTY, GRID, INK, INK2, MUTED, RS, SPECIAL, SYNC, bare, save, setup, text_on

STS = RS  # STS = 보안 측거 필드 (빨강)


def _box(ax, x, y, w, h, color, label, fs=9):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="white", lw=1.5))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=text_on(color))


def sp_configs() -> None:
    """STS 패킷 구성 SP0–SP3."""
    rows = [
        ("SP0", [("SYNC", 3.0, SYNC), ("SFD", 0.8, SYNC), ("PHR", 0.8, CTRL), ("PHY payload", 3.2, DL)]),
        ("SP1", [("SYNC", 3.0, SYNC), ("SFD", 0.8, SYNC), ("STS", 2.4, STS), ("PHR", 0.8, CTRL), ("PHY payload", 3.2, DL)]),
        ("SP2", [("SYNC", 3.0, SYNC), ("SFD", 0.8, SYNC), ("PHR", 0.8, CTRL), ("PHY payload", 3.2, DL), ("STS", 2.4, STS)]),
        ("SP3", [("SYNC", 3.0, SYNC), ("SFD", 0.8, SYNC), ("STS", 2.4, STS)]),
    ]
    fig, ax = plt.subplots(figsize=(10, 3.2))
    bare(ax)
    h = 0.62
    for i, (name, fields) in enumerate(rows):
        y = (len(rows) - 1 - i) * 0.9
        ax.text(-0.25, y + h / 2, name, ha="right", va="center", fontsize=10, color=INK, fontweight="bold")
        x = 0.0
        for label, w, c in fields:
            _box(ax, x, y, w, h, c, label)
            x += w
        # RMARKER: SFD 끝
        ax.plot([3.8, 3.8], [y - 0.08, y + h + 0.08], color=INK, lw=1.4)
    ax.text(3.8, 3 * 0.9 + h + 0.18, "RMARKER (end of SFD)", ha="center", fontsize=9, color=INK)
    ax.text(1.9, -0.32, "SHR", ha="center", fontsize=9, color=INK2)
    ax.plot([0, 3.8], [-0.14, -0.14], color=INK2, lw=0.8)
    ax.set_xlim(-0.9, 10.6)
    ax.set_ylim(-0.45, 3.6)
    save(fig, "hrp_sp_configs")


def frame_timeline() -> None:
    """BPRF SP1 예: 필드 순서와 대략적 길이 (64 심볼 프리앰블, 8 심볼 SFD, 64×512칩 STS)."""
    chip = 1 / 499.2e6
    sync = 64 * 508 * chip * 1e6      # 길이 127 코드, L=4 → 508칩/심볼
    sfd = 8 * 508 * chip * 1e6
    sts = 64 * 512 * chip * 1e6
    fields = [("SYNC\n64 sym\n~65.1 us", sync, SYNC), ("SFD", sfd, SYNC),
              ("STS\n64 x 512 chips\n~65.6 us", sts, STS),
              ("PHR", 12, CTRL), ("PHY payload\n(length varies)", 40, DL)]
    fig, ax = plt.subplots(figsize=(10, 2.4))
    x = 0.0
    for label, w, c in fields:
        _box(ax, x, 0, w, 1, c, label, fs=8.5)
        x += w
    rm = sync + sfd
    ax.annotate("RMARKER", xy=(rm, 1.0), xytext=(rm, 1.45), ha="center", fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK))
    ax.text(sync + sfd / 2, -0.12, "8 sym\n~8.1 us", ha="center", va="top", fontsize=8, color=INK2)
    ax.text(0, -0.35, "acquisition, AGC, CIR estimate", fontsize=8.5, color=INK2)
    ax.text(sync + sfd + 8, -0.35, "secure CIR (key-dependent)", fontsize=8.5, color=INK2)
    ax.text(sync + sfd + sts + 2, -0.35, "header + data", fontsize=8.5, color=INK2)
    ax.set_xlim(-2, x + 2)
    ax.set_ylim(-0.6, 1.8)
    ax.set_yticks([])
    ax.set_xlabel("time (us, PHR/payload not to scale)")
    ax.spines[["top", "right", "left"]].set_visible(False)
    save(fig, "hrp_frame_timeline")


def bpm_bpsk() -> None:
    """BPM-BPSK 심볼: 두 BPM 구간, 각 구간 앞쪽 절반에 버스트 후보, 뒤쪽은 가드."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 3.6), sharex=True)
    n_half = 8  # 그림용 칸 수 (실제 Nburst와 무관)
    for ax, (title, half, pol) in zip(axes, [("systematic bit 0 -> burst in 1st interval; parity bit sets polarity (+)", 0, 1),
                                             ("systematic bit 1 -> burst in 2nd interval; parity bit sets polarity (-)", 1, -1)]):
        ax.set_xlim(-0.2, 2 * n_half + 0.2)
        ax.set_ylim(-1.3, 1.5)
        bare(ax)
        for h in range(2):
            x0 = h * n_half
            # 후보 버스트 위치(앞쪽 절반)와 가드(뒤쪽 절반)
            ax.add_patch(Rectangle((x0, -1.1), n_half / 2, 2.2, facecolor=EMPTY, edgecolor=GRID))
            ax.add_patch(Rectangle((x0 + n_half / 2, -1.1), n_half / 2, 2.2, facecolor=SPECIAL, alpha=0.25, edgecolor=GRID))
            ax.text(x0 + n_half * 0.75, 1.2, "guard", ha="center", fontsize=8.5, color=INK2)
            ax.text(x0 + n_half * 0.25, 1.2, "possible burst positions", ha="center", fontsize=8.5, color=INK2)
            for k in range(1, 4):
                ax.plot([x0 + k, x0 + k], [-1.1, 1.1], color=GRID, lw=0.6)
        ax.plot([n_half, n_half], [-1.25, 1.45], color=INK, lw=1.2)
        hop = 2  # 확산 수열이 고른 위치 (예)
        bx = half * n_half + hop
        ax.add_patch(Rectangle((bx, 0), 1, 0.9 * pol, facecolor=DL, edgecolor="white"))
        ax.text(bx + 0.5, 0.45 * pol, "+" if pol > 0 else "-", ha="center", va="center", color="white", fontsize=10)
        ax.axhline(0, color=MUTED, lw=0.6)
        ax.set_title(title, fontsize=9.5, loc="left", color=INK)
    axes[1].text(n_half / 2, -1.28, "first BPM interval", ha="center", va="top", fontsize=9, color=INK2)
    axes[1].text(n_half * 1.5, -1.28, "second BPM interval", ha="center", va="top", fontsize=9, color=INK2)
    fig.tight_layout()
    save(fig, "bpm_bpsk_symbol")


if __name__ == "__main__":
    setup()
    sp_configs()
    frame_timeline()
    bpm_bpsk()
