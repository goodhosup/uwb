"""UWB 채널 맵: HRP 채널 0–15의 위치와 폭, FCC 실내 마스크의 −41.3 dBm/MHz 구간."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from style import CTRL, DL, GRID, INK2, MUTED, SPECIAL, SYNC, bare, save, setup, text_on

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from uwb_numbers import CHANNELS, POPULAR  # noqa: E402


def channel_map() -> None:
    fig, ax = plt.subplots(figsize=(10, 3.2))
    bare(ax)
    # FCC 실내 UWB 허용 대역 3.1–10.6 GHz
    ax.add_patch(mpatches.Rectangle((3100, -0.6), 7500, 0.35, color=SPECIAL, alpha=0.35, lw=0))
    ax.text(6850, -0.43, "FCC indoor mask −41.3 dBm/MHz (3.1–10.6 GHz)", ha="center", va="center", fontsize=9, color=INK2)
    narrow = {k: v for k, v in CHANNELS.items() if v[1] == 499.2 and k != 0}
    wide = {k: v for k, v in CHANNELS.items() if v[1] != 499.2}
    for k, (fc, bw, _) in narrow.items():
        color = DL if k in POPULAR else SYNC
        ax.add_patch(mpatches.Rectangle((fc - bw / 2 + 8, 0), bw - 16, 0.8, color=color, lw=0))
        ax.text(fc, 0.4, f"Ch{k}", ha="center", va="center", fontsize=9, color=text_on(color))
    for row, (k, (fc, bw, _)) in enumerate(sorted(wide.items())):
        y = 1.0 + (row % 2) * 0.55
        ax.add_patch(mpatches.Rectangle((fc - bw / 2 + 8, y), bw - 16, 0.45, color=CTRL, lw=0, alpha=0.85))
        ax.text(fc, y + 0.225, f"Ch{k} ({bw:.0f} MHz)", ha="center", va="center", fontsize=8, color=text_on(CTRL))
    for ghz in range(3, 11):
        ax.plot([ghz * 1000] * 2, [-0.7, -0.62], color=GRID, lw=1)
        ax.text(ghz * 1000, -0.82, f"{ghz} GHz", ha="center", va="top", fontsize=8, color=MUTED)
    ax.set_xlim(2600, 10800)
    ax.set_ylim(-1.0, 2.2)
    save(fig, "channel_map")


if __name__ == "__main__":
    setup()
    channel_map()
