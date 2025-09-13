from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class BollingerBandsStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        period = parameters.get("period", 20)
        deviation = parameters.get("deviation", 2)

        closes = [c['close'] for c in candles]
        trades = []

        for i in range(period, len(candles)):
            sma = sum(closes[i - period:i]) / period
            std_dev = (sum([(x - sma) ** 2 for x in closes[i - period:i]]) / period) ** 0.5

            upper_band = sma + deviation * std_dev
            lower_band = sma - deviation * std_dev
            price = candles[i]['close']

            if price < lower_band:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": candles[i]['time'],
                    "price": price,
                    "profit": 0
                })
            elif price > upper_band:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": candles[i]['time'],
                    "price": price,
                    "profit": 0
                })

        return trades