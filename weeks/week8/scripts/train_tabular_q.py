"""Week 8: tabular Q-learning baseline for American put stopping."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WEEK4 = REPO / "weeks" / "week4"
WEEK7 = REPO / "weeks" / "week7"
sys.path.insert(0, str(WEEK7))

from src.american_put_env import AmericanPutEnv, EnvConfig, run_policy

crr_spec = importlib.util.spec_from_file_location("week4_crr", WEEK4 / "src" / "crr.py")
week4_crr = importlib.util.module_from_spec(crr_spec)
assert crr_spec.loader is not None
sys.modules["week4_crr"] = week4_crr
crr_spec.loader.exec_module(week4_crr)
crr_put_price = week4_crr.crr_put_price


FIGURES = ROOT / "figures"
DATA = ROOT / "data"
FIGURES.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)


def bins_for_state(state):
    t, m = state
    ti = min(9, max(0, int(t * 10)))
    mi = min(14, max(0, int((m - 0.55) / 0.06)))
    return ti, mi


def train(seed: int = 91):
    env = AmericanPutEnv(EnvConfig(steps=50, seed=seed))
    rng = np.random.default_rng(seed)
    Q = np.zeros((10, 15, 2))
    alpha, gamma = 0.08, env.discount
    epsilon_start, epsilon_min, decay = 1.0, 0.05, 0.997
    episodes = 12000
    for ep in range(episodes):
        state = env.reset(seed + ep)
        epsilon = max(epsilon_min, epsilon_start * (decay ** ep))
        while True:
            ti, mi = bins_for_state(state)
            action = int(rng.integers(0, 2)) if rng.random() < epsilon else int(np.argmax(Q[ti, mi]))
            next_state, reward, done, _ = env.step(action)
            nti, nmi = bins_for_state(next_state)
            target = reward if done else reward + gamma * np.max(Q[nti, nmi])
            Q[ti, mi, action] += alpha * (target - Q[ti, mi, action])
            state = next_state
            if done:
                break
    np.save(DATA / "tabular_q.npy", Q)
    return Q


def q_policy(Q):
    def policy(state, env):
        return int(np.argmax(Q[bins_for_state(state)]))
    return policy


def save_region_svg(Q):
    cell = 28
    width, height = 15 * cell + 140, 10 * cell + 110
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        '<text x="280" y="28" text-anchor="middle" font-size="20" font-family="Arial">Learned Exercise Region</text>',
    ]
    for t in range(10):
        for m in range(15):
            exercise = np.argmax(Q[t, m]) == 1
            color = "#d73a49" if exercise else "#1f6feb"
            x = 70 + m * cell
            y = 55 + t * cell
            pieces.append(f'<rect x="{x}" y="{y}" width="{cell-1}" height="{cell-1}" fill="{color}" opacity="0.78" />')
    pieces.extend([
        '<text x="280" y="365" text-anchor="middle" font-size="13" font-family="Arial">Moneyness S/K increases left to right</text>',
        '<text x="20" y="190" text-anchor="middle" font-size="13" font-family="Arial" transform="rotate(-90 20 190)">Time fraction increases downward</text>',
        '<text x="525" y="90" font-size="13" font-family="Arial" fill="#d73a49">red = exercise</text>',
        '<text x="525" y="112" font-size="13" font-family="Arial" fill="#1f6feb">blue = hold</text>',
        "</svg>",
    ])
    (FIGURES / "exercise_region.svg").write_text("\n".join(pieces), encoding="utf-8")


def always_hold(state, env): return 0
def immediate_exercise(state, env): return 1
def random_policy(state, env): return int(env.rng.random() < 0.5)


def main():
    Q = train()
    env = AmericanPutEnv(EnvConfig(steps=50, seed=123))
    benchmark = crr_put_price(100, 100, 1.0, 0.05, 0.25, 500, american=True)
    results = {
        "contract": {"S0": 100, "K": 100, "T": 1.0, "r": 0.05, "sigma": 0.25, "steps": 50},
        "training": {"method": "tabular Q-learning", "episodes": 12000, "seed": 91, "alpha": 0.08},
        "binomial_benchmark_500_steps": benchmark,
        "always_hold": run_policy(env, always_hold, 5000, 1),
        "immediate_exercise": run_policy(env, immediate_exercise, 5000, 2),
        "random": run_policy(env, random_policy, 5000, 3),
        "learned_tabular_q": run_policy(env, q_policy(Q), 5000, 4),
    }
    save_region_svg(Q)
    (ROOT / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
