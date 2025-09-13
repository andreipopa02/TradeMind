from fastapi import HTTPException, APIRouter, Query, Depends
from sqlalchemy.exc import IntegrityError, DatabaseError

from business.bal.trade_bal import TradeBAL
from business.bao.services.trade_bao_service import TradeBAOService
from configurations.jws_authentification import get_current_user
from persistence.dal.trade_dal import TradeDAL
from persistence.entities.utils_entity import SourceType
from presentation.pal.trade_pal import TradePAL
from presentation.pao.services.trade_pao_service import TradePAOService
from database import get_db

router = APIRouter()

db = next(get_db())
trade_dal = TradeDAL(db)
trade_bao = TradeBAOService(trade_dal)
trade_bal = TradeBAL(trade_bao)
trade_pao = TradePAOService(trade_bal)
trade_pal = TradePAL(trade_pao)


@router.post("/api/trademind/trades/add_trade")
def add_trade(trade_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        trade_data["user_id"] = current_user["user_id"]
        return trade_pal.add_trade(trade_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Database constraint violation.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.put("/api/trademind/trades/update_trade/{trade_id}")
def update_trade(trade_id: int, trade_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        trade_data["user_id"] = current_user["user_id"]
        updated_trade = trade_pal.update_trade(trade_id, trade_data)
        if not updated_trade:
            raise HTTPException(status_code=404, detail="Trade not found.")
        return updated_trade
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.delete("/api/trademind/trades/{trade_id}")
def delete_trade(trade_id: int, current_user: dict = Depends(get_current_user)):
    try:
        success = trade_pal.delete_trade(trade_id)
        if not success:
            raise HTTPException(status_code=404, detail="Trade not found.")
        return {"message": "Trade deleted successfully"}
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Database error while deleting trade.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/trades/user/{user_id}")
def get_trades_by_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these trades.")

    try:
        trades = trade_pal.get_trades_by_user(user_id)
        if not trades:
            raise HTTPException(status_code=404, detail="No trades found for this user.")
        return trades
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/api/trademind/trades/backtest/{backtest_id}")
def get_trades_by_backtest(backtest_id: int, current_user: dict = Depends(get_current_user)):
    try:
        trades = trade_pal.get_trades_by_backtest(backtest_id)
        if not trades:
            raise HTTPException(status_code=404, detail="No trades found for this backtest.")
        return trades
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/api/trademind/trades/user/{user_id}/filter")
def filter_trades(user_id: int, filters: dict, current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to filter these trades.")

    try:
        trades = trade_pal.get_trades_by_field(user_id, SourceType.USER, **filters)

        if not trades:
            raise HTTPException(status_code=404, detail="No trades found matching the filters.")

        return trades

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
