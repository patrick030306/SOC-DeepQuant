# Week 6 Assignment: Neural Network On Synthetic Option Data

## Objective

This week trains a neural network to approximate American put prices generated
by the Week 4 CRR binomial pricer.

The course asks for a PyTorch MLP. The local runtime available for this project
does not include PyTorch, so I implemented the same MLP idea using NumPy:
two hidden ReLU layers, standardized inputs, train/validation/test split, and
manual backpropagation.

## Part A: Dataset Generation

I generated 10,000 synthetic contracts with the following ranges:

| Feature | Range |
| --- | --- |
| `S0` | 60 to 140 |
| `K` | 80 to 120 |
| `T` | 0.05 to 2.0 years |
| `r` | 0.00 to 0.10 |
| `sigma` | 0.10 to 0.50 |

Labels were generated using:

```python
crr_put_price(S0, K, T, r, sigma, steps=100, american=True)
```

Label checks:

- all labels finite
- all labels non-negative
- all labels at least intrinsic value

Dataset file:

- `data/synthetic_contracts.csv`

## Part B: Training

Model:

- Input dimension: 5
- Hidden layers: 48 and 32 ReLU units
- Output: American put price
- Loss: MSE on standardized target
- Split: 80% train, 10% validation, 10% test

Generated artifacts:

- `data/mlp_weights.npz`
- `figures/training_loss.svg`
- `figures/predicted_vs_binomial.svg`

## Part C: Evaluation

| Metric | Value |
| --- | ---: |
| Test MAE | 1.8437 |
| Test RMSE | 2.3319 |
| Max absolute error | 9.7703 |
| Bias | 0.1347 |

MAE by moneyness bucket:

| Bucket | MAE |
| --- | ---: |
| Deep ITM put, `S/K < 0.9` | 2.0985 |
| Near ATM, `0.9 <= S/K <= 1.1` | 1.6434 |
| Deep OTM put, `S/K > 1.1` | 1.7300 |

The model learns the broad pricing surface but is still a prototype. The largest
errors occur in regions where the surface changes quickly or where the early
exercise constraint creates kinks. This is expected for a small MLP trained from
scratch without extensive hyperparameter tuning.

## Reflection

The neural network approximates the binomial pricer, not the true market price.
Its value is speed after training: once fitted, it can estimate prices without
running a full tree for every contract. The risk is that it can violate financial
structure unless we test non-negativity, intrinsic value, monotonicity in spot,
and errors by moneyness.

## Reproducibility

```bash
python weeks/week6/scripts/train_neural_pricer.py
```

