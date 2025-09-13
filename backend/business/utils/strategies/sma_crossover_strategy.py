from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class SMACrossoverStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        short_period = parameters.get("short_period", 5)
        long_period = parameters.get("long_period", 20)

        closes = [c['close'] for c in candles]
        trades = []
        position = None

        for i in range(len(candles)):
            if i < long_period:
                continue
            short_sma = sum(closes[i - short_period:i]) / short_period
            long_sma = sum(closes[i - long_period:i]) / long_period

            if i == 0:
                continue

            prev_short_sma = sum(closes[i - short_period - 1:i - 1]) / short_period
            prev_long_sma = sum(closes[i - long_period - 1:i - 1]) / long_period

            # Crossover signals
            if prev_short_sma < prev_long_sma and short_sma > long_sma:
                if position != "long":
                    trades.append({
                        "trade_id": len(trades) + 1,
                        "action": "BUY",
                        "timestamp": candles[i]['time'],
                        "price": candles[i]['close'],
                        "profit": 0
                    })
                    position = "long"
            elif prev_short_sma > prev_long_sma and short_sma < long_sma:
                if position != "short":
                    trades.append({
                        "trade_id": len(trades) + 1,
                        "action": "SELL",
                        "timestamp": candles[i]['time'],
                        "price": candles[i]['close'],
                        "profit": 0
                    })
                    position = "short"

        return trades
