from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.american_put_env import AmericanPutEnv, EnvConfig, run_policy


def always_hold(state, env): return 0
def immediate_exercise(state, env): return 1
def random_policy(state, env): return int(env.rng.random() < 0.5)


def main() -> None:
    env = AmericanPutEnv(EnvConfig())
    sample = []
    for i in range(5):
        state = env.reset(100 + i)
        while True:
            action = random_policy(state, env)
            state, reward, done, info = env.step(action)
            if done:
                sample.append({"episode": i, "reason": info["reason"], "step": env.step_index, "reward": reward})
                break
    results = {
        "sample_episodes": sample,
        "always_hold": run_policy(env, always_hold, 1000, 10),
        "immediate_exercise": run_policy(env, immediate_exercise, 1000, 20),
        "random": run_policy(env, random_policy, 1000, 30),
    }
    (ROOT / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

