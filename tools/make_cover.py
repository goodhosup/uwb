"""책 표지(위키독스·전자책용)를 만든다.

한글 글꼴(Noto Sans KR)이 필요해서 그림 파이프라인(build_figures.py)과 분리했다.
결과물은 docs/assets/cover.png (1200×1600, 3:4)와 cover.svg.

    python tools/make_cover.py --font-dir <NotoSansKR-*.otf가 있는 폴더>
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets"

BG_TOP = "#1a1f5c"     # indigo
BG_BOTTOM = "#0b0d26"
AMBER = "#ffc233"      # 사이트 accent(amber)
CYAN = "#5fd4e6"
WHITE = "#ffffff"
SOFT = "#b9bfe8"


def fonts(font_dir: Path) -> dict[str, font_manager.FontProperties]:
    f = {}
    for w in ("Black", "Bold", "Regular"):
        path = font_dir / f"NotoSansKR-{w}.otf"
        font_manager.fontManager.addfont(str(path))
        f[w] = font_manager.FontProperties(fname=str(path))
    return f


def cover(font_dir: Path) -> None:
    f = fonts(font_dir)
    W, H = 12, 16
    fig = plt.figure(figsize=(W, H), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_axis_off()

    # 배경 세로 그라데이션
    grad = np.linspace(0, 1, 256)[:, None]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("bg", [BG_BOTTOM, BG_TOP])
    ax.imshow(grad, extent=(0, W, 0, H), origin="lower", cmap=cmap, aspect="auto", zorder=0)

    # 측거 원: 오른쪽 위 앵커에서 퍼지는 동심원
    cx, cy = 9.6, 12.2
    for i, r in enumerate(np.arange(0.6, 9.5, 0.75)):
        ax.add_patch(Circle((cx, cy), r, fill=False, lw=1.2, ec=CYAN, alpha=max(0.05, 0.42 - i * 0.03), zorder=1))
    ax.add_patch(Circle((cx, cy), 0.16, color=AMBER, zorder=3))

    # CIR: 첫 경로(강조) + 감쇠하는 다중 경로 임펄스
    rng = np.random.default_rng(15)
    base_y, x0 = 5.55, 1.0
    ax.plot([x0, W - 1.0], [base_y, base_y], color=SOFT, lw=1.0, alpha=0.5, zorder=2)
    ax.plot([x0 + 0.55] * 2, [base_y, base_y + 2.3], color=AMBER, lw=5, solid_capstyle="round", zorder=4)
    xs = x0 + 0.95 + np.cumsum(rng.exponential(0.22, 34))
    xs = xs[xs < W - 1.1]
    for x in xs:
        amp = 1.9 * np.exp(-(x - x0 - 0.9) / 2.6) * rng.uniform(0.35, 1.0)
        ax.plot([x, x], [base_y, base_y + amp], color=CYAN, lw=3.4, solid_capstyle="round", alpha=0.85, zorder=3)
    ax.text(x0 + 0.55, base_y - 0.42, "first path", color=AMBER, fontproperties=f["Bold"], fontsize=15, ha="center", va="top")

    # 위쪽 띠
    ax.add_patch(Rectangle((1.0, 14.55), 0.12, 0.62, color=AMBER, zorder=3))
    ax.text(1.32, 14.86, "IEEE 802.15.4z/ab · FiRa · Digital Key", color=SOFT,
            fontproperties=f["Regular"], fontsize=19, va="center")

    # 제목
    ax.text(0.92, 11.0, "UWB", color=WHITE, fontproperties=f["Black"], fontsize=150, va="baseline")
    ax.text(1.0, 9.55, "Handbook", color=WHITE, fontproperties=f["Bold"], fontsize=58, va="baseline")
    ax.text(1.02, 8.55, "초광대역 무선 핸드북", color=AMBER, fontproperties=f["Bold"], fontsize=40, va="baseline")

    # 부제
    ax.text(1.02, 3.6, "임펄스 라디오에서 보안 측거,\n디지털 키와 차세대 802.15.4ab까지",
            color=WHITE, fontproperties=f["Regular"], fontsize=27, va="top", linespacing=1.55)
    ax.text(1.02, 1.72, "기초  →  중급  →  전문가", color=SOFT, fontproperties=f["Regular"], fontsize=20, va="baseline")
    ax.text(W - 1.0, 0.95, "goodhosup.github.io/uwb", color=SOFT, fontproperties=f["Regular"], fontsize=16,
            ha="right", va="baseline", alpha=0.85)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "cover.png", dpi=100)
    plt.rcParams["svg.fonttype"] = "path"
    fig.savefig(OUT / "cover.svg")
    plt.close(fig)
    print(f"→ {(OUT / 'cover.png').relative_to(ROOT)}, cover.svg")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--font-dir", type=Path, required=True)
    cover(ap.parse_args().font_dir)
