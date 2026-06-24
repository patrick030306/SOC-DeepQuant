# American Option Pricing - Midterm Repository

This repository tracks my work for the American Option Pricing SOC project.

The first four weeks cover option basics, Black-Scholes pricing, binomial trees,
and a coded CRR baseline for American put pricing. The midterm submission will
include written reports, reproducible Python code, tests, and generated figures.

## Current Scope

| Week | Topic | Main Deliverable | Status |
| --- | --- | --- | --- |
| 1 | Basics of Options | Real-world options advisory memo | Complete |
| 2 | Black-Scholes | Pricing memo and model calculation | Complete |
| 3 | Binomial Model | Hand-worked American put tree | Complete |
| 4 | Code the Baseline | CRR American put pricer, tests, plots | Complete |

## Repository Layout

```text
.
├── data/              # Input data, if needed
├── figures/           # Saved plots for reports
├── notebooks/         # Exploratory notebooks
├── reports/           # Weekly written reports
├── scripts/           # Reproducible output and sanity-check scripts
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

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests with pytest:

```bash
pytest
```

Run dependency-light sanity checks:

```bash
python scripts/run_sanity_checks.py
```

Regenerate Week 4 outputs:

```bash
python scripts/generate_week4_outputs.py
```

## Midterm Checklist

- [x] Week 1 report completed
- [x] Week 2 report completed
- [x] Week 3 calculations completed and checked
- [x] Week 4 pricer implemented
- [x] Tests passing
- [x] Figures generated
- [x] README updated with final results
- [ ] GitHub repository submitted

## Key Week 4 Results

For `S0 = 100`, `K = 100`, `T = 1`, `r = 5%`, `sigma = 25%`, and
`steps = 500`:

| Quantity | Value |
| --- | ---: |
| European put | 7.453999 |
| American put | 7.972371 |
| Early-exercise premium | 0.518373 |

