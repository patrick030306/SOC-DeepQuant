# SOC DeepQuant - American Option Pricing

This repository contains my week-by-week work for the American Option Pricing
SOC project. Each assignment is kept in its own folder so the midterm submission
is easy to review.

## Week-by-Week Structure

| Week | Topic | Folder | Deliverable |
| --- | --- | --- | --- |
| 1 | Basics of Options | `weeks/week1/` | Options advisory memo |
| 2 | Black-Scholes | `weeks/week2/` | Black-Scholes pricing memo |
| 3 | Binomial Model | `weeks/week3/` | Hand-worked American put tree |
| 4 | Code the Baseline | `weeks/week4/` | CRR pricer, tests, figures, report |

## Repository Layout

```text
.
|-- weeks/
|   |-- week1/
|   |   `-- report.md
|   |-- week2/
|   |   `-- report.md
|   |-- week3/
|   |   `-- report.md
|   `-- week4/
|       |-- report.md
|       |-- src/
|       |   `-- crr.py
|       |-- tests/
|       |   `-- test_crr.py
|       |-- scripts/
|       |   |-- generate_week4_outputs.py
|       |   `-- run_sanity_checks.py
|       `-- figures/
|           |-- week4_exercise_boundary.svg
|           `-- week4_price_surface.svg
|-- requirements.txt
`-- README.md
```

## Week 4 Reproducibility

Install dependencies from the repository root:

```bash
pip install -r requirements.txt
```

Run the Week 4 sanity checks:

```bash
python weeks/week4/scripts/run_sanity_checks.py
```

Regenerate the Week 4 figures and convergence output:

```bash
python weeks/week4/scripts/generate_week4_outputs.py
```

Run the Week 4 pytest suite:

```bash
python -m pytest weeks/week4/tests
```

## Key Week 4 Results

For `S0 = 100`, `K = 100`, `T = 1`, `r = 5%`, `sigma = 25%`, and
`steps = 500`:

| Quantity | Value |
| --- | ---: |
| European put | 7.453999 |
| American put | 7.972371 |
| Early-exercise premium | 0.518373 |

