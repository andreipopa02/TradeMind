from typing import List, Dict
from business.utils.strategies.base_strategy import BaseStrategy

class MACDCrossoverStrategy(BaseStrategy):
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        fast_period = parameters.get("fast_period", 12)
        slow_period = parameters.get("slow_period", 26)
        signal_period = parameters.get("signal_period", 9)

        closes = [c['close'] for c in candles]
        macd = []
        signal = []
        trades = []
        position = None

        for i in range(len(candles)):
            if i < slow_period:
                macd.append(None)
                signal.append(None)
                continue

            fast_ema = sum(closes[i - fast_period:i]) / fast_period
            slow_ema = sum(closes[i - slow_period:i]) / slow_period
            macd_val = fast_ema - slow_ema
            macd.append(macd_val)

            if i >= slow_period + signal_period:
                signal_val = sum(macd[i - signal_period + 1:i + 1]) / signal_period
                signal.append(signal_val)

                if macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
                    if position != "long":
                        trades.append({
                            "trade_id": len(trades) + 1,
                            "action": "BUY",
                            "timestamp": candles[i]['time'],
                            "price": candles[i]['close'],
                            "profit": 0
                        })
                        position = "long"
                elif macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:
                    if position != "short":
                        trades.append({
                            "trade_id": len(trades) + 1,
                            "action": "SELL",
                            "timestamp": candles[i]['time'],
                            "price": candles[i]['close'],
                            "profit": 0
                        })
                        position = "short"
            else:
                signal.append(None)

        return trades