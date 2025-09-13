from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class EngulfingPatternStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        trades = []
        for i in range(1, len(candles)):
            prev = candles[i - 1]
            curr = candles[i]

            # Bullish Engulfing
            if prev['close'] < prev['open'] and curr['close'] > curr['open'] and curr['close'] > prev['open'] and curr['open'] < prev['close']:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": curr['time'],
                    "price": curr['close'],
                    "profit": 0
                })
            # Bearish Engulfing
            elif prev['close'] > prev['open'] and curr['close'] < curr['open'] and curr['open'] > prev['close'] and curr['close'] < prev['open']:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": curr['time'],
                    "price": curr['close'],
                    "profit": 0
                })

        return trades
