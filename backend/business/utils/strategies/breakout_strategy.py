from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class BreakoutStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        window = parameters.get("window", 20)
        trades = []
        for i in range(window, len(candles)):
            highs = [c['high'] for c in candles[i - window:i]]
            lows = [c['low'] for c in candles[i - window:i]]
            high = max(highs)
            low = min(lows)
            price = candles[i]['close']

            if price > high:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": candles[i]['time'],
                    "price": price,
                    "profit": 0
                })
            elif price < low:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": candles[i]['time'],
                    "price": price,
                    "profit": 0
                })

        return trades