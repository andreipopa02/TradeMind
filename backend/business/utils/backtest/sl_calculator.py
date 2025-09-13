from typing import List, Dict
import math
import numpy as np
import pandas as pd
from ta.volatility import AverageTrueRange

def _pip_size(symbol: str) -> float:
    s = symbol.upper()
    # indices/metale/crypto/forex
    if s.startswith(("XAU", "GOLD")):
        return 0.1
    if s.startswith(("XAG", "SILVER")):
        return 0.01
    if s.endswith(("USDT", "USD")) and not (len(s) == 6 and s.isalpha()):
        return 0.01  # Crypto
    if s.endswith(("JPY", "JPT", "HKD")):
        return 0.01  # Asian FX pairs
    if len(s) == 6 and s.isalpha():
        return 0.0001  # standard FX pairs
    return 0.0001

def get_dynamic_sl(
    entry_price: float,
    candles: List[Dict],
    entry_index: int,
    symbol: str,
    action: str,
    ) -> float:
    if not candles or entry_index <= 0 or entry_index >= len(candles):
        return 20 * _pip_size(symbol)

    df = pd.DataFrame(candles, dtype=float)
    for col in ("high", "low", "close", "open"):
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # 1) ATR(14) * 1.5
    dist_atr = None
    try:
        atr_series = AverageTrueRange(
            high=df["high"], low=df["low"], close=df["close"], window=14
        ).average_true_range()
        atr_val = float(atr_series.iloc[entry_index])
        if math.isfinite(atr_val) and atr_val > 0:
            dist_atr = atr_val * 1.5
    except Exception:
        pass

    # 2) Price structure (swing low/high for last N candles)
    lookback = 10
    left = max(0, entry_index - lookback)
    lows = df["low"].iloc[left:entry_index]
    highs = df["high"].iloc[left:entry_index]
    dist_structure = None
    if len(lows) and len(highs):
        is_buy = (action or "").upper() == "BUY"
        if is_buy:
            dist_structure = max(0.0, entry_price - float(lows.min()))
        else:
            dist_structure = max(0.0, float(highs.max()) - entry_price)

    # 3) Fallback: percentila 75 a True Range
    dist_vol = None
    try:
        tr = (df["high"] - df["low"]).astype(float)
        W = 30
        tr_win = tr.iloc[max(0, entry_index - W + 1): entry_index + 1]
        if len(tr_win):
            p75 = float(np.nanpercentile(tr_win, 75))
            if math.isfinite(p75) and p75 > 0:
                dist_vol = p75 * 1.2
    except Exception:
        pass

    candidates = [d for d in (dist_atr, dist_structure, dist_vol) if d is not None and d > 0]
    if candidates:
        return float(max(candidates))

    return float(20 * _pip_size(symbol))
