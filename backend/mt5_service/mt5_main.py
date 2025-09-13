from datetime import datetime

from fastapi import FastAPI, HTTPException
import MetaTrader5 as mt5

app = FastAPI()


@app.get("/mt5/account_info/{account_id}")
def get_account_info(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Login failed. Check account credentials.")

        account_info = mt5.account_info()
        if account_info is None:
            raise HTTPException(status_code=404, detail="Account info not found.")

        active_positions = mt5.positions_total()

        return {
            "balance": account_info.balance,
            "equity": account_info.equity,
            "margin_free": account_info.margin_free,
            "margin_level": account_info.margin_level,
            "currency": account_info.currency,
            "active_positions": active_positions,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


@app.get("/mt5/trades/{account_id}")
def get_active_trades(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Login failed. Check account credentials.")

        trades = mt5.positions_get()
        if trades is None:
            raise HTTPException(status_code=404, detail="No active trades found.")

        return [
            {
                "ticket": trade.ticket,
                "symbol": trade.symbol,
                "volume": trade.volume,
                "price_open": trade.price_open,
                "price_sl": trade.sl,
                "price_tp": trade.tp,
                "profit": trade.profit
            }
            for trade in trades
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


@app.get("/mt5/trade_history/{account_id}")
def get_trade_history(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Login failed. Check account credentials.")

        deals = mt5.history_deals_get(datetime(2000, 1, 1), datetime.now())
        if deals is None:
            raise HTTPException(status_code=404, detail="No trade history found.")

        filtered_deals = [
            {
                "ticket": deal.ticket,
                "symbol": deal.symbol,
                "volume": deal.volume,
                "price": deal.price,
                "commission": deal.commission,
                "swap": deal.swap,
                "profit": deal.profit,
                "time": deal.time
            }
            for deal in deals if not (deal.profit == 0 and deal.commission == 0 and deal.swap == 0)
        ]

        return filtered_deals[1:]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


@app.get("/mt5/account_performance/{account_id}")
def get_account_performance(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Login failed. Check account credentials.")

        deals = mt5.history_deals_get(datetime(2025, 1, 1), datetime.now())
        if deals is None:
            raise HTTPException(status_code=404, detail="No trade history found.")

        balance_history = []
        running_balance = 0

        for deal in deals:
            running_balance += deal.profit
            balance_history.append({"date": deal.time, "balance": running_balance})

        return balance_history

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


@app.get("/mt5/account_stats/{account_id}")
def get_account_stats(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Login failed. Check account credentials.")

        deals = mt5.history_deals_get(datetime(2025, 1, 1), datetime.now())
        if deals is None:
            raise HTTPException(status_code=404, detail="No trade history found.")

        sorted_deals = sorted(mt5.orders_get(), key=lambda d: d.time)

        filtered_deals = sorted_deals[1:]
        for deal in deals[1:]:
            if not (deal.profit == 0 and deal.commission == 0 and deal.swap == 0):
                filtered_deals.append(deal)

        total_trades = len(filtered_deals)
        wins = sum(1 for deal in filtered_deals if deal.profit > 0)
        losses = total_trades - wins
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0

        avg_profit = sum(deal.profit for deal in filtered_deals if deal.profit > 0) / max(wins, 1)
        avg_loss = sum(deal.profit for deal in filtered_deals if deal.profit < 0) / max(losses, 1)
        profit_factor = abs(avg_profit / avg_loss) if avg_loss != 0 else 100

        return {
            "totalTrades": total_trades,
            "winRate": round(win_rate, 2),
            "avgProfit": round(avg_profit, 2),
            "avgLoss": round(avg_loss, 2),
            "profitFactor": round(profit_factor, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


@app.get("/mt5/account_trading_journal/{account_id}")
def get_account_trading_journal(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Login failed. Check account credentials.")

        deals = mt5.history_deals_get(datetime(2025, 1, 1), datetime.now())
        if deals is None:
            raise HTTPException(status_code=404, detail="No trade history found.")

        trade_journal = [
            {
                "date": deal.time,
                "type": "Buy" if deal.type == mt5.ORDER_TYPE_BUY else "Sell",
                "volume": deal.volume,
                "symbol": deal.symbol,
                "profit": deal.profit if deal.profit else 0.0,
                "commission": deal.commission,
                "swap": deal.swap
            }
            for deal in deals if not (deal.profit == 0 and deal.commission == 0 and deal.swap == 0)
        ]

        return trade_journal

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


@app.get("/mt5/check_credentials/{account_id}")
def check_credentials(account_id: int, password: str, server: str):
    try:
        if not mt5.initialize():
            raise HTTPException(status_code=500, detail="Failed to initialize MT5 connection")

        if not mt5.login(account_id, password, server):
            mt5.shutdown()
            raise HTTPException(status_code=401, detail="Invalid credentials. Please check your account ID, password, or server.")

        return {"message": "Credentials are valid. You may proceed."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5001)
