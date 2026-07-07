from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.american_put_env import AmericanPutEnv, EnvConfig


def test_payoff_non_negative():
    env = AmericanPutEnv(EnvConfig())
    env.reset(1)
    _, reward, done, _ = env.step(1)
    assert done
    assert reward >= 0


def test_cannot_step_after_done():
    env = AmericanPutEnv(EnvConfig())
    env.reset(1)
    env.step(1)
    try:
        env.step(0)
    except RuntimeError:
        return
    raise AssertionError("Expected RuntimeError after done")

