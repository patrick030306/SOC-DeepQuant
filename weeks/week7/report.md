# Week 7 Assignment: American Put RL Environment

## Objective

This week defines the American put exercise problem as a reinforcement-learning
environment. The option holder is the agent. At every step, the agent chooses
whether to hold or exercise.

## Part A: MDP Definition

State features:

- `time_fraction = current_step / total_steps`
- `moneyness = spot / strike`

Actions:

- `0 = hold`
- `1 = exercise`

Transition:

- If the agent exercises, the episode ends immediately.
- If the agent holds, the stock evolves one GBM step.
- At expiry, the option is automatically settled for terminal payoff.

Reward:

- Exercise reward: `max(K - S_t, 0)`
- Hold reward: `0` until expiry
- Expiry reward: `max(K - S_T, 0)`

The state does not leak future information. It contains only current time and
current moneyness, not future stock path values, future maximum payoff, or the
binomial boundary.

## Part B: Environment Implementation

Implemented:

- `weeks/week7/src/american_put_env.py`
- `AmericanPutEnv.reset()`
- `AmericanPutEnv.step(action)`
- `run_policy(...)`

Tests:

- payoff is non-negative
- cannot step after the episode is done

Test file:

- `weeks/week7/tests/test_env.py`

## Part C: Policy Comparison

Evaluation used 1,000 simulated episodes.

| Policy | Mean discounted payoff | Standard error | Exercise rate | Avg exercise step |
| --- | ---: | ---: | ---: | ---: |
| Always hold | 6.9439 | 0.3346 | 0.0000 | 50.0000 |
| Immediate exercise | 0.0000 | 0.0000 | 1.0000 | 0.0000 |
| Random | 0.9316 | 0.0691 | 1.0000 | 1.0410 |

The always-hold policy performs best among these simple baselines because
immediate exercise at `S0 = K = 100` gives zero payoff, and random exercise often
terminates too early. A good American put policy should exercise mainly when the
option is sufficiently in the money, not randomly or immediately at the money.

## Reproducibility

```bash
python weeks/week7/scripts/evaluate_policies.py
```

