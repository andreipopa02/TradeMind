from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy


class DoubleTopBottomStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        trades = []
        for i in range(2, len(candles) - 2):
            a = candles[i - 2]['high']
            b = candles[i]['high']
            c = candles[i + 2]['high']

            # Double Top
            if abs(a - c) < (a * 0.005) and b < a:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": candles[i + 2]['time'],
                    "price": candles[i + 2]['close'],
                    "profit": 0
                })

            # Double Bottom (inverse pe low)
            a = candles[i - 2]['low']
            b = candles[i]['low']
            c = candles[i + 2]['low']

            if abs(a - c) < (a * 0.005) and b > a:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": candles[i + 2]['time'],
                    "price": candles[i + 2]['close'],
                    "profit": 0
                })
        return trades