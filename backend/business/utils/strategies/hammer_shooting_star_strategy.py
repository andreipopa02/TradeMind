from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class HammerShootingStarStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        trades = []
        for c in candles:
            body = abs(c['close'] - c['open'])
            upper_wick = c['high'] - max(c['close'], c['open'])
            lower_wick = min(c['close'], c['open']) - c['low']

            # Hammer (potential BUY)
            if lower_wick > 2 * body and upper_wick < body:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": c['time'],
                    "price": c['close'],
                    "profit": 0
                })
            # Shooting Star (potential SELL)
            elif upper_wick > 2 * body and lower_wick < body:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": c['time'],
                    "price": c['close'],
                    "profit": 0
                })
        return trades