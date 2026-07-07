# SOC DeepQuant - American Option Pricing

This repository contains my week-by-week work for the American Option Pricing
SOC project. The project moves from option-pricing fundamentals to a final
comparison of binomial trees, neural-network approximation, and reinforcement
learning for American put options.

## Week-by-Week Structure

| Week | Topic | Folder | Deliverable |
| --- | --- | --- | --- |
| 1 | Basics of Options | `weeks/week1/` | Options advisory memo |
| 2 | Black-Scholes | `weeks/week2/` | Black-Scholes pricing memo |
| 3 | Binomial Model | `weeks/week3/` | Hand-worked American put tree |
| 4 | Code the Baseline | `weeks/week4/` | CRR pricer, tests, figures, report |
| 5 | Intro to ML | `weeks/week5/` | Gradient descent and tiny ReLU net |
| 6 | NN on Synthetic Data | `weeks/week6/` | Neural pricer trained on CRR labels |
| 7 | Reinforcement Learning | `weeks/week7/` | American put RL environment |
| 8 | Train RL | `weeks/week8/` | Tabular Q-learning stopping policy |
| 9 | Compare and Ship | `weeks/week9/` | Final comparison report |

## Core Results

For the benchmark contract `S0 = 100`, `K = 100`, `T = 1`, `r = 5%`,
`sigma = 25%`:

| Method | Main result |
| --- | ---: |
| CRR binomial, 500 steps | 7.9724 American put price |
| Neural pricer, 10,000 synthetic labels | 1.8437 test MAE |
| Tabular Q-learning policy | 5.2673 estimated policy value |
| Always-hold baseline | 7.2553 estimated policy value |

The binomial tree remains the most reliable benchmark. The neural network gives
a usable first approximation but still has meaningful pricing error. The
tabular RL policy is a prototype and exercises too early, which is discussed in
Weeks 8-9.

## Reproducibility

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the main scripts:

```bash
python weeks/week4/scripts/run_sanity_checks.py
python weeks/week5/scripts/ml_basics.py
python weeks/week6/scripts/train_neural_pricer.py
python weeks/week7/scripts/evaluate_policies.py
python weeks/week8/scripts/train_tabular_q.py
python weeks/week9/scripts/final_comparison.py
```

Dependency note: the local runtime used for this repository had NumPy and
pandas but did not have PyTorch or Matplotlib. Therefore, Weeks 5-9 use NumPy
implementations and dependency-free SVG figures.

## Repository Layout

```text
.
|-- weeks/
|   |-- week1/ ... week9/
|-- requirements.txt
`-- README.md
```

