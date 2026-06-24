from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.crr import crr_put_price


def test_american_put_not_less_than_european():
    args = dict(S0=100, K=100, T=1.0, r=0.05, sigma=0.25, steps=500)
    euro = crr_put_price(**args, american=False)
    amer = crr_put_price(**args, american=True)
    assert amer >= euro


def test_put_value_falls_as_spot_rises():
    low_spot = crr_put_price(80, 100, 1.0, 0.05, 0.25, 300, american=True)
    high_spot = crr_put_price(120, 100, 1.0, 0.05, 0.25, 300, american=True)
    assert low_spot > high_spot


def test_put_value_increases_with_volatility():
    low_vol = crr_put_price(100, 100, 1.0, 0.05, 0.15, 300, american=True)
    high_vol = crr_put_price(100, 100, 1.0, 0.05, 0.35, 300, american=True)
    assert high_vol >= low_vol


def test_american_put_above_intrinsic_value():
    price = crr_put_price(70, 100, 1.0, 0.05, 0.25, 300, american=True)
    assert price >= 30
