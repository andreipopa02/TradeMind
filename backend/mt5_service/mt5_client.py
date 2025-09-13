import requests

MT5_API_URL = "http://host.docker.internal:5001"

def get_account_info(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/account_info/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}

def get_active_trades(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/trades/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}

def get_trade_history(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/trade_history/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}

def get_account_performance(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/account_performance/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}

def get_account_stats(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/account_stats/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}

def get_account_trading_journal(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/account_trading_journal/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}

def check_credentials(account_id: int, password: str, server: str):
    params = {
        "password": password,
        "server": server
    }

    response = requests.get(f"{MT5_API_URL}/mt5/check_credentials/{account_id}", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}", "details": response.text}