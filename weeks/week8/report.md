# Week 8 Assignment: Train And Evaluate An RL Stopping Policy

## Objective

This week trains and evaluates a value-based stopping policy for the American
put environment from Week 7.

The course allows a DQN or a clearly explained stronger tabular baseline. Since
PyTorch is unavailable in the local runtime, I implemented tabular Q-learning
over discretized time and moneyness.

## Part A: Training Setup

Contract parameters:

| Parameter | Value |
| --- | ---: |
| `S0` | 100 |
| `K` | 100 |
| `T` | 1.0 |
| `r` | 0.05 |
| `sigma` | 0.25 |
| Environment steps | 50 |

Training setup:

| Item | Value |
| --- | ---: |
| Method | Tabular Q-learning |
| Episodes | 12,000 |
| Learning rate alpha | 0.08 |
| Seed | 91 |
| State grid | 10 time bins x 15 moneyness bins |
| Actions | hold, exercise |

The state uses only current time fraction and current moneyness. It does not
include future prices or binomial boundary labels.

## Part B: Evaluation

Final evaluation used 5,000 episodes.

| Policy | Mean discounted payoff | Standard error | Exercise rate | Avg exercise step |
| --- | ---: | ---: | ---: | ---: |
| Always hold | 7.2553 | 0.1521 | 0.0000 | 50.0000 |
| Immediate exercise | 0.0000 | 0.0000 | 1.0000 | 0.0000 |
| Random | 0.8988 | 0.0305 | 1.0000 | 1.0264 |
| Learned tabular Q | 5.2673 | 0.0661 | 0.7624 | 22.2888 |

Week 4 binomial benchmark on the matching core contract:

```text
CRR American put price, 500 steps = 7.9724
```

Generated figure:

- `figures/exercise_region.svg`

## Part C: Analysis

The learned tabular policy is not yet strong enough. It improves substantially
over random exercise, but it underperforms always-hold and the binomial
benchmark. The main issue is that it exercises too early too often: the exercise
rate is about 76.24%, with average exercise around step 22.3 out of 50.

This makes the result a useful prototype rather than a production-quality RL
policy. It shows the environment and training loop are working end-to-end, but
the policy needs better state representation, more stable value approximation,
or a DQN-style function approximator to learn a smoother boundary.

## Reproducibility

```bash
python weeks/week8/scripts/train_tabular_q.py
```

