# Week 4 Assignment: CRR American Put Baseline

## Objective

Week 4 turns the hand-built binomial tree into a reusable Python baseline for
American put pricing. The baseline uses the Cox-Ross-Rubinstein tree and
backward induction.

Core implementation:

```python
crr_put_price(S0, K, T, r, sigma, steps, american=True)
```

The implementation lives in `src/crr.py`.

## Model

The CRR parameters are:

```text
dt = T / N
u = exp(sigma * sqrt(dt))
d = 1 / u
p = [exp(r dt) - d] / [u - d]
discount = exp(-r dt)
```

At maturity, the put payoff is:

```text
max(K - S, 0)
```

At each earlier node, the European value is the discounted risk-neutral
continuation value. The American value is:

```text
max(continuation value, K - S)
```

This final maximum is the early-exercise feature.

## Required Pricing Case

Inputs:

- `S0 = 100`
- `K = 100`
- `T = 1`
- `r = 5%`
- `sigma = 25%`
- `steps = 500`

Results:

| Quantity | Value |
| --- | ---: |
| European put | 7.453999 |
| American put | 7.972371 |
| Early-exercise premium | 0.518373 |

The American price is higher than the European price, which is required because
early exercise adds flexibility.

## Sanity Tests

The following tests are included in `tests/test_crr.py`:

- American put price is not below European put price.
- Put value falls as spot price rises.
- Put value increases when volatility increases.
- Deep in-the-money American put is at least intrinsic value.

For environments without `pytest`, the same checks can be run through:

```bash
python scripts/run_sanity_checks.py
```

Verification result:

```text
All sanity checks passed.
```

## Convergence Table

| Steps | American put price |
| ---: | ---: |
| 25 | 8.052667 |
| 50 | 7.952030 |
| 100 | 7.963611 |
| 200 | 7.969091 |
| 500 | 7.972371 |
| 1000 | 7.973439 |

The price stabilizes as the number of steps increases. The difference between
500 and 1000 steps is about `0.0011`, so 500 steps is a reasonable default for
report-quality examples in this assignment.

## Visualizations

Generated figures:

- `figures/week4_price_surface.svg`
- `figures/week4_exercise_boundary.svg`

The price surface uses spot prices from 60 to 140 and maturities from 0.05 to
2.0 years. The surface is highest when the spot price is low, because the put is
deep in the money. It becomes small when the spot price is far above the strike.

The exercise-boundary plot records the highest stock price at which immediate
exercise is optimal. The boundary is below the strike, showing that early
exercise appears primarily in deep in-the-money states.

## Reflection

The American put differs from the European put because the holder can stop early.
In the CRR tree, this is handled by comparing continuation value with immediate
exercise value at every node. Early exercise appears when the option is deep in
the money and close enough to maturity that waiting is less attractive than
receiving `K - S` immediately.

This baseline is important for later machine-learning work. A neural network or
reinforcement-learning model needs a reference target. For American puts, a
high-step binomial tree is a practical benchmark because there is no simple
closed-form Black-Scholes equivalent with early exercise.

