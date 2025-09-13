from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class HeadAndShouldersStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        trades = []
        for i in range(2, len(candles) - 2):
            l_shoulder = candles[i - 2]['high']
            head = candles[i]['high']
            r_shoulder = candles[i + 2]['high']

            if l_shoulder < head and r_shoulder < head and abs(l_shoulder - r_shoulder) < (head * 0.01):
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": candles[i + 2]['time'],
                    "price": candles[i + 2]['close'],
                    "profit": 0
                })
        return trades