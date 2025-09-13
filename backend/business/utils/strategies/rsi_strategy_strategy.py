from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        period = parameters.get("period", 14)
        overbought = parameters.get("overbought", 70)
        oversold = parameters.get("oversold", 30)

        trades = []
        gains = []
        losses = []

        for i in range(1, len(candles)):
            delta = candles[i]['close'] - candles[i - 1]['close']
            gains.append(max(delta, 0))
            losses.append(abs(min(delta, 0)))

            if i < period:
                continue

            avg_gain = sum(gains[i - period:i]) / period
            avg_loss = sum(losses[i - period:i]) / period
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))

            if rsi > overbought:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "SELL",
                    "timestamp": candles[i]['time'],
                    "price": candles[i]['close'],
                    "profit": 0
                })
            elif rsi < oversold:
                trades.append({
                    "trade_id": len(trades) + 1,
                    "action": "BUY",
                    "timestamp": candles[i]['time'],
                    "price": candles[i]['close'],
                    "profit": 0
                })

        return trades