"""Week 5: gradient descent and a tiny neural network with NumPy."""

from __future__ import annotations

from pathlib import Path
import json

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)


def save_line_svg(path: Path, xs, ys_list, labels, title, x_label, y_label) -> None:
    width, height = 760, 460
    left, top, chart_w, chart_h = 70, 50, 620, 320
    xs = np.asarray(xs)
    all_y = np.concatenate([np.asarray(y) for y in ys_list])
    min_x, max_x = float(xs.min()), float(xs.max())
    min_y, max_y = float(all_y.min()), float(all_y.max())
    pad = 0.08 * (max_y - min_y + 1e-12)
    min_y, max_y = min_y - pad, max_y + pad

    colors = ["#1f6feb", "#d73a49", "#22863a", "#6f42c1"]
    pieces = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="460" viewBox="0 0 760 460">',
        '<rect width="100%" height="100%" fill="white" />',
        f'<text x="380" y="28" text-anchor="middle" font-size="20" font-family="Arial">{title}</text>',
        f'<rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="none" stroke="#222" />',
    ]
    for idx, y in enumerate(ys_list):
        points = []
        for x_val, y_val in zip(xs, y):
            x = left + (x_val - min_x) / (max_x - min_x) * chart_w
            yy = top + (max_y - y_val) / (max_y - min_y) * chart_h
            points.append(f"{x:.1f},{yy:.1f}")
        pieces.append(
            f'<polyline points="{" ".join(points)}" fill="none" stroke="{colors[idx]}" stroke-width="2" />'
        )
        pieces.append(
            f'<text x="560" y="{80 + 22 * idx}" font-size="13" font-family="Arial" fill="{colors[idx]}">{labels[idx]}</text>'
        )
    pieces.extend(
        [
            f'<text x="380" y="425" text-anchor="middle" font-size="14" font-family="Arial">{x_label}</text>',
            f'<text x="20" y="210" text-anchor="middle" font-size="14" font-family="Arial" transform="rotate(-90 20 210)">{y_label}</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(pieces), encoding="utf-8")


def linear_regression(seed: int = 42) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 10, 240)
    y = 2.5 * x + 1.0 + rng.normal(0, 1.0, size=x.shape)
    idx = rng.permutation(len(x))
    split = int(0.8 * len(x))
    train, val = idx[:split], idx[split:]

    w, b = 0.0, 0.0
    lr = 0.01
    for _ in range(3000):
        pred = w * x[train] + b
        err = pred - y[train]
        w -= lr * 2 * np.mean(err * x[train])
        b -= lr * 2 * np.mean(err)

    train_mse = float(np.mean((w * x[train] + b - y[train]) ** 2))
    val_mse = float(np.mean((w * x[val] + b - y[val]) ** 2))
    fitted = w * x + b
    save_line_svg(
        FIGURES / "linear_regression_fit.svg",
        x,
        [y, fitted],
        ["synthetic data", "fitted line"],
        "Linear Regression by Gradient Descent",
        "x",
        "y",
    )
    return {"w": float(w), "b": float(b), "train_mse": train_mse, "val_mse": val_mse}


def tiny_relu_net(seed: int = 7) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 2 * np.pi, 600).reshape(-1, 1)
    y = np.sin(x) + 0.1 * rng.normal(size=x.shape)
    idx = rng.permutation(len(x))
    split = int(0.8 * len(x))
    train, val = idx[:split], idx[split:]

    hidden = 24
    W1 = rng.normal(0, 0.5, size=(1, hidden))
    b1 = np.zeros((1, hidden))
    W2 = rng.normal(0, 0.2, size=(hidden, 1))
    b2 = np.zeros((1, 1))
    lr = 0.01
    train_losses, val_losses = [], []

    for epoch in range(2500):
        xt, yt = x[train], y[train]
        z1 = xt @ W1 + b1
        h = np.maximum(z1, 0)
        pred = h @ W2 + b2
        err = pred - yt
        grad_pred = 2 * err / len(xt)
        grad_W2 = h.T @ grad_pred
        grad_b2 = np.sum(grad_pred, axis=0, keepdims=True)
        grad_h = grad_pred @ W2.T
        grad_z1 = grad_h * (z1 > 0)
        grad_W1 = xt.T @ grad_z1
        grad_b1 = np.sum(grad_z1, axis=0, keepdims=True)
        W2 -= lr * grad_W2
        b2 -= lr * grad_b2
        W1 -= lr * grad_W1
        b1 -= lr * grad_b1
        if epoch % 25 == 0:
            train_losses.append(float(np.mean(err**2)))
            hv = np.maximum(x[val] @ W1 + b1, 0)
            val_losses.append(float(np.mean((hv @ W2 + b2 - y[val]) ** 2)))

    dense = np.linspace(0, 2 * np.pi, 400).reshape(-1, 1)
    pred_dense = np.maximum(dense @ W1 + b1, 0) @ W2 + b2
    save_line_svg(
        FIGURES / "relu_sine_fit.svg",
        dense.ravel(),
        [np.sin(dense).ravel(), pred_dense.ravel()],
        ["true sin(x)", "ReLU net"],
        "Tiny ReLU Network on sin(x)",
        "x",
        "y",
    )
    epochs = np.arange(len(train_losses)) * 25
    save_line_svg(
        FIGURES / "relu_loss_curve.svg",
        epochs,
        [np.array(train_losses), np.array(val_losses)],
        ["train MSE", "validation MSE"],
        "Training and Validation Loss",
        "epoch",
        "MSE",
    )
    hv = np.maximum(x[val] @ W1 + b1, 0)
    val_pred = hv @ W2 + b2
    return {
        "val_mae": float(np.mean(np.abs(val_pred - y[val]))),
        "max_abs_error": float(np.max(np.abs(val_pred - y[val]))),
        "final_train_mse": train_losses[-1],
        "final_val_mse": val_losses[-1],
    }


def main() -> None:
    results = {
        "linear_regression": linear_regression(),
        "tiny_relu_net": tiny_relu_net(),
        "seed_notes": "Linear seed=42, ReLU seed=7",
    }
    (ROOT / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

