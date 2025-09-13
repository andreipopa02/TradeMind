from typing import List, Dict

from business.utils.strategies.base_strategy import BaseStrategy


class InsideBarStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        trades = []
        for i in range(1, len(candles)):
            prev = candles[i - 1]
            curr = candles[i]

            if curr['high'] < prev['high'] and curr['low'] > prev['low']:
                direction = "BUY" if curr['close'] > curr['open'] else "SELL"
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": direction,
                    "timestamp": curr['time'],
                    "price": curr['close'],
                    "profit": 0
                })
        return trades