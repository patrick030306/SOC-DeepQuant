"""Cox-Ross-Rubinstein binomial tree pricing utilities."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, sqrt

import numpy as np


@dataclass(frozen=True)
class CRRParameters:
    """Derived one-step CRR parameters."""

    dt: float
    u: float
    d: float
    p: float
    discount: float


def crr_parameters(T: float, r: float, sigma: float, steps: int) -> CRRParameters:
    """Return CRR tree parameters for annualized inputs."""

    if T <= 0:
        raise ValueError("T must be positive and measured in years.")
    if sigma <= 0:
        raise ValueError("sigma must be positive and expressed as a decimal.")
    if steps < 1 or int(steps) != steps:
        raise ValueError("steps must be a positive integer.")

    steps = int(steps)
    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = 1.0 / u
    growth = exp(r * dt)
    p = (growth - d) / (u - d)
    if not 0 < p < 1:
        raise ValueError("Risk-neutral probability is outside (0, 1).")
    return CRRParameters(dt=dt, u=u, d=d, p=p, discount=exp(-r * dt))


def crr_put_price(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    steps: int,
    american: bool = True,
) -> float:
    """Price a European or American put using a CRR binomial tree."""

    if S0 <= 0:
        raise ValueError("S0 must be positive.")
    if K <= 0:
        raise ValueError("K must be positive.")

    params = crr_parameters(T=T, r=r, sigma=sigma, steps=steps)
    steps = int(steps)

    j = np.arange(steps + 1)
    stock = S0 * (params.u ** j) * (params.d ** (steps - j))
    value = np.maximum(K - stock, 0.0)

    for i in range(steps - 1, -1, -1):
        value = params.discount * (
            params.p * value[1 : i + 2] + (1.0 - params.p) * value[0 : i + 1]
        )
        if american:
            j = np.arange(i + 1)
            stock = S0 * (params.u ** j) * (params.d ** (i - j))
            exercise = np.maximum(K - stock, 0.0)
            value = np.maximum(value, exercise)

    return float(value[0])


def crr_put_tree_details(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    steps: int,
) -> dict[str, object]:
    """Return stock tree, European values, American values, and exercise flags."""

    if S0 <= 0 or K <= 0:
        raise ValueError("S0 and K must be positive.")

    params = crr_parameters(T=T, r=r, sigma=sigma, steps=steps)
    steps = int(steps)
    stock_layers: list[np.ndarray] = []
    for i in range(steps + 1):
        j = np.arange(i + 1)
        stock_layers.append(S0 * (params.u ** j) * (params.d ** (i - j)))

    euro_layers: list[np.ndarray | None] = [None] * (steps + 1)
    amer_layers: list[np.ndarray | None] = [None] * (steps + 1)
    exercise_layers: list[np.ndarray | None] = [None] * (steps + 1)

    terminal = np.maximum(K - stock_layers[-1], 0.0)
    euro_layers[-1] = terminal.copy()
    amer_layers[-1] = terminal.copy()
    exercise_layers[-1] = terminal > 0

    euro = terminal.copy()
    amer = terminal.copy()
    for i in range(steps - 1, -1, -1):
        euro = params.discount * (
            params.p * euro[1 : i + 2] + (1.0 - params.p) * euro[0 : i + 1]
        )
        continuation = params.discount * (
            params.p * amer[1 : i + 2] + (1.0 - params.p) * amer[0 : i + 1]
        )
        exercise = np.maximum(K - stock_layers[i], 0.0)
        amer = np.maximum(continuation, exercise)
        euro_layers[i] = euro.copy()
        amer_layers[i] = amer.copy()
        exercise_layers[i] = exercise > continuation + 1e-12

    return {
        "params": params,
        "stock_layers": stock_layers,
        "european_layers": euro_layers,
        "american_layers": amer_layers,
        "exercise_layers": exercise_layers,
    }


def exercise_boundary(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    steps: int,
) -> tuple[float, list[tuple[float, float]]]:
    """Return American put price and highest exercise stock per time layer."""

    details = crr_put_tree_details(S0, K, T, r, sigma, steps)
    params = details["params"]
    stock_layers = details["stock_layers"]
    exercise_layers = details["exercise_layers"]

    boundary: list[tuple[float, float]] = []
    for i in range(steps + 1):
        flags = exercise_layers[i]
        stocks = stock_layers[i]
        if flags is not None and np.any(flags):
            boundary.append((i * params.dt, float(np.max(stocks[flags]))))

    price = float(details["american_layers"][0][0])
    return price, boundary

