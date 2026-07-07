# Week 9 Final Project Submission

## Objective

The final project integrates the course methods for American put pricing:

- CRR binomial tree benchmark
- Neural-network price approximation
- RL stopping policy

The goal is to compare the methods under shared assumptions and explain where
each method works or fails.

## Repository Structure

The project is organized week by week:

```text
weeks/week1  option basics memo
weeks/week2  Black-Scholes memo
weeks/week3  hand-worked binomial tree
weeks/week4  CRR binomial implementation
weeks/week5  ML basics
weeks/week6  neural network pricer
weeks/week7  RL environment
weeks/week8  RL training/evaluation
weeks/week9  final comparison
```

## Binomial Benchmark

The CRR binomial tree remains the reference model because American puts do not
have a simple closed-form Black-Scholes price.

For the main contract:

| Parameter | Value |
| --- | ---: |
| `S0` | 100 |
| `K` | 100 |
| `T` | 1 |
| `r` | 5% |
| `sigma` | 25% |
| Tree steps | 500 |

Week 4 benchmark:

```text
American put price = 7.9724
```

## Neural Network Comparison

The Week 6 neural pricer was trained on 10,000 synthetic contracts labelled by
the CRR pricer with 100 tree steps.

| Metric | Value |
| --- | ---: |
| Test MAE | 1.8437 |
| Test RMSE | 2.3319 |
| Max absolute error | 9.7703 |
| Bias | 0.1347 |

The neural network is faster after training but less reliable than the tree. It
works as a first approximation and exposes where more tuning/data are needed.

## RL Policy Comparison

The Week 8 tabular Q-learning policy was evaluated against simple baselines and
the binomial benchmark.

| Method | Value |
| --- | ---: |
| Binomial benchmark | 7.9724 |
| Always hold | 7.2553 |
| Immediate exercise | 0.0000 |
| Random | 0.8988 |
| Learned tabular Q | 5.2673 |

The learned policy underperforms the benchmark because it exercises too early.
This result is still useful because it identifies the main RL failure mode and
shows why policy evaluation must be compared against a binomial anchor.

## Final Assessment

| Method | Strength | Weakness |
| --- | --- | --- |
| CRR binomial | Accurate, interpretable, handles early exercise | Slower for large datasets |
| Neural network | Fast inference after training | Approximation errors and possible finance-rule violations |
| RL stopping policy | Directly models exercise vs hold | Training instability and early-exercise mistakes |

## Limitations

- The neural model is a NumPy MLP rather than PyTorch due to local dependency
  limits.
- The RL model is tabular Q-learning, not a full DQN.
- Synthetic labels are generated from the binomial model, so the ML model learns
  the benchmark, not market prices.
- The RL policy needs more robust function approximation before it can match the
  binomial stopping rule.

## Reproducibility

Run the final comparison:

```bash
python weeks/week9/scripts/final_comparison.py
```

Key supporting commands:

```bash
python weeks/week5/scripts/ml_basics.py
python weeks/week6/scripts/train_neural_pricer.py
python weeks/week7/scripts/evaluate_policies.py
python weeks/week8/scripts/train_tabular_q.py
```

