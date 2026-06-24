"""Generate Week 4 tables and dependency-free SVG figures."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.crr import crr_put_price, exercise_boundary


FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)


def convergence_table() -> list[tuple[int, float]]:
    steps_list = [25, 50, 100, 200, 500, 1000]
    return [
        (steps, crr_put_price(100, 100, 1.0, 0.05, 0.25, steps, american=True))
        for steps in steps_list
    ]


def _svg_polyline(points: list[tuple[float, float]], color: str) -> str:
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2" />'


def save_price_surface() -> Path:
    spot_values = np.linspace(60, 140, 41)
    maturity_values = np.linspace(0.05, 2.0, 40)
    prices = np.zeros((len(maturity_values), len(spot_values)))

    for i, maturity in enumerate(maturity_values):
        for j, spot in enumerate(spot_values):
            prices[i, j] = crr_put_price(
                spot, 100, maturity, 0.05, 0.25, 300, american=True
            )

    left, top, chart_w, chart_h = 80, 70, 760, 420
    min_price, max_price = float(prices.min()), float(prices.max())
    cell_w = chart_w / len(spot_values)
    cell_h = chart_h / len(maturity_values)
    rects: list[str] = []
    for i in range(len(maturity_values)):
        for j in range(len(spot_values)):
            normalized = (prices[i, j] - min_price) / (max_price - min_price)
            r = int(35 + 190 * normalized)
            g = int(70 + 110 * (1 - abs(normalized - 0.55)))
            b = int(145 - 110 * normalized)
            x = left + j * cell_w
            y = top + (len(maturity_values) - 1 - i) * cell_h
            rects.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_w + 0.2:.1f}" '
                f'height="{cell_h + 0.2:.1f}" fill="rgb({r},{g},{b})" />'
            )

    path = FIGURES / "week4_price_surface.svg"
    path.write_text(
        "\n".join(
            [
                '<svg xmlns="http://www.w3.org/2000/svg" width="920" height="580" viewBox="0 0 920 580">',
                '<rect width="100%" height="100%" fill="white" />',
                '<text x="460" y="34" text-anchor="middle" font-size="22" font-family="Arial">CRR American Put Price Surface</text>',
                *rects,
                f'<rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="none" stroke="#222" />',
                '<text x="460" y="540" text-anchor="middle" font-size="16" font-family="Arial">Spot price S0: 60 to 140</text>',
                '<text x="22" y="280" text-anchor="middle" font-size="16" font-family="Arial" transform="rotate(-90 22 280)">Time to maturity T: 0.05 to 2.0 years</text>',
                f'<text x="840" y="84" font-size="13" font-family="Arial">High price {max_price:.2f}</text>',
                f'<text x="840" y="490" font-size="13" font-family="Arial">Low price {min_price:.2f}</text>',
                "</svg>",
            ]
        ),
        encoding="utf-8",
    )
    return path


def save_exercise_boundary() -> tuple[Path, list[tuple[float, float]]]:
    _, boundary = exercise_boundary(100, 100, 1.0, 0.05, 0.25, 500)
    times = [point[0] for point in boundary]
    stocks = [point[1] for point in boundary]

    left, top, chart_w, chart_h = 85, 60, 650, 360
    min_t, max_t = min(times), max(times)
    min_s, max_s = min(stocks), max(stocks)
    points = [
        (
            left + (t - min_t) / (max_t - min_t) * chart_w,
            top + (max_s - s) / (max_s - min_s) * chart_h,
        )
        for t, s in boundary
    ]

    grid = []
    for k in range(6):
        x = left + k * chart_w / 5
        y = top + k * chart_h / 5
        grid.append(
            f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + chart_h}" stroke="#ddd" />'
        )
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + chart_w}" y2="{y:.1f}" stroke="#ddd" />'
        )

    path = FIGURES / "week4_exercise_boundary.svg"
    path.write_text(
        "\n".join(
            [
                '<svg xmlns="http://www.w3.org/2000/svg" width="820" height="520" viewBox="0 0 820 520">',
                '<rect width="100%" height="100%" fill="white" />',
                '<text x="410" y="32" text-anchor="middle" font-size="22" font-family="Arial">American Put Early-Exercise Boundary</text>',
                *grid,
                f'<line x1="{left}" y1="{top + chart_h}" x2="{left + chart_w}" y2="{top + chart_h}" stroke="#222" />',
                f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#222" />',
                _svg_polyline(points, "#1f6feb"),
                '<text x="410" y="478" text-anchor="middle" font-size="15" font-family="Arial">Time t</text>',
                '<text x="22" y="250" text-anchor="middle" font-size="15" font-family="Arial" transform="rotate(-90 22 250)">Highest exercise stock price</text>',
                f'<text x="92" y="445" font-size="13" font-family="Arial">t={min_t:.2f}</text>',
                f'<text x="690" y="445" font-size="13" font-family="Arial">t={max_t:.2f}</text>',
                f'<text x="32" y="68" font-size="13" font-family="Arial">S={max_s:.2f}</text>',
                f'<text x="32" y="420" font-size="13" font-family="Arial">S={min_s:.2f}</text>',
                "</svg>",
            ]
        ),
        encoding="utf-8",
    )
    return path, boundary


def main() -> None:
    euro = crr_put_price(100, 100, 1.0, 0.05, 0.25, 500, american=False)
    amer = crr_put_price(100, 100, 1.0, 0.05, 0.25, 500, american=True)
    print(f"European put: {euro:.6f}")
    print(f"American put: {amer:.6f}")
    print(f"Early-exercise premium: {amer - euro:.6f}")
    print("Convergence:")
    for steps, price in convergence_table():
        print(f"{steps:4d}: {price:.6f}")
    surface = save_price_surface()
    boundary_path, boundary = save_exercise_boundary()
    print(f"Saved {surface}")
    print(f"Saved {boundary_path}")
    print("Boundary sample:")
    for t, s in boundary[:10]:
        print(f"{t:.3f}, {s:.6f}")


if __name__ == "__main__":
    main()
