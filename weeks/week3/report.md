# Week 3 Assignment: Hand-Worked American Put Tree

## Inputs

| Parameter | Value |
| --- | ---: |
| Spot price, `S0` | 100 |
| Strike, `K` | 100 |
| Risk-free rate, `r` | 6% |
| Volatility, `sigma` | 25% |
| Time to maturity, `T` | 1 year |
| Steps, `N` | 3 |

## CRR Parameters

```text
dt = T / N = 1 / 3 = 0.3333
u = exp(sigma * sqrt(dt)) = 1.1553
d = 1 / u = 0.8656
p = [exp(r dt) - d] / [u - d] = 0.5337
discount = exp(-r dt) = 0.9802
```

The tree recombines because `u * d = 1`.

## Stock Price Tree

| Time | Stock prices |
| --- | --- |
| 0 | 100.0000 |
| 1 | 86.5596, 115.5274 |
| 2 | 74.9256, 100.0000, 133.4658 |
| 3 | 64.8552, 86.5596, 115.5274, 154.1896 |

## European Put Backward Induction

Terminal payoff is `max(K - S, 0)`.

| Time | European put node values |
| --- | --- |
| 3 | 35.1448, 13.4404, 0.0000, 0.0000 |
| 2 | 23.0943, 6.1430, 0.0000 |
| 1 | 13.7690, 2.8077 |
| 0 | 7.7620 |

So the 3-step European put value is:

```text
European put = 7.7620
```

## American Put Backward Induction

For the American put, each node value is:

```text
max(continuation value, immediate exercise value)
```

| Time | American put node values |
| --- | --- |
| 3 | 35.1448, 13.4404, 0.0000, 0.0000 |
| 2 | 25.0744, 6.1430, 0.0000 |
| 1 | 14.6740, 2.8077 |
| 0 | 8.1756 |

At time 2, the lowest stock node is `S = 74.9256`. Immediate exercise gives:

```text
K - S = 100 - 74.9256 = 25.0744
```

This is larger than continuation value, so early exercise is optimal at that
node. At the other non-terminal nodes, holding is better.

## Early-Exercise Premium

```text
Premium = American put - European put
        = 8.1756 - 7.7620
        = 0.4136
```

The premium is positive, as expected. The right to exercise early cannot reduce
the option value.

## Exercise Boundary

For this 3-step tree, early exercise is optimal at:

- Time 2, lowest stock node: `S = 74.9256`
- Terminal in-the-money nodes are exercised at expiry by definition.

This means the early-exercise region appears when the put is deep in the money,
close to maturity.

## Delta

Using the first layer of the American put tree:

```text
delta = (f_up - f_down) / (S_up - S_down)
      = (2.8077 - 14.6740) / (115.5274 - 86.5596)
      = -0.4096
```

The negative delta makes financial sense because put values fall when the stock
price rises.

## Reflection

Early exercise appears in the deep in-the-money region, where the stock price is
well below the strike. With positive interest rates, exercising a put can be
valuable because the holder receives the strike cash sooner. This matches the
intuition from Week 2: American puts need a tree or another numerical method
because the early-exercise decision has to be checked at each node.

