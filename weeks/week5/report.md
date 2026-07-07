# Week 5 Assignment: Intro to ML

## Objective

This week builds the machine-learning basics needed for the neural option
pricer. I implemented gradient descent for linear regression and a small ReLU
network for a nonlinear `sin(x)` target using NumPy.

## Part A: Linear Regression With Gradient Descent

Synthetic data:

```text
y = 2.5x + 1.0 + noise, x in [0, 10], 240 points
```

The data was split 80/20 into training and validation sets. I fit:

```text
y_hat = wx + b
```

using hand-written MSE gradients.

| Metric | Value |
| --- | ---: |
| Learned `w` | 2.4990 |
| Learned `b` | 0.9413 |
| True slope | 2.5000 |
| True intercept | 1.0000 |
| Train MSE | 0.7470 |
| Validation MSE | 1.0517 |

The fitted slope is very close to the true slope, so the gradient descent
implementation is working.

Generated figure:

- `figures/linear_regression_fit.svg`

## Part B: Tiny ReLU Neural Network

Nonlinear target:

```text
y = sin(x) + 0.1 noise, x in [0, 2pi], 600 points
```

Model:

- 1 input
- 1 hidden ReLU layer
- 24 hidden units
- 1 output
- MSE loss
- NumPy backpropagation

| Metric | Value |
| --- | ---: |
| Validation MAE | 0.3322 |
| Max absolute error | 1.1290 |
| Final train MSE | 0.1543 |
| Final validation MSE | 0.1683 |

Generated figures:

- `figures/relu_sine_fit.svg`
- `figures/relu_loss_curve.svg`

## Part C: Connection To Option Pricing

A linear model is not enough for the American put surface because the option
price is highly nonlinear in spot, maturity, and volatility. The surface bends
near the strike, flattens when the put is far out of the money, and is constrained
by intrinsic value when the put is deep in the money. American exercise adds an
additional kink because the model must compare continuation value with immediate
exercise value.

For Week 6, the five features are:

- `S0`: spot price
- `K`: strike
- `T`: time to maturity in years
- `r`: continuously compounded annual risk-free rate as a decimal
- `sigma`: annual volatility as a decimal

The main sanity check for the neural pricer will be non-negativity and no large
violations below intrinsic value.

## Reproducibility

```bash
python weeks/week5/scripts/ml_basics.py
```

