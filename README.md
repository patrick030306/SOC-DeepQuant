# American Option Pricing - Midterm Repository

This repository tracks my work for the American Option Pricing SOC project.

The first four weeks cover option basics, Black-Scholes pricing, binomial trees,
and a coded CRR baseline for American put pricing. The midterm submission will
include written reports, reproducible Python code, tests, and generated figures.

## Current Scope

| Week | Topic | Main Deliverable | Status |
| --- | --- | --- | --- |
| 1 | Basics of Options | Real-world options advisory memo | Planned |
| 2 | Black-Scholes | Pricing memo on a real options chain | Planned |
| 3 | Binomial Model | Hand-worked American put tree | Planned |
| 4 | Code the Baseline | CRR American put pricer, tests, plots | Planned |

## Repository Layout

```text
.
├── data/              # Input data, if needed
├── figures/           # Saved plots for reports
├── notebooks/         # Exploratory notebooks
├── reports/           # Weekly written reports
├── src/               # Reusable pricing code
├── tests/             # Unit and sanity tests
├── requirements.txt   # Python dependencies
└── README.md
```

## Planned Week 4 API

```python
crr_put_price(S0, K, T, r, sigma, steps, american=True)
```

The implementation will use the Cox-Ross-Rubinstein binomial tree with backward
induction. For American puts, each node will compare continuation value with
immediate exercise value.

## Reproducibility

After implementation, the intended workflow will be:

```bash
pip install -r requirements.txt
pytest
python scripts/generate_week4_outputs.py
```

## Midterm Checklist

- [ ] Week 1 report completed
- [ ] Week 2 report completed
- [ ] Week 3 calculations completed and checked
- [ ] Week 4 pricer implemented
- [ ] Tests passing
- [ ] Figures generated
- [ ] README updated with final results
- [ ] GitHub repository submitted

