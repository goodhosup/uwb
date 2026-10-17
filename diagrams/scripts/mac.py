"""MAC 그림: 측거 블록·라운드·슬롯 시간 구조, 일대다 DS-TWR 슬롯 배치, 듀티 사이클."""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch, Rectangle

from style import ALT, CTRL, DL, EMPTY, GRID, INK, INK2, MUTED, SPECIAL, UL, bare, save, setup, text_on


def box(ax, x, y, w, h, color, label="", fs=8.5):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="white", lw=1.2))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, color=text_on(color))


def block_round_slot() -> None:
    """블록 → 라운드 → 슬롯의 3단 시간 구조."""
    fig, ax = plt.subplots(figsize=(10, 4.2))
    bare(ax)
    ax.set_xlim(-1.2, 24.5)
    ax.set_ylim(-0.6, 7.2)

    # 1단: 측거 블록 2개
    ax.text(-1.1, 6.35, "blocks", fontsize=9, color=INK2, va="center")
    for b in range(2):
        x0 = 1 + b * 11.5
        box(ax, x0, 6.0, 11, 0.7, EMPTY)
        box(ax, x0, 6.0, 1.1, 0.7, DL, "R0", 8)
        ax.text(x0 + 6, 6.35, f"ranging block {b}  (e.g. 100-200 ms)", ha="center", va="center", fontsize=8.5, color=INK2)
    ax.text(12.9, 5.75, "idle rounds -> radio can sleep", fontsize=8, color=MUTED, ha="center", va="top")

    # 2단: 블록 0을 라운드로 펼침
    ax.text(-1.1, 4.0, "rounds", fontsize=9, color=INK2, va="center")
    n_round = 8
    rw = 22 / n_round
    for r in range(n_round):
        c = DL if r == 0 else EMPTY
        box(ax, 1 + r * rw, 3.65, rw, 0.7, c, f"round {r}" if r < 3 or r == n_round - 1 else "...", 8)
    for xa, xb in ((1, 1), (2.1, 1 + rw)):
        ax.add_artist(ConnectionPatch((xa, 6.0), (xb, 4.35), "data", "data", color=MUTED, lw=0.8, ls=":"))
    ax.text(13, 4.55, "only the round(s) used by this session are active (others: other sessions or sleep)",
            fontsize=8, color=MUTED, ha="center", va="bottom")

    # 3단: 라운드 0을 슬롯으로 펼침 (일대다 DS-TWR 예)
    ax.text(-1.1, 1.5, "slots", fontsize=9, color=INK2, va="center")
    slots = [("RCM", CTRL), ("Poll", DL), ("Resp 1", UL), ("Resp 2", UL), ("Resp 3", UL),
             ("Final", DL), ("Report", ALT), ("free", EMPTY), ("free", EMPTY)]
    sw = 22 / len(slots)
    for i, (lab, c) in enumerate(slots):
        box(ax, 1 + i * sw, 1.15, sw, 0.7, c, lab, 8)
    for xa, xb in ((1, 1), (1 + rw, 23)):
        ax.add_artist(ConnectionPatch((xa, 3.65), (xb, 1.85), "data", "data", color=MUTED, lw=0.8, ls=":"))
    ax.annotate("", xy=(1 + sw, 0.85), xytext=(1, 0.85), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.9))
    ax.text(1 + sw / 2, 0.55, "1 slot (e.g. 2 ms)", fontsize=8, color=INK2, ha="center", va="top")
    ax.text(12, 0.55, "each slot carries at most one frame exchange step", fontsize=8, color=MUTED, ha="left", va="top")
    save(fig, "mac_block_round_slot")


def one_to_many_slots() -> None:
    """일대다 DS-TWR: 장치별 TX/RX 슬롯 배치."""
    slots = ["RCM", "Poll", "Resp 1", "Resp 2", "Resp 3", "Final", "Report"]
    rows = [
        ("controller / initiator", ["T", "T", "R", "R", "R", "T", "T"], DL),
        ("controlee 1 / responder", ["R", "R", "T", "-", "-", "R", "R"], UL),
        ("controlee 2 / responder", ["R", "R", "-", "T", "-", "R", "R"], UL),
        ("controlee 3 / responder", ["R", "R", "-", "-", "T", "R", "R"], UL),
    ]
    fig, ax = plt.subplots(figsize=(10, 3.4))
    bare(ax)
    x0, sw, rh = 3.6, 1.15, 0.62
    ax.set_xlim(0, x0 + sw * len(slots) + 0.2)
    ax.set_ylim(-0.9, len(rows) * 0.8 + 0.8)
    top = len(rows) * 0.8
    for i, s in enumerate(slots):
        ax.text(x0 + i * sw + sw / 2, top + 0.35, s, ha="center", va="center", fontsize=8.5, color=INK)
        ax.text(x0 + i * sw + sw / 2, -0.55, f"slot {i}", ha="center", va="center", fontsize=8, color=MUTED)
    for r, (name, acts, txc) in enumerate(rows):
        y = top - (r + 1) * 0.8
        ax.text(x0 - 0.15, y + rh / 2, name, ha="right", va="center", fontsize=8.5, color=INK2)
        for i, a in enumerate(acts):
            if a == "T":
                c = CTRL if slots[i] == "RCM" else (ALT if slots[i] == "Report" else txc)
                box(ax, x0 + i * sw, y, sw, rh, c, "TX", 8)
            elif a == "R":
                ax.add_patch(Rectangle((x0 + i * sw, y), sw, rh, facecolor="white", edgecolor=GRID, lw=1.0, hatch="///"))
                ax.text(x0 + i * sw + sw / 2, y + rh / 2, "RX", ha="center", va="center", fontsize=8, color=INK2)
            else:
                box(ax, x0 + i * sw, y, sw, rh, SPECIAL, "sleep", 7.5)
    save(fig, "mac_one_to_many_slots")


def duty_cycle() -> None:
    """블록 주기 동안의 무선부 상태(전류)를 개념적으로."""
    fig, ax = plt.subplots(figsize=(10, 2.6))
    levels = {"sleep": 0.05, "wake": 0.35, "rx": 1.0, "tx": 0.75}
    seq = []
    for b in range(3):
        t0 = b * 100
        seq += [(t0, t0 + 3, "wake"), (t0 + 3, t0 + 5, "rx"), (t0 + 5, t0 + 7, "tx"),
                (t0 + 7, t0 + 11, "rx"), (t0 + 11, t0 + 13, "tx"), (t0 + 13, t0 + 100, "sleep")]
    xs, ys = [], []
    for a, b, s in seq:
        xs += [a, b]
        ys += [levels[s], levels[s]]
    ax.plot(xs, ys, color=DL, lw=1.6, drawstyle="default")
    ax.fill_between(xs, ys, color=DL, alpha=0.12, lw=0)
    ax.annotate("active round\n(wake + RX/TX, ~10 ms)", xy=(8, 1.0), xytext=(22, 0.92), fontsize=8.5, color=INK2,
                arrowprops=dict(arrowstyle="->", color=INK2))
    ax.text(55, 0.13, "deep sleep until next block", fontsize=8.5, color=MUTED, ha="center")
    ax.annotate("", xy=(100, -0.12), xytext=(0, -0.12), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.9),
                annotation_clip=False)
    ax.text(50, -0.2, "block interval (e.g. 100 ms)", fontsize=8.5, color=INK2, ha="center", va="top")
    ax.set_ylim(-0.35, 1.2)
    ax.set_xlim(-2, 300)
    ax.set_xlabel("time (ms, illustrative)")
    ax.set_ylabel("radio current (relative)")
    ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "mac_duty_cycle")


if __name__ == "__main__":
    setup()
    block_round_slot()
    one_to_many_slots()
    duty_cycle()
