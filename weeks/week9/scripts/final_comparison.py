"""Week 9: collect final comparison metrics across binomial, NN, and RL."""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    week6 = load(REPO / "weeks" / "week6" / "metrics.json")
    week8 = load(REPO / "weeks" / "week8" / "metrics.json")
    comparison = {
        "binomial_benchmark": {
            "method": "CRR binomial tree",
            "american_put_price": week8["binomial_benchmark_500_steps"],
            "role": "reference price and exercise intuition",
        },
        "neural_network": {
            "method": "two-hidden-layer NumPy MLP",
            "contracts": week6["n_contracts"],
            "label_steps": week6["label_steps"],
            "test_mae": week6["test_mae"],
            "test_rmse": week6["test_rmse"],
            "test_max_abs_error": week6["test_max_abs_error"],
            "bias": week6["test_bias"],
        },
        "rl_policy": {
            "method": week8["training"]["method"],
            "training_episodes": week8["training"]["episodes"],
            "learned_value": week8["learned_tabular_q"]["mean_discounted_payoff"],
            "learned_standard_error": week8["learned_tabular_q"]["standard_error"],
            "always_hold_value": week8["always_hold"]["mean_discounted_payoff"],
            "exercise_rate": week8["learned_tabular_q"]["exercise_rate"],
            "average_exercise_step": week8["learned_tabular_q"]["average_exercise_step"],
        },
        "conclusion": "Binomial tree is the reliable benchmark; NN approximation is usable but imperfect; tabular RL is a prototype and exercises too early.",
    }
    (ROOT / "final_comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    print(json.dumps(comparison, indent=2))


if __name__ == "__main__":
    main()

