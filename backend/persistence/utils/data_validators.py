import re
from datetime import datetime, time
from typing import Optional

from business.bto.trade_bto import TradeBTO
from persistence.entities.utils_entity import SessionType, StrategyType


# user validators
def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")

def validate_email_format(email: str) -> None:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")

def validate_phone(phone: str) -> None:
    if not re.match(r"^\+?\d{8,15}$", phone):
        raise ValueError("Invalid phone number format")

def validate_gender(gender: str) -> None:
    if gender not in {"Male", "Female", "Other"}:
        raise ValueError("Invalid gender value")


# trading account validators

def validate_broker_name(name: str) -> None:
    if not name or len(name.strip()) < 3:
        raise ValueError("Broker name must be at least 3 characters long.")
    if not re.match(r"^[a-zA-Z\s]+$", name):
        raise ValueError("Broker name must contain only letters and spaces.")

def validate_account_id(account_id: int) -> None:
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("Account ID must be a positive integer.")
    if len(str(account_id)) < 5 or len(str(account_id)) > 15:
        raise ValueError("Account ID must be between 5 and 15 digits.")

def validate_server(server: str) -> None:
    if not server or len(server.strip()) < 3:
        raise ValueError("Server must be provided and contain at least 3 characters.")
    if not re.match(r"^[a-zA-Z0-9\-\.]+$", server):
        raise ValueError("Server contains invalid characters.")

def validate_password(password: str) -> None:
    if not password or len(password.strip()) < 6:
        raise ValueError("Password must be at least 6 characters long.")


# trade validators

def get_session_from_open_time(trade_bto: TradeBTO) -> SessionType:
    open_time = trade_bto.open_time
    if not open_time:
        return SessionType.UNKNOWN

    if isinstance(open_time, str):
        try:
            open_time = datetime.strptime(open_time, "%H:%M:%S").time()
        except ValueError:
            try:
                open_time = datetime.strptime(open_time, "%H:%M").time()
            except ValueError:
                return SessionType.UNKNOWN
    elif isinstance(open_time, time):
        open_time = open_time

    if time(0, 0) <= open_time < time(10, 0):
        return SessionType.ASIA
    elif time(10, 0) <= open_time < time(14, 0):
        return SessionType.LONDON
    elif time(14, 0) <= open_time < time(21, 0):
        return SessionType.NEW_YORK
    else:
        return SessionType.UNKNOWN

def to_time(value) -> Optional[time]:
    if isinstance(value, time):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%H:%M").time()
        except ValueError:
            return None
    return None

def is_valid_time_and_date(trade_bto: TradeBTO) -> None:
    if trade_bto.close_date:
        if trade_bto.close_date < trade_bto.open_date:
            raise ValueError("Invalid trade: close_date must be after or equal to open_date.")

        if trade_bto.close_time:
            if trade_bto.close_date == trade_bto.open_date and trade_bto.close_time <= trade_bto.open_time:
                raise ValueError("Invalid trade: on the same date, close_time must be after open_time.")
    else:
        if trade_bto.close_time:
            if trade_bto.close_time <= trade_bto.open_time:
                raise ValueError("Invalid trade: if close_date is not set, close_time must be after open_time.")

def is_valid_price(trade_bto: TradeBTO) -> None:
    if trade_bto.type == "sell":
        if trade_bto.tp_price and trade_bto.tp_price >= trade_bto.open_price:
            raise ValueError("Invalid SELL trade: Take-Profit (TP) should be < open_price.")
        if trade_bto.sl_price and trade_bto.sl_price <= trade_bto.open_price:
            raise ValueError("Invalid SELL trade: Stop-Loss (SL) should be > open_price.")

    if trade_bto.type == "buy":
        if trade_bto.tp_price and trade_bto.tp_price <= trade_bto.open_price:
            raise ValueError("Invalid BUY trade: Take-Profit (TP) should be > open_price.")
        if trade_bto.sl_price and trade_bto.sl_price >= trade_bto.open_price:
            raise ValueError("Invalid BUY trade: Stop-Loss (SL) should be < open_price.")

def calculate_pips(trade_bto: TradeBTO) -> float:
    if trade_bto.open_price is None or trade_bto.close_price is None:
        return 0.0

    price_diff = abs(trade_bto.close_price - trade_bto.open_price)
    avg_price = (trade_bto.close_price + trade_bto.open_price) / 2

    if avg_price < 10:
        return price_diff * 10000
    elif 10 <= avg_price < 1000:
        return price_diff * 100
    elif 1000 <= avg_price < 10000:
        return price_diff / 10
    else:
        return price_diff


# strategy validators

def validate_strategy_name(name: str) -> None:
    if not name or len(name.strip()) < 3:
        raise ValueError("Strategy name must be at least 3 characters long.")
    if len(name) > 50:
        raise ValueError("Strategy name must be at most 50 characters.")
    if not re.match(r"^[a-zA-Z0-9\s\-_]+$", name):
        raise ValueError("Strategy name contains invalid characters.")

def validate_strategy_description(description: str) -> None:
    if description and len(description) > 255:
        raise ValueError("Strategy description must be at most 255 characters.")

def validate_strategy_type(strategy_type: StrategyType) -> None:
    if strategy_type not in StrategyType:
        raise ValueError("Invalid strategy type.")

def validate_strategy_parameters(parameters: dict) -> None:
    if parameters is not None and not isinstance(parameters, dict):
        raise ValueError("Parameters must be a dictionary.")


# statistic validators

def validate_statistic_name(name: str) -> None:
    if not name or len(name.strip()) < 3:
        raise ValueError("Statistic name must be at least 3 characters.")
    if len(name) > 100:
        raise ValueError("Statistic name must be at most 100 characters.")
    if not re.match(r"^[a-zA-Z0-9\s\-_]+$", name):
        raise ValueError("Statistic name contains invalid characters.")

def validate_statistic_params(params: dict) -> None:
    if params is not None and not isinstance(params, dict):
        raise ValueError("Statistic parameters must be a dictionary.")