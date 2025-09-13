from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy


class EMACrossoverStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        short_period = parameters.get("short_period", 5)
        long_period = parameters.get("long_period", 20)

        short_ema = []
        long_ema = []
        trades = []
        position = None

        closes = [c["close"] for c in candles]

        def calculate_ema(period: int) -> List[float]:
            ema = [None] * len(closes)
            multiplier = 2 / (period + 1)

            for i in range(period - 1, len(closes)):
                if i == period - 1:
                    sma = sum(closes[:period]) / period
                    ema[i] = sma
                else:
                    if ema[i - 1] is not None:
                        ema[i] = (closes[i] - ema[i - 1]) * multiplier + ema[i - 1]
            return ema

        short_ema = calculate_ema(short_period)
        long_ema = calculate_ema(long_period)

        for i in range(1, len(candles)):
            if (
                short_ema[i - 1] is None or long_ema[i - 1] is None or
                short_ema[i] is None or long_ema[i] is None
            ):
                continue

            current_time = candles[i]["time"]
            price = candles[i]["close"]

            # BUY crossover
            if short_ema[i - 1] < long_ema[i - 1] and short_ema[i] > long_ema[i]:
                if position != "long":
                    trades.append({
                        "trade_id": len(trades) + 1,
                        "action": "BUY",
                        "timestamp": current_time,
                        "price": price,
                        "profit": 0
                    })
                    position = "long"

            # SELL crossover
            elif short_ema[i - 1] > long_ema[i - 1] and short_ema[i] < long_ema[i]:
                if position != "short":
                    trades.append({
                        "trade_id": len(trades) + 1,
                        "action": "SELL",
                        "timestamp": current_time,
                        "price": price,
                        "profit": 0
                    })
                    position = "short"

        return trades
