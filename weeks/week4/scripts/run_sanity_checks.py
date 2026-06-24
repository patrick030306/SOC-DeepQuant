"""Run core finance sanity checks without requiring pytest."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.crr import crr_put_price


def main() -> None:
    args = dict(S0=100, K=100, T=1.0, r=0.05, sigma=0.25, steps=500)
    euro = crr_put_price(**args, american=False)
    amer = crr_put_price(**args, american=True)
    assert amer >= euro

    low_spot = crr_put_price(80, 100, 1.0, 0.05, 0.25, 300, american=True)
    high_spot = crr_put_price(120, 100, 1.0, 0.05, 0.25, 300, american=True)
    assert low_spot > high_spot

    low_vol = crr_put_price(100, 100, 1.0, 0.05, 0.15, 300, american=True)
    high_vol = crr_put_price(100, 100, 1.0, 0.05, 0.35, 300, american=True)
    assert high_vol >= low_vol

    deep_itm = crr_put_price(70, 100, 1.0, 0.05, 0.25, 300, american=True)
    assert deep_itm >= 30

    print("All sanity checks passed.")


if __name__ == "__main__":
    main()
