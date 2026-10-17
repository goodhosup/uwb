"""측거와 측위 그림: SS/DS-TWR 타이밍, TDoA 쌍곡선, PDoA 두 안테나 기하."""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from style import CTRL, DL, INK, INK2, MUTED, RS, SPECIAL, SYNC, UL, bare, save, setup


def _msg(ax, x0, y0, x1, y1, color, label):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=12,
                                 color=color, lw=1.6))
    ax.text((x0 + x1) / 2 + 0.12, (y0 + y1) / 2, label, color=color, fontsize=9,
            ha="left", va="center")


def _span(ax, x0, x1, y, label, color, above=True):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (0.13 if above else -0.13), label, color=color, fontsize=9.5,
            ha="center", va="bottom" if above else "top")


def twr_timing() -> None:
    """위: SS-TWR (Tround, Treply). 아래: DS-TWR (Ra, Db, Rb, Da)."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 5.6), gridspec_kw={"height_ratios": [1, 1.1]})
    tof = 0.6
    yA, yB = 1.0, 0.0
    # --- SS-TWR
    ax = a1
    ax.set_title("SS-TWR: one round trip, ToF = (Tround - Treply) / 2", fontsize=10, loc="left")
    t0, trep = 0.5, 3.0
    t1 = t0 + tof
    t2 = t1 + trep
    t3 = t2 + tof
    for y, n in ((yA, "A (initiator)"), (yB, "B (responder)")):
        ax.plot([0, 6.5], [y, y], color=MUTED, lw=1)
        ax.text(-0.1, y, n, ha="right", va="center", fontsize=9.5, color=INK)
    _msg(ax, t0, yA, t1, yB, DL, "Poll")
    _msg(ax, t2, yB, t3, yA, UL, "Response")
    _span(ax, t0, t3, yA + 0.08, "Tround (A clock)", DL)
    _span(ax, t1, t2, yB - 0.08, "Treply (B clock)", UL, above=False)
    # --- DS-TWR
    ax = a2
    ax.set_title("DS-TWR: two round trips, ToF = (Ra*Rb - Da*Db) / (Ra + Rb + Da + Db)",
                 fontsize=10, loc="left")
    db, da = 2.2, 1.6
    p0 = 0.5
    p1 = p0 + tof
    r0 = p1 + db
    r1 = r0 + tof
    f0 = r1 + da
    f1 = f0 + tof
    for y, n in ((yA, "A (initiator)"), (yB, "B (responder)")):
        ax.plot([0, 6.5], [y, y], color=MUTED, lw=1)
        ax.text(-0.1, y, n, ha="right", va="center", fontsize=9.5, color=INK)
    _msg(ax, p0, yA, p1, yB, DL, "Poll")
    _msg(ax, r0, yB, r1, yA, UL, "Response")
    _msg(ax, f0, yA, f1, yB, CTRL, "Final")
    _span(ax, p0, r1, yA + 0.08, "Ra (round A)", DL)
    _span(ax, r1, f0, yA + 0.08, "Da (reply A)", SPECIAL)
    _span(ax, p1, r0, yB - 0.08, "Db (reply B)", SPECIAL, above=False)
    _span(ax, r0, f1, yB - 0.38, "Rb (round B)", UL, above=False)
    for ax in (a1, a2):
        ax.set_xlim(-1.6, 6.7)
        ax.set_ylim(-0.75, 1.45)
        bare(ax)
    fig.text(0.5, 0.01, "ToF exaggerated for clarity; real ToF is ns, replies are hundreds of us to ms",
             ha="center", fontsize=8.5, color=INK2)
    save(fig, "twr_timing")


def tdoa_hyperbola() -> None:
    anchors = np.array([[0, 0], [20, 0], [20, 14], [0, 14]], float)
    tag = np.array([13.0, 5.0])
    x, y = np.meshgrid(np.linspace(-4, 24, 700), np.linspace(-4, 18, 600))
    dist = [np.hypot(x - ax_, y - ay_) for ax_, ay_ in anchors]
    true = [np.hypot(*(tag - a)) for a in anchors]
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    cols = (DL, UL, SYNC)
    for k, c in zip((1, 2, 3), cols):
        dd = true[k] - true[0]
        ax.contour(x, y, dist[k] - dist[0], levels=[dd], colors=[c], linewidths=1.8, linestyles="solid")
        ax.plot([], [], color=c, lw=1.8, label=f"d{k} - d0 = {dd:+.2f} m")
    ax.scatter(anchors[:, 0], anchors[:, 1], marker="s", s=70, color=CTRL, zorder=3)
    for i, (px, py) in enumerate(anchors):
        ax.text(px + (0.6 if px < 10 else -0.6), py + (0.7 if py < 7 else -0.9), f"A{i}",
                ha="left" if px < 10 else "right", fontsize=10, color=CTRL)
    ax.scatter(*tag, marker="o", s=70, color=RS, zorder=4)
    ax.text(tag[0] + 0.5, tag[1] + 0.5, "tag", color=RS, fontsize=10)
    ax.set_aspect("equal")
    ax.set_xlim(-4, 24)
    ax.set_ylim(-4, 18)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.legend(loc="upper left", fontsize=8.5, frameon=False, bbox_to_anchor=(1.01, 1.0),
              title="hyperbola branch\n(reference A0)", title_fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("each range difference = one hyperbola branch; they cross at the tag", fontsize=10)
    save(fig, "tdoa_hyperbola")


def pdoa_geometry() -> None:
    fig, ax = plt.subplots(figsize=(8, 4.6))
    theta = np.radians(35)
    d = 2.0
    a1 = np.array([-d / 2, 0.0])
    a2 = np.array([d / 2, 0.0])
    u = np.array([np.sin(theta), np.cos(theta)])        # 도래 방향(신호원 쪽)
    # 평면파 파면 (u에 수직인 선)
    w = np.array([np.cos(theta), -np.sin(theta)])
    for s in np.arange(0.75, 4.5, 0.75):
        c = a2 + u * s
        p, q = c - 2.2 * w, c + 1.2 * w
        ax.plot([p[0], q[0]], [p[1], q[1]], color=GRIDC, lw=1, ls=":")
    # 입사 광선
    for a in (a1, a2):
        st = a + u * 3.6
        ax.add_patch(FancyArrowPatch(st, a, arrowstyle="-|>", mutation_scale=12, color=DL, lw=1.6))
    # 경로 차: a2 에서 a1을 지나는 파면까지
    foot = a1 + u * np.dot(a2 - a1, u)
    ax.plot([a1[0], foot[0]], [a1[1], foot[1]], color=RS, lw=3, zorder=3)
    ax.text((a1[0] + foot[0]) / 2 - 0.15, (a1[1] + foot[1]) / 2, "extra path\nd sin(theta)",
            color=RS, fontsize=9.5, ha="right", va="center")
    ax.plot([a2[0], foot[0]], [a2[1], foot[1]], color=INK2, lw=1.2, ls="--")
    # 안테나
    for a, n in ((a1, "ant 1"), (a2, "ant 2")):
        ax.plot(*a, marker="^", ms=13, color=CTRL)
        ax.text(a[0], a[1] - 0.35, n, ha="center", va="top", fontsize=9.5, color=CTRL)
    ax.annotate("", xy=(a1[0], -0.85), xytext=(a2[0], -0.85),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.1))
    ax.text(0, -0.95, "d  (<= lambda/2)", ha="center", va="top", fontsize=9.5, color=INK2)
    # 보어사이트와 각도
    ax.plot([0, 0], [0, 3.4], color=MUTED, lw=1, ls="--")
    ax.text(0.05, 3.45, "boresight", fontsize=9, color=MUTED, ha="center", va="bottom")
    arc = np.linspace(0, theta, 40)
    ax.plot(1.6 * np.sin(arc), 1.6 * np.cos(arc), color=SPECIAL, lw=1.6)
    ax.text(1.75 * np.sin(theta / 2), 1.75 * np.cos(theta / 2), "theta", color=INK, fontsize=10)
    ax.text(2.7, 3.3, "plane wave from tag", color=DL, fontsize=9.5)
    ax.text(2.0, -0.9, "delta phi = 2 pi d sin(theta) / lambda", fontsize=10, color=INK)
    ax.set_xlim(-2.6, 5.4)
    ax.set_ylim(-1.5, 4.0)
    ax.set_aspect("equal")
    bare(ax)
    save(fig, "pdoa_geometry")


GRIDC = MUTED

if __name__ == "__main__":
    setup()
    twr_timing()
    tdoa_hyperbola()
    pdoa_geometry()
