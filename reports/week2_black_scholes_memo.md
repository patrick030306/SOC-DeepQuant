# Week 2 Assignment: Black-Scholes Pricing Memo

## Objective

This memo applies the Black-Scholes model to a market-style European option
example and interprets the result. The purpose is not to claim that the model is
perfect, but to understand what the formula says and where it breaks down for
American options.

## Contract And Inputs

Example contract:

- Underlying: Apple Inc. style equity option
- Option type: European call and put comparison
- Spot price, `S`: 195
- Strike price, `K`: 200
- Time to maturity, `T`: 30 / 365 = 0.0822 years
- Risk-free rate, `r`: 5.00% annually
- Volatility, `sigma`: 25.00% annually

These inputs represent a near-the-money, one-month option. In a live submission,
the same workflow can be repeated with a downloaded option-chain row by replacing
`S`, `K`, `T`, `r`, and `sigma`.

## Formula

For a non-dividend-paying European call:

```text
C = S N(d1) - K e^(-rT) N(d2)
```

For a European put:

```text
P = K e^(-rT) N(-d2) - S N(-d1)
```

where:

```text
d1 = [ln(S/K) + (r + sigma^2 / 2)T] / [sigma sqrt(T)]
d2 = d1 - sigma sqrt(T)
```

## Calculation

Using the inputs above:

| Quantity | Value |
| --- | ---: |
| `d1` | -0.2601 |
| `d2` | -0.3317 |
| `N(d1)` | 0.3974 |
| `N(d2)` | 0.3700 |
| Black-Scholes call value | 3.7891 |
| Black-Scholes put value | 7.9689 |

The put is more expensive than the call because the spot price is below the
strike. The contract is slightly out of the money for the call and slightly in
the money for the put.

## Greeks

Approximate Greeks from the same inputs:

| Greek | Interpretation | Value |
| --- | --- | ---: |
| Call delta | Change in call price for a 1-unit rise in spot | 0.3974 |
| Put delta | Change in put price for a 1-unit rise in spot | -0.6026 |
| Gamma | Curvature of price with respect to spot | 0.0276 |
| Vega | Price change for a 1 percentage-point rise in volatility | 0.2156 |

The call delta below 0.5 makes sense because the call is out of the money. The
put delta is negative because puts gain value when the stock falls.

## Put-Call Parity Check

European prices should satisfy:

```text
C - P = S - K e^(-rT)
```

With the values above, both sides are approximately `-4.1798`, so the call and
put values are internally consistent.

## Limitations

Black-Scholes is a clean benchmark, but it relies on strong assumptions:

- Constant volatility
- Constant risk-free rate
- Lognormal stock dynamics
- Frictionless trading
- No early exercise

The final point is the most important for this project. Black-Scholes directly
prices European options. It does not solve the American put early-exercise
problem. For American puts, the holder may exercise early when the option is
deep in the money, especially with positive interest rates. That is why Week 3
and Week 4 move to binomial trees.

## Reflection

Black-Scholes gives a useful first benchmark and teaches how option prices react
to spot, time, volatility, and rates. However, it cannot fully price American
puts because early exercise turns the problem into an optimal-stopping problem.
The binomial model is a natural next step because it can compare continuation
value with immediate exercise value at every node.

