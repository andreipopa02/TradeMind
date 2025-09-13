import time
from sqlalchemy.exc import OperationalError
from database import engine, Base
from persistence.entities.user_entity import UserEntity
from persistence.entities.trading_account_entity import TradingAccountEntity
from persistence.entities.trade_entity import TradeEntity
from persistence.entities.backtest_entity import BacktestEntity
from persistence.entities.strategy_entity import StrategyEntity
from persistence.entities.statistic_entity import StatisticEntity

# from persistence.entities.event_entity import EventEntity



def wait_for_db():
    retries = 5
    while retries > 0:
        try:
            with engine.connect() as conn:
                print("Database is ready.")
                return
        except OperationalError as e:
            print(f"Database not ready. Retrying... Error: {e}")
            time.sleep(5)
            retries -= 1
    print("Could not connect to the database.")

def init_db():
    wait_for_db()
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()


# init strategy table
#
# INSERT INTO strategies (name, description, type, parameters, is_public, created_by, created_at)
# VALUES
#   ('Engulfing Pattern', 'Bullish/Bearish engulfing candle strategy.', 'ENGULFING_PATTERN', '{}', true, NULL, NOW()),
#   ('Hammer & Shooting Star', 'Hammer bottom and shooting star reversal pattern.', 'HAMMER_SHOOTING_STAR', '{}', true, NULL, NOW()),
#   ('Head and Shoulders', 'Classic reversal pattern with neckline breakout.', 'HEAD_AND_SHOULDERS', '{}', true, NULL, NOW()),
#   ('Double Top / Bottom', 'Double top (bearish) and double bottom (bullish) formations.', 'DOUBLE_TOP_BOTTOM', '{}', true, NULL, NOW()),
#   ('Inside Bar Strategy', 'Inside candle with breakout direction.', 'INSIDE_BAR', '{}', true, NULL, NOW()),
#   ('SMA Crossover', 'Simple Moving Average crossover strategy.', 'SMA_CROSSOVER', '{"short_period": 10, "long_period": 50}', true, NULL, NOW()),
#   ('EMA Crossover', 'Exponential Moving Average crossover strategy.', 'EMA_CROSSOVER', '{"short_period": 10, "long_period": 50}', true, NULL, NOW()),
#   ('RSI Overbought/Oversold', 'RSI-based mean reversion entries.', 'RSI_OVERBOUGHT_OVERSOLD', '{"rsi_period": 14, "overbought": 70, "oversold": 30}', true, NULL, NOW()),
#   ('Bollinger Bands', 'Buy below lower band, sell above upper band.', 'BOLLINGER_BANDS', '{"period": 20, "deviation": 2}', true, NULL, NOW()),
#   ('Breakout Strategy', 'Breakout from price consolidation range.', 'BREAKOUT', '{"window": 20}', true, NULL, NOW()),
#   ('Donchian Channel', 'Breakout from highest high / lowest low in range.', 'DONCHIAN_CHANNEL', '{"window": 20}', true, NULL, NOW());
#
#
# init trades table
#
# INSERT INTO trades (
#     user_id, market, volume, type,
#     open_date, open_time, close_date, close_time, session,
#     open_price, close_price, sl_price, tp_price,
#     swap, commission, profit, pips, link_photo, source_type
# )
# VALUES
# -- EURUSD Trades
# (1, 'EURUSD', 2.00, 'SELL', '2025-07-08', '16:38:00', '2025-07-12', '03:37:00', 'NEW_YORK', 1.17155, 1.17199, 1.17199, 1.17100, 0.00, -6.00, -120.00, 4.40, 'https://example.com/chart.png', 'USER'),
# (1, 'EURUSD', 2.20, 'BUY',  '2025-06-24', '16:40:00', '2025-07-03', '19:32:00', 'NEW_YORK', 1.17124, 1.17200, 1.17089, 1.17199, 0.00, -6.60, 220.00, 7.60, 'https://www.tradingview.com/x/ZNdnU61F/', 'USER'),
# (1, 'EURUSD', 1.00, 'BUY',  '2025-07-01', '10:00:00', '2025-07-01', '14:45:00', 'LONDON',   1.17010, 1.17150, 1.16950, 1.17200, 0.00, -3.00, 140.00, 14.00, 'https://trading.com/chart1', 'USER'),
# (1, 'EURUSD', 1.50, 'SELL', '2025-07-02', '09:10:00', '2025-07-02', '16:00:00', 'ASIA',     1.17230, 1.17100, 1.17290, 1.17080, 0.00, -3.00, 195.00, 13.00, 'https://trading.com/chart2', 'USER'),
# (1, 'EURUSD', 2.00, 'BUY',  '2025-07-03', '15:15:00', '2025-07-03', '20:00:00', 'NEW_YORK', 1.17100, 1.17350, 1.17000, 1.17400, 0.00, -5.00, 250.00, 25.00, 'https://trading.com/chart3', 'USER'),
# (1, 'EURUSD', 1.80, 'SELL', '2025-07-04', '08:00:00', '2025-07-04', '11:30:00', 'LONDON',   1.17380, 1.17120, 1.17420, 1.17050, 0.00, -4.00, 260.00, 23.00, 'https://trading.com/chart4', 'USER'),
# (1, 'EURUSD', 1.20, 'BUY',  '2025-07-05', '11:00:00', '2025-07-05', '14:00:00', 'ASIA',     1.17110, 1.17290, 1.17000, 1.17300, 0.00, -2.50, 180.00, 18.00, 'https://trading.com/chart5', 'USER'),
# (1, 'EURUSD', 1.75, 'SELL', '2025-07-06', '10:45:00', '2025-07-06', '17:20:00', 'NEW_YORK', 1.17320, 1.17200, 1.17380, 1.17120, 0.00, -3.50, 120.00, 10.00, 'https://trading.com/chart6', 'USER'),
# (1, 'EURUSD', 1.90, 'BUY',  '2025-07-07', '13:00:00', '2025-07-07', '18:00:00', 'LONDON',   1.17180, 1.17300, 1.17120, 1.17350, 0.00, -4.00, 120.00, 10.00, 'https://trading.com/chart7', 'USER'),
# (1, 'EURUSD', 1.30, 'SELL', '2025-07-08', '14:10:00', '2025-07-08', '15:45:00', 'NEW_YORK', 1.17340, 1.17190, 1.17380, 1.17100, 0.00, -2.50, 150.00, 15.00, 'https://trading.com/chart8', 'USER'),
#
# -- GBPUSD Trades
# (1, 'GBPUSD', 2.00, 'SELL', '2025-07-09', '16:38:00', '2025-07-09', '19:37:00', 'NEW_YORK', 1.28800, 1.28600, 1.28900, 1.28400, 0.00, -6.00, 200.00, 20.00, 'https://gbp.com/chart1', 'USER'),
# (1, 'GBPUSD', 2.20, 'BUY',  '2025-07-10', '12:40:00', '2025-07-10', '17:32:00', 'LONDON',   1.28450, 1.28700, 1.28400, 1.28800, 0.00, -6.60, 250.00, 25.00, 'https://gbp.com/chart2', 'USER'),
# (1, 'GBPUSD', 1.50, 'SELL', '2025-07-11', '09:10:00', '2025-07-11', '13:00:00', 'ASIA',     1.28900, 1.28650, 1.29000, 1.28500, 0.00, -4.50, 250.00, 25.00, 'https://gbp.com/chart3', 'USER'),
# (1, 'GBPUSD', 2.00, 'BUY',  '2025-07-12', '15:15:00', '2025-07-12', '20:00:00', 'NEW_YORK', 1.28500, 1.28750, 1.28400, 1.28800, 0.00, -5.00, 250.00, 25.00, 'https://gbp.com/chart4', 'USER'),
# (1, 'GBPUSD', 1.80, 'SELL', '2025-07-13', '08:00:00', '2025-07-13', '11:30:00', 'LONDON',   1.28780, 1.28520, 1.28850, 1.28450, 0.00, -4.00, 260.00, 26.00, 'https://gbp.com/chart5', 'USER'),
# (1, 'GBPUSD', 1.20, 'BUY',  '2025-07-14', '11:00:00', '2025-07-14', '14:00:00', 'ASIA',     1.28440, 1.28620, 1.28400, 1.28700, 0.00, -2.50, 180.00, 18.00, 'https://gbp.com/chart6', 'USER'),
# (1, 'GBPUSD', 1.75, 'SELL', '2025-07-15', '10:45:00', '2025-07-15', '17:20:00', 'NEW_YORK', 1.28650, 1.28500, 1.28700, 1.28400, 0.00, -3.50, 150.00, 15.00, 'https://gbp.com/chart7', 'USER'),
# (1, 'GBPUSD', 1.90, 'BUY',  '2025-07-16', '13:00:00', '2025-07-16', '18:00:00', 'LONDON',   1.28580, 1.28710, 1.28500, 1.28800, 0.00, -4.00, 130.00, 13.00, 'https://gbp.com/chart8', 'USER'),
# (1, 'GBPUSD', 1.30, 'SELL', '2025-07-17', '14:10:00', '2025-07-17', '15:45:00', 'NEW_YORK', 1.28710, 1.28560, 1.28750, 1.28450, 0.00, -2.50, 150.00, 15.00, 'https://gbp.com/chart9', 'USER'),
# (1, 'GBPUSD', 2.00, 'BUY',  '2025-07-18', '10:20:00', '2025-07-18', '13:20:00', 'LONDON',   1.28480, 1.28720, 1.28400, 1.28800, 0.00, -5.00, 240.00, 24.00, 'https://gbp.com/chart10', 'USER');
