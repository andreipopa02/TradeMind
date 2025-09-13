from fastapi import  HTTPException, APIRouter, Depends

from business.bal.trading_account_bal import TradingAccountBAL
from business.bao.services.trading_account_bao_service import TradingAccountBAOService
from persistence.dal.trading_account_dal import TradingAccountDAL
from presentation.pal.trading_account_pal import TradingAccountPAL
from presentation.pao.services.trading_account_pao_service import TradingAccountPAOService
from configurations.jws_authentification import get_current_user

from database import get_db


router = APIRouter()

db = next(get_db())
account_dal = TradingAccountDAL(db)
account_bao = TradingAccountBAOService(account_dal)
account_bal = TradingAccountBAL(account_bao)
account_pao = TradingAccountPAOService(account_bal)
account_pal = TradingAccountPAL(account_pao)


# Create & Delete
@router.post("/api/trademind/trading_accounts/add_account")
def register_trading_account(account_data: dict):
    try:
        # account_data["user_id"] = current_user["user_id"]
        new_account = account_pal.register_trading_account(account_data)
        if not new_account:
            raise HTTPException(status_code=400, detail="Failed to create trading account. ")
        return new_account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/trademind/trading_accounts/delete_account/{account_id}")
def delete_trading_account(account_id: int, current_user: dict = Depends(get_current_user)):
    try:
        account = account_pal.get_credentials_by_id(account_id)

        if not account or account.user_id != current_user["user_id"]:
            raise HTTPException(status_code=400, detail="Failed to find this trading account. ")
        return account_pal.delete_trading_account(account_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Getters
@router.get("/api/trademind/trading_accounts/{account_id}/get_account_info")
def get_account_info_by_id(account_id: int, current_user: dict = Depends(get_current_user)):
    account_bto = account_pal.get_credentials_by_id(account_id)
    account = account_pal.get_account_info_by_id(account_id)
    if not account or account_bto.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this account.")
    return account


@router.get("/api/trademind/trading_accounts/{account_id}/get_account_info/reload")
def reload_account_info_by_id(account_id: int, current_user: dict = Depends(get_current_user)):
    account_bto = account_pal.get_credentials_by_id(account_id)
    account = account_pal.get_account_info_by_id(account_id, force_reload=True)
    if not account or account_bto.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to reload this account.")
    return account


@router.get("/api/trademind/trading_accounts/{account_id}/trade_history")
def get_trade_history(account_id: int, current_user: dict = Depends(get_current_user)):
    try:
        account_bto = account_pal.get_credentials_by_id(account_id)
        trade_history = account_pal.get_trade_history_by_id(account_id)
        if not trade_history or account_bto.user_id != current_user["user_id"]:
            raise HTTPException(status_code=404, detail="No trade history found for this account.")
        return trade_history
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/trading_accounts/{account_id}/active_trades")
def get_active_trades(account_id: int, current_user: dict = Depends(get_current_user)):
    try:
        account_bto = account_pal.get_credentials_by_id(account_id)
        active_trades = account_pal.get_active_trades_by_id(account_id)
        if not active_trades or account_bto.user_id != current_user["user_id"]:
            raise HTTPException(status_code=404, detail="No active trades found for this account.")
        return active_trades
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/trading_accounts/{account_id}/performance")
def get_account_performance(account_id: int, current_user: dict = Depends(get_current_user)):
    try:
        account_bto = account_pal.get_credentials_by_id(account_id)
        performance_data = account_pal.get_account_performance(account_id)
        if not performance_data or account_bto.user_id != current_user["user_id"]:
            raise HTTPException(status_code=404, detail="No performance data found for this account.")
        return performance_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/trading_accounts/{account_id}/stats")
def get_account_stats(account_id: int, current_user: dict = Depends(get_current_user)):
    try:
        account_bto = account_pal.get_credentials_by_id(account_id)
        stats = account_pal.get_account_stats(account_id)
        if not stats or account_bto.user_id != current_user["user_id"]:
            raise HTTPException(status_code=404, detail="No statistics found for this account.")
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/trading_accounts/{account_id}/trading_journal")
def get_account_trading_journal(account_id: int, current_user: dict = Depends(get_current_user)):
    try:
        account_bto = account_pal.get_credentials_by_id(account_id)
        journal = account_pal.get_trade_history_by_id(account_id)
        if not journal or account_bto.user_id != current_user["user_id"]:
            raise HTTPException(status_code=404, detail="No trading journal found for this account.")
        return journal
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/trademind/trading_accounts/{account_id}/credentials")
def get_credentials(account_id: int, current_user: dict = Depends(get_current_user)):
    account = account_pal.get_credentials_by_id(account_id)
    if not account or account.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view credentials.")
    return account



@router.get("/api/trademind/trading_accounts/brroker/{broker_name}")
def get_accounts_by_broker(broker_name: str, current_user: dict = Depends(get_current_user)):
    all_accounts = account_pal.get_accounts_by_broker(broker_name)
    user_accounts = [acc for acc in all_accounts if acc.user_id == current_user["user_id"]]
    return user_accounts


# Get all accounts
@router.get("/api/trademind/trading_accounts/accounts/{user_id}")
def get_user_accounts(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these accounts.")
    accounts = account_pal.get_trading_accounts(user_id)
    if not accounts:
        raise HTTPException(status_code=404, detail="No trading accounts found for this user.")
    return accounts