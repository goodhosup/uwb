"""책 표지 (위키독스·웹 공용)

위키독스 표지 비율(약 10:13)에 맞춘 1500×1950 px PNG와 JPG를 만든다.
한글 글꼴(나눔스퀘어)이 필요해 CI 그림 빌드(diagrams/scripts/)와 분리해 두었다.

    python diagrams/cover.py            # → docs/assets/cover.png, cover.jpg
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Arc, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "cover.png"
FONT_DIR = Path("/usr/share/fonts/truetype/nanum")

W, H = 100, 130          # 그림 좌표계 (가로 100, 세로 130)
BG_TOP, BG_BOTTOM = "#071a24", "#0d3b4f"
ACCENT = "#5ee0c8"       # 청록 (UWB 펄스)
WARM = "#ffb454"         # 주황 (측거 응답)
PALE = "#bfeee6"


def font(name: str) -> font_manager.FontProperties:
    path = FONT_DIR / name
    font_manager.fontManager.addfont(str(path))
    return font_manager.FontProperties(fname=str(path))


def monocycle(t: np.ndarray, width: float) -> np.ndarray:
    """가우시안 2차 미분(멕시칸 햇) 펄스, 최댓값 1로 정규화"""
    x = t / width
    return (1 - x**2) * np.exp(-x**2 / 2)


def main() -> None:
    bold = font("NanumSquareB.ttf")
    regular = font("NanumSquareR.ttf")

    fig = plt.figure(figsize=(15, 19.5), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_axis_off()

    # 배경 그라데이션
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    top = np.array(matplotlib.colors.to_rgb(BG_TOP))
    bottom = np.array(matplotlib.colors.to_rgb(BG_BOTTOM))
    img = top * (1 - grad[..., None]) + bottom * grad[..., None]
    ax.imshow(img, extent=[0, W, 0, H], aspect="auto", zorder=0)

    # 배경 시간 격자 (칩 간격처럼 촘촘한 세로선)
    for x in np.arange(2, W, 2.5):
        ax.plot([x, x], [8.5, 57], color="#9fe8dc", lw=1.0, alpha=0.06, zorder=1)

    # 두 장치 위치
    a, b, y0 = (16, 37), (84, 37), 37
    # 장치에서 퍼지는 측거 파면 (동심 호)
    for k, rad in enumerate((6, 10, 14, 18)):
        alpha = 0.55 - k * 0.11
        ax.add_patch(Arc(a, 2 * rad, 2 * rad, theta1=-55, theta2=55, color=ACCENT, lw=3,
                         alpha=alpha, zorder=2))
        ax.add_patch(Arc(b, 2 * rad, 2 * rad, theta1=125, theta2=235, color=WARM, lw=3,
                         alpha=alpha, zorder=2))

    # 임펄스 펄스열 (A→B 폴, B→A 응답) — 짧은 펄스 = 넓은 대역
    t = np.linspace(20, 80, 4000)
    poll = sum(monocycle(t - c, 0.55) for c in (27, 35, 43))
    resp = sum(monocycle(t - c, 0.55) for c in (57, 65, 73))
    ax.plot(t, y0 + 4 + poll * 9, color=ACCENT, lw=3.2, zorder=4)
    ax.plot(t, y0 - 4 + resp * 9, color=WARM, lw=3.2, zorder=4)
    ax.plot([20, 80], [y0 + 4, y0 + 4], color=ACCENT, lw=1.2, alpha=0.35, zorder=3)
    ax.plot([20, 80], [y0 - 4, y0 - 4], color=WARM, lw=1.2, alpha=0.35, zorder=3)
    ax.annotate("", xy=(79, y0 + 15), xytext=(21, y0 + 15),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=2.5, mutation_scale=30), zorder=4)
    ax.annotate("", xy=(21, y0 - 15), xytext=(79, y0 - 15),
                arrowprops=dict(arrowstyle="-|>", color=WARM, lw=2.5, mutation_scale=30), zorder=4)
    ax.text(50, y0 + 17.8, "POLL", fontproperties=bold, fontsize=26, color=ACCENT, ha="center",
            va="center", zorder=5)
    ax.text(50, y0 - 17.8, "RESPONSE", fontproperties=bold, fontsize=26, color=WARM, ha="center",
            va="center", zorder=5)

    # 장치 아이콘: 왼쪽 스마트폰, 오른쪽 앵커(차량·도어락)
    ax.add_patch(FancyBboxPatch((a[0] - 3.4, y0 - 6.5), 6.8, 13, boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor=BG_TOP, edgecolor="#ffffff", lw=4, zorder=6))
    ax.plot([a[0] - 1.2, a[0] + 1.2], [y0 + 5, y0 + 5], color="#ffffff", lw=3, zorder=7)
    ax.add_patch(plt.Circle(a, 1.3, color=ACCENT, zorder=7))
    ax.add_patch(FancyBboxPatch((b[0] - 4.2, y0 - 4.2), 8.4, 8.4, boxstyle="round,pad=0,rounding_size=1.6",
                                facecolor=BG_TOP, edgecolor="#ffffff", lw=4, zorder=6))
    ax.add_patch(plt.Circle(b, 1.3, color=WARM, zorder=7))

    # 거리 표시
    ax.annotate("", xy=(b[0], 10.0), xytext=(a[0], 10.0),
                arrowprops=dict(arrowstyle="<|-|>", color="#ffffff", lw=2, mutation_scale=24), zorder=5)
    ax.text(50, 12.6, "d = c · ToF   ( ±10 cm )", fontproperties=bold, fontsize=28, color="#ffffff",
            ha="center", va="center", zorder=5)

    # 상단 라벨
    ax.text(8, 121, "IEEE 802.15.4z / 4ab  ·  FiRa  ·  DIGITAL KEY", fontproperties=bold, fontsize=30,
            color=ACCENT, va="center", zorder=10)
    ax.plot([8, 92], [116.5, 116.5], color=ACCENT, lw=2, alpha=0.6, zorder=10)

    # 제목
    ax.text(6.4, 101.5, "UWB", fontproperties=bold, fontsize=190, color="#ffffff", va="center", zorder=10)
    ax.text(7.0, 81.5, "핸드북", fontproperties=bold, fontsize=150, color="#ffffff", va="center", zorder=10)
    ax.text(8.2, 69.0, "Ultra-Wideband Handbook", fontproperties=bold, fontsize=52, color=PALE,
            va="center", zorder=10)

    # 부제
    ax.text(8.2, 62.5, "임펄스 라디오부터 보안 측거까지, 초광대역을 한 권으로", fontproperties=regular,
            fontsize=34, color="#dff7f2", va="center", zorder=10)

    # 하단 칩
    chips = [("802.15.4z", "#0f8f7c"), ("802.15.4ab", "#2a78d6"), ("FiRa", "#7a5ae0"),
             ("CCC DK", "#d9822b")]
    x = 8
    for label, c in chips:
        width = 4.2 + 1.95 * len(label)
        ax.add_patch(FancyBboxPatch((x, 2.4), width, 4.2, boxstyle="round,pad=0,rounding_size=2.1",
                                    facecolor=c, edgecolor="none", zorder=10))
        ax.text(x + width / 2, 4.5, label, fontproperties=bold, fontsize=28, color="#ffffff",
                ha="center", va="center", zorder=11)
        x += width + 2.0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=100)
    fig.savefig(OUT.with_suffix(".jpg"), dpi=100, pil_kwargs={"quality": 92})
    plt.close(fig)
    print(f"✓ {OUT.relative_to(ROOT)}, {OUT.with_suffix('.jpg').name}")


if __name__ == "__main__":
    main()
