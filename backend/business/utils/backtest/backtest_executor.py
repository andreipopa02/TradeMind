import math
import pandas as pd
from typing import List, Dict
from ta.volatility import AverageTrueRange

from business.utils.backtest.sl_calculator import get_dynamic_sl
from persistence.entities.utils_entity import TradeType


def map_action_to_trade_type(action: str) -> TradeType:
    action = action.lower()
    for member in TradeType:
        if member.value == action:
            return member

    return TradeType.UNKNOWN

class BacktestExecutor:
    def __init__(self, initial_balance: float, risk_per_trade: float, risk_reward_ratio: float):
        self.initial_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.risk_reward_ratio = risk_reward_ratio

        self.equity = initial_balance
        self.equity_curve = [initial_balance]

        self.total_profit = 0.0
        self.wins = 0
        self.losses = 0
        self.profit_sum = 0.0
        self.loss_sum = 0.0
        self.nr_trades = 0
        self.timeframe = None

    def simulate_trades(self, signals: List[Dict], candles: List[Dict], timeframe: str, symbol: str) -> Dict:
        executed_trades = []
        self.timeframe = timeframe

        position = None
        entry_price, entry_index = None, None
        sl_price, tp_price = None, None

        signal_pointer = 0
        current_signal = signals[signal_pointer] if signals else None

        for i in range(len(candles)):
            candle_time = candles[i]["time"]

            if position is not None:
                hit_tp, hit_sl = self._check_exit_conditions(candles, entry_index, i, sl_price, tp_price, position)
                if hit_tp or hit_sl:
                    exit_price = candles[i]["close"]
                    exit_action = "SELL" if position == "BUY" else "BUY"
                    profit = self._calculate_profit(exit_price, entry_price, sl_price, tp_price, hit_tp, hit_sl, position)

                    executed_trades.append(
                        self._record_trade(
                            candles, entry_index, i,
                            entry_action=position,
                            exit_action=exit_action,
                            entry_price=entry_price,
                            exit_price=exit_price,
                            sl_price=sl_price,
                            tp_price=tp_price,
                            profit=profit,
                        )
                    )

                    self._update_metrics(profit)
                    position = entry_price = entry_index = sl_price = tp_price = None

            if current_signal and candle_time >= current_signal["timestamp"]:
                action = current_signal["action"]
                price = current_signal["price"]

                if position is None:
                    position, entry_price, entry_index, sl_price, tp_price = (
                        self._enter_position(action, price, i, candles, symbol)
                    )

                elif position != action:
                    exit_price = price
                    hit_tp, hit_sl = self._check_exit_conditions(candles, entry_index, i, sl_price, tp_price, position)
                    profit = self._calculate_profit(exit_price, entry_price, sl_price, tp_price, hit_tp, hit_sl, position)
                    exit_action = "SELL" if position == "BUY" else "BUY"

                    executed_trades.append(
                        self._record_trade(
                            candles, entry_index, i,
                            entry_action=position,
                            exit_action=exit_action,
                            entry_price=entry_price,
                            exit_price=exit_price,
                            sl_price=sl_price,
                            tp_price=tp_price,
                            profit=profit,
                        )
                    )

                    self._update_metrics(profit)

                    position, entry_price, entry_index, sl_price, tp_price = (
                        self._enter_position(action, price, i, candles, symbol)
                    )

                signal_pointer += 1
                current_signal = signals[signal_pointer] if signal_pointer < len(signals) else None

        if position is not None:
            exit_index = len(candles) - 1
            exit_price = candles[exit_index]["close"]
            hit_tp, hit_sl = self._check_exit_conditions(candles, entry_index, exit_index, sl_price, tp_price, position)
            profit = self._calculate_profit(exit_price, entry_price, sl_price, tp_price, hit_tp, hit_sl, position)
            exit_action = "SELL" if position == "BUY" else "BUY"

            executed_trades.append(
                self._record_trade(
                    candles, entry_index, exit_index,
                    entry_action=position,
                    exit_action=exit_action,
                    entry_price=entry_price,
                    exit_price=exit_price,
                    sl_price=sl_price,
                    tp_price=tp_price,
                    profit=profit,
                )
            )
            self._update_metrics(profit)

        metrics = self._calculate_final_metrics()

        return {
            "metrics": metrics,
            "executed_trades": executed_trades,
        }

    def _enter_position(self, action: str, price: float, index: int, candles: List[Dict], symbol: str):
        risk_amount = self.equity * (self.risk_per_trade / 100)
        sl_distance = get_dynamic_sl(price, candles, index, symbol, action)

        tp_distance = sl_distance * self.risk_reward_ratio

        if action == "BUY":
            sl_price = price - sl_distance
            tp_price = price + tp_distance
        else:
            sl_price = price + sl_distance
            tp_price = price - tp_distance

        return action, price, index, sl_price, tp_price

    def _check_exit_conditions(
            self, candles: List[Dict], entry_index: int, current_index: int,
            sl_price: float, tp_price: float, position: str
    ):
        hit_tp, hit_sl = False, False

        for j in range(entry_index + 1, current_index + 1):
            o = candles[j]["open"]
            h = candles[j]["high"]
            l = candles[j]["low"]
            c = candles[j]["close"]

            if position == "BUY":
                if l <= sl_price and h >= tp_price:
                    if abs(o - sl_price) < abs(o - tp_price):
                        return False, True  # SL first
                    else:
                        return True, False  # TP first
                elif l <= sl_price:
                    return False, True
                elif h >= tp_price:
                    return True, False

            else:  # SELL
                if h >= sl_price and l <= tp_price:
                    if abs(o - sl_price) < abs(o - tp_price):
                        return False, True  # SL first
                    else:
                        return True, False  # TP first
                elif h >= sl_price:
                    return False, True
                elif l <= tp_price:
                    return True, False
        return hit_tp, hit_sl

    def _calculate_profit(self, exit_price: float, entry_price: float,
                          sl_price: float, tp_price: float,
                          hit_tp: bool, hit_sl: bool, position: str):
        risk_amount = self.equity * (self.risk_per_trade / 100)

        if hit_tp:
            profit = risk_amount * self.risk_reward_ratio
            return round(profit, 2)
        if hit_sl:
            return round(-risk_amount, 2)

        if position == "BUY":
            sl_distance = entry_price - sl_price
            move = exit_price - entry_price
        else:  # SELL
            sl_distance = sl_price - entry_price
            move = entry_price - exit_price

        if sl_distance <= 0:
            return 0.0

        rr_achieved = move / sl_distance
        rr_achieved = max(-1.0, min(self.risk_reward_ratio, rr_achieved))

        profit = risk_amount * rr_achieved
        return round(profit, 2)

    def _record_trade(self, candles: List[Dict], entry_index: int, exit_index: int,
                      entry_action: str, exit_action: str,
                      entry_price: float, exit_price: float,
                      sl_price: float, tp_price: float,
                      profit: float) -> Dict:
        return {
            "entry_id": entry_index,
            "exit_id": exit_index,
            "entry_action": entry_action,
            "exit_action": exit_action,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "sl_price": sl_price,
            "tp_price": tp_price,
            "profit": profit,
            "pips": abs(entry_price - exit_price),
            "open_timestamp": candles[entry_index]["time"],
            "close_timestamp": candles[exit_index]["time"]
        }

    def _update_metrics(self, profit: float):
        self.nr_trades += 1
        self.equity += profit
        self.equity_curve.append(self.equity)
        self.total_profit += profit

        if profit > 0:
            self.wins += 1
            self.profit_sum += profit
        elif profit < 0:
            self.losses += 1
            self.loss_sum += abs(profit)

    def _calculate_final_metrics(self) -> Dict:
        winrate = (self.wins / self.nr_trades * 100) if self.nr_trades else 0
        profit_factor = (self.profit_sum / self.loss_sum) if self.loss_sum else math.inf
        expectancy = (self.total_profit / self.nr_trades) if self.nr_trades else 0
        max_dd = self._calculate_max_drawdown()

        balance_curve = [{"trade": i, "balance": bal} for i, bal in enumerate(self.equity_curve)]

        return {
            "total_profit": round(self.total_profit, 2),
            "drawdown_max": round(max_dd, 2),
            "winrate": round(winrate, 2),
            "nr_trades": self.nr_trades,
            "profit_factor": round(profit_factor, 2) if profit_factor != math.inf else None,
            "expectancy": round(expectancy, 2),
            "balance_curve": balance_curve,
        }

    def _calculate_max_drawdown(self) -> float:
        peak = self.equity_curve[0]
        max_dd = 0.0
        for balance in self.equity_curve:
            if balance > peak:
                peak = balance
            drawdown = peak - balance
            max_dd = max(max_dd, drawdown)
        return max_dd

