"""American put optimal-stopping environment."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, sqrt

import numpy as np


@dataclass
class EnvConfig:
    S0: float = 100.0
    K: float = 100.0
    T: float = 1.0
    r: float = 0.05
    sigma: float = 0.25
    steps: int = 50
    seed: int = 123


class AmericanPutEnv:
    """A small no-leakage American put exercise environment."""

    def __init__(self, config: EnvConfig | None = None):
        self.config = config or EnvConfig()
        self.rng = np.random.default_rng(self.config.seed)
        self.dt = self.config.T / self.config.steps
        self.discount = exp(-self.config.r * self.dt)
        self.done = True
        self.step_index = 0
        self.spot = self.config.S0

    def reset(self, seed: int | None = None) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.done = False
        self.step_index = 0
        self.spot = self.config.S0
        return self.state()

    def state(self) -> np.ndarray:
        time_fraction = self.step_index / self.config.steps
        return np.array([time_fraction, self.spot / self.config.K], dtype=float)

    def step(self, action: int):
        if self.done:
            raise RuntimeError("Cannot step after episode is done.")
        if action not in (0, 1):
            raise ValueError("action must be 0=hold or 1=exercise.")

        payoff = max(self.config.K - self.spot, 0.0)
        if action == 1:
            self.done = True
            return self.state(), payoff, True, {"reason": "exercise"}

        self.step_index += 1
        z = self.rng.normal()
        drift = (self.config.r - 0.5 * self.config.sigma**2) * self.dt
        shock = self.config.sigma * sqrt(self.dt) * z
        self.spot *= exp(drift + shock)

        if self.step_index >= self.config.steps:
            self.done = True
            return self.state(), max(self.config.K - self.spot, 0.0), True, {"reason": "expiry"}

        return self.state(), 0.0, False, {"reason": "hold"}


def run_policy(env: AmericanPutEnv, policy, episodes: int = 1000, seed: int = 0) -> dict[str, float]:
    payoffs, exercise_steps, exercised = [], [], []
    for i in range(episodes):
        state = env.reset(seed + i)
        total = 0.0
        gamma = 1.0
        while True:
            action = policy(state, env)
            state, reward, done, info = env.step(action)
            total += gamma * reward
            if done:
                payoffs.append(total)
                exercised.append(1.0 if info["reason"] == "exercise" else 0.0)
                exercise_steps.append(env.step_index)
                break
            gamma *= env.discount
    arr = np.array(payoffs)
    return {
        "episodes": episodes,
        "mean_discounted_payoff": float(arr.mean()),
        "standard_error": float(arr.std(ddof=1) / np.sqrt(len(arr))),
        "exercise_rate": float(np.mean(exercised)),
        "average_exercise_step": float(np.mean(exercise_steps)),
    }

