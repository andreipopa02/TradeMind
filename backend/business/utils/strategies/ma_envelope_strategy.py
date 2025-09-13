from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class MovingAverageEnvelopeStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        period = parameters.get("period", 20)
        percent = parameters.get("percent", 0.02)

        closes = [c['close'] for c in candles]
        trades = []

        for i in range(period, len(candles)):
            sma = sum(closes[i - period:i]) / period
            upper = sma * (1 + percent)
            lower = sma * (1 - percent)
            price = closes[i]

            if price > upper:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": candles[i]['time'],
                    "price": price,
                    "profit": 0
                })
            elif price < lower:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": candles[i]['time'],
                    "price": price,
                    "profit": 0
                })

        return trades