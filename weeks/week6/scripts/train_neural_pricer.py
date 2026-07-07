"""Week 6: NumPy MLP pricer trained on CRR binomial labels."""

from __future__ import annotations

from pathlib import Path
import csv
import json
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WEEK4 = REPO / "weeks" / "week4"
sys.path.insert(0, str(WEEK4))

from src.crr import crr_put_price


DATA = ROOT / "data"
FIGURES = ROOT / "figures"
DATA.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


def save_scatter_svg(path: Path, x, y, title: str, x_label: str, y_label: str) -> None:
    width, height = 720, 520
    left, top, chart_w, chart_h = 70, 55, 560, 360
    x, y = np.asarray(x), np.asarray(y)
    lo, hi = float(min(x.min(), y.min())), float(max(x.max(), y.max()))
    pieces = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="520" viewBox="0 0 720 520">',
        '<rect width="100%" height="100%" fill="white" />',
        f'<text x="360" y="30" text-anchor="middle" font-size="20" font-family="Arial">{title}</text>',
        f'<rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="none" stroke="#222" />',
    ]
    for xi, yi in zip(x[:: max(1, len(x)//1000)], y[:: max(1, len(y)//1000)]):
        sx = left + (xi - lo) / (hi - lo) * chart_w
        sy = top + (hi - yi) / (hi - lo) * chart_h
        pieces.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2" fill="#1f6feb" opacity="0.45" />')
    pieces.append(f'<line x1="{left}" y1="{top+chart_h}" x2="{left+chart_w}" y2="{top}" stroke="#d73a49" stroke-width="2" />')
    pieces.extend([
        f'<text x="360" y="470" text-anchor="middle" font-size="14" font-family="Arial">{x_label}</text>',
        f'<text x="20" y="240" text-anchor="middle" font-size="14" font-family="Arial" transform="rotate(-90 20 240)">{y_label}</text>',
        "</svg>",
    ])
    path.write_text("\n".join(pieces), encoding="utf-8")


def save_line_svg(path: Path, xs, ys_list, labels, title, x_label, y_label) -> None:
    width, height = 760, 460
    left, top, chart_w, chart_h = 70, 50, 620, 320
    xs = np.asarray(xs)
    all_y = np.concatenate([np.asarray(y) for y in ys_list])
    min_x, max_x = float(xs.min()), float(xs.max())
    min_y, max_y = float(all_y.min()), float(all_y.max())
    colors = ["#1f6feb", "#d73a49", "#22863a"]
    pieces = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="460" viewBox="0 0 760 460">',
        '<rect width="100%" height="100%" fill="white" />',
        f'<text x="380" y="28" text-anchor="middle" font-size="20" font-family="Arial">{title}</text>',
        f'<rect x="{left}" y="{top}" width="{chart_w}" height="{chart_h}" fill="none" stroke="#222" />',
    ]
    for idx, y in enumerate(ys_list):
        pts = []
        for xv, yv in zip(xs, y):
            px = left + (xv - min_x) / (max_x - min_x) * chart_w
            py = top + (max_y - yv) / (max_y - min_y + 1e-12) * chart_h
            pts.append(f"{px:.1f},{py:.1f}")
        pieces.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colors[idx]}" stroke-width="2" />')
        pieces.append(f'<text x="560" y="{80 + 22*idx}" font-size="13" font-family="Arial" fill="{colors[idx]}">{labels[idx]}</text>')
    pieces.extend([
        f'<text x="380" y="425" text-anchor="middle" font-size="14" font-family="Arial">{x_label}</text>',
        f'<text x="20" y="210" text-anchor="middle" font-size="14" font-family="Arial" transform="rotate(-90 20 210)">{y_label}</text>',
        "</svg>",
    ])
    path.write_text("\n".join(pieces), encoding="utf-8")


def generate_dataset(n: int = 10_000, steps: int = 100, seed: int = 11) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X = np.column_stack(
        [
            rng.uniform(60, 140, n),
            rng.uniform(80, 120, n),
            rng.uniform(0.05, 2.0, n),
            rng.uniform(0.00, 0.10, n),
            rng.uniform(0.10, 0.50, n),
        ]
    )
    y = np.array([crr_put_price(*row, steps=steps, american=True) for row in X])
    with (DATA / "synthetic_contracts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["S0", "K", "T", "r", "sigma", "american_put_price"])
        writer.writerows(np.column_stack([X, y]))
    return X, y.reshape(-1, 1)


def relu(z): return np.maximum(z, 0)


def train_mlp(X: np.ndarray, y: np.ndarray, seed: int = 17) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    n_train, n_val = int(0.8 * len(X)), int(0.1 * len(X))
    train, val, test = idx[:n_train], idx[n_train:n_train+n_val], idx[n_train+n_val:]
    mean, std = X[train].mean(axis=0), X[train].std(axis=0)
    Xs = (X - mean) / std
    scale_y = y[train].std()
    mean_y = y[train].mean()
    ys = (y - mean_y) / scale_y

    dims = [5, 48, 32, 1]
    W = [rng.normal(0, np.sqrt(2/dims[i]), size=(dims[i], dims[i+1])) for i in range(len(dims)-1)]
    b = [np.zeros((1, dims[i+1])) for i in range(len(dims)-1)]
    lr = 0.006
    losses_train, losses_val = [], []

    for epoch in range(850):
        xb, yb = Xs[train], ys[train]
        z1 = xb @ W[0] + b[0]; a1 = relu(z1)
        z2 = a1 @ W[1] + b[1]; a2 = relu(z2)
        pred = a2 @ W[2] + b[2]
        grad = 2 * (pred - yb) / len(xb)
        gW2 = a2.T @ grad; gb2 = grad.sum(axis=0, keepdims=True)
        ga2 = grad @ W[2].T; gz2 = ga2 * (z2 > 0)
        gW1 = a1.T @ gz2; gb1 = gz2.sum(axis=0, keepdims=True)
        ga1 = gz2 @ W[1].T; gz1 = ga1 * (z1 > 0)
        gW0 = xb.T @ gz1; gb0 = gz1.sum(axis=0, keepdims=True)
        for arr, g in zip(W, [gW0, gW1, gW2]): arr -= lr * g
        for arr, g in zip(b, [gb0, gb1, gb2]): arr -= lr * g
        if epoch % 10 == 0:
            losses_train.append(float(np.mean((predict_scaled(Xs[train], W, b) - ys[train]) ** 2)))
            losses_val.append(float(np.mean((predict_scaled(Xs[val], W, b) - ys[val]) ** 2)))

    pred_test = predict_scaled(Xs[test], W, b) * scale_y + mean_y
    true_test = y[test]
    err = pred_test - true_test
    metrics = {
        "n_contracts": int(len(X)),
        "label_steps": 100,
        "test_mae": float(np.mean(np.abs(err))),
        "test_rmse": float(np.sqrt(np.mean(err**2))),
        "test_max_abs_error": float(np.max(np.abs(err))),
        "test_bias": float(np.mean(err)),
    }
    moneyness = X[test, 0] / X[test, 1]
    buckets = {
        "deep_itm_put_S_over_K_below_0.9": moneyness < 0.9,
        "near_atm_0.9_to_1.1": (moneyness >= 0.9) & (moneyness <= 1.1),
        "deep_otm_put_S_over_K_above_1.1": moneyness > 1.1,
    }
    metrics["bucket_mae"] = {
        name: float(np.mean(np.abs(err[mask]))) for name, mask in buckets.items() if np.any(mask)
    }
    save_line_svg(FIGURES / "training_loss.svg", np.arange(len(losses_train))*10, [losses_train, losses_val], ["train", "validation"], "MLP Training Loss", "epoch", "scaled MSE")
    save_scatter_svg(FIGURES / "predicted_vs_binomial.svg", true_test.ravel(), pred_test.ravel(), "Predicted vs Binomial Prices", "binomial", "neural prediction")
    np.savez(DATA / "mlp_weights.npz", mean=mean, std=std, mean_y=mean_y, scale_y=scale_y, **{f"W{i}": W[i] for i in range(3)}, **{f"b{i}": b[i] for i in range(3)})
    return {"metrics": metrics, "losses_train": losses_train, "losses_val": losses_val}


def predict_scaled(Xs, W, b):
    return relu(relu(Xs @ W[0] + b[0]) @ W[1] + b[1]) @ W[2] + b[2]


def main() -> None:
    X, y = generate_dataset()
    assert np.all(np.isfinite(y)) and np.all(y >= 0)
    intrinsic = np.maximum(X[:, 1] - X[:, 0], 0)
    assert np.all(y.ravel() + 1e-8 >= intrinsic)
    result = train_mlp(X, y)
    (ROOT / "metrics.json").write_text(json.dumps(result["metrics"], indent=2), encoding="utf-8")
    print(json.dumps(result["metrics"], indent=2))


if __name__ == "__main__":
    main()

