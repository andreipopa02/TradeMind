import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def extract_price(value):
    try:
        return float(value.iloc[0]) if isinstance(value, pd.Series) else float(value)
    except Exception:
        return None

class YahooFinanceLoader:
    def get_historical_data(self, symbol: str,
                            interval: str = "1m",
                            start: str = None,
                            end: str = None) -> tuple[pd.DataFrame, list[dict]]:

        interval_mapping = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "60m": "60m",
            "daily": "1d"
        }

        if interval not in interval_mapping:
            raise ValueError(f"Unsupported interval '{interval}' for Yahoo Finance.")

        yf_interval = interval_mapping[interval]

        if not start or not end:
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - pd.Timedelta(days=7)).strftime('%Y-%m-%d')
        else:
            start_date = start
            end_date = end

        df = yf.download(symbol, start=start_date, end=end_date, interval=yf_interval, auto_adjust=False)

        if df.empty:
            raise ValueError(f"No data returned by Yahoo Finance for symbol: {symbol} and interval: {yf_interval}")

        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        candles = []
        for ts, row in df.iterrows():
            open_price = extract_price(row["open"])
            high_price = extract_price(row["high"])
            low_price = extract_price(row["low"])
            close_price = extract_price(row["close"])

            if None in (open_price, high_price, low_price, close_price):
                continue

            candles.append({
                "time": int(ts.timestamp()),
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price
            })

        return df, candles


class BinanceLoader:
    BASE_URL = "https://api.binance.com/api/v3/klines"

    def get_historical_data(self, symbol: str, interval: str = "1m", start: str = None, end: str = None,
                            limit: int = 1000) -> tuple[pd.DataFrame, list[dict]]:

        if not start or not end:
            end_dt = datetime.utcnow()
            start_dt = end_dt - timedelta(days=1)
        else:
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d")

        start_ts = int(start_dt.timestamp() * 1000)
        end_ts = int(end_dt.timestamp() * 1000)

        df_all = pd.DataFrame()

        while start_ts < end_ts:
            params = {
                "symbol": symbol.upper(),
                "interval": interval,
                "startTime": start_ts,
                "endTime": end_ts,
                "limit": limit
            }

            response = requests.get(self.BASE_URL, params=params)
            if response.status_code != 200:
                msg = response.json().get("msg", "")
                raise Exception(f"Binance API error: {response.status_code} - {msg}")

            data = response.json()
            if not data:
                break

            df = pd.DataFrame(data, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
            ])

            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
            df = df.set_index("open_time")
            df = df[["open", "high", "low", "close", "volume"]].astype(float)

            df_all = pd.concat([df_all, df])

            last_time = data[-1][0]
            start_ts = last_time + 1

        df_all = df_all.sort_index()

        candles = [
            {
                "time": int(ts.timestamp()),
                "open": extract_price(row["open"]),
                "high": extract_price(row["high"]),
                "low": extract_price(row["low"]),
                "close": extract_price(row["close"]),
            }
            for ts, row in df_all.iterrows()
        ]

        return df_all, candles


class UniversalDataLoader:
    SYMBOL_MAPPING = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "USDJPY=X",
        "GER40": "^GDAXI",
        "UK100": "^FTSE",
        "US100": "^NDX",
        "US30": "^DJI",
        "BTCUSDT": "BTCUSDT",
        "ETHUSDT": "ETHUSDT",
        "SOLUSDT": "SOLUSDT",
        "BNBUSDT": "BNBUSDT",
        "XRPUSDT": "XRPUSDT"
    }

    @classmethod
    def get_loader_and_symbol(cls, symbol: str):
        symbol_upper = symbol.upper()
        mapped_symbol = cls.SYMBOL_MAPPING.get(symbol_upper, symbol_upper)

        if symbol_upper in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]:
            return BinanceLoader(), mapped_symbol
        else:
            return YahooFinanceLoader(), mapped_symbol
