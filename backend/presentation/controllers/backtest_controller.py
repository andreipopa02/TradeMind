from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from business.bal.backtest_bal import BacktestBAL
from business.bao.services.backtest_bao_service import BacktestBAOService
from persistence.dal.backtest_dal import BacktestDAL
from presentation.pao.services.backtest_pao_service import BacktestPAOService
from presentation.pal.backtest_pal import BacktestPAL
from database import get_db

router = APIRouter()

db = next(get_db())
backtest_dal = BacktestDAL(db)
backtest_bao = BacktestBAOService(db, backtest_dal)
backtest_bal = BacktestBAL(backtest_bao)
backtest_pao = BacktestPAOService(backtest_bal)
backtest_pal = BacktestPAL(backtest_pao)

@router.post("/api/trademind/backtests/save")
def save_backtest(backtest_data: dict):
    try:
        return backtest_pal.save_backtest(backtest_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Constraint violation.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print("ERROR in save_backtest:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.post("/api/trademind/backtests/preview")
def run_backtest_preview(backtest_data: dict):
    try:
        response = backtest_pal.run_backtest_preview(backtest_data)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/trademind/backtests/{backtest_id}")
def get_backtest_by_id(backtest_id: int):
    try:
        backtest = backtest_pal.get_backtest_by_id(backtest_id)
        if not backtest:
            raise HTTPException(status_code=404, detail="Backtest not found.")
        return backtest
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/backtests/user/{user_id}")
def get_backtests_by_user(user_id: int):
    try:
        return backtest_pal.get_backtests_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.get("/api/trademind/backtests/strategy/{strategy_id}")
def get_backtests_by_strategy(strategy_id: int):
    try:
        return backtest_pal.get_backtests_by_strategy(strategy_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.delete("/api/trademind/backtests/{backtest_id}")
def delete_backtest(backtest_id: int):
    try:
        success = backtest_pal.delete_backtest(backtest_id)
        if not success:
            raise HTTPException(status_code=404, detail="Backtest not found.")
        return {"message": "Backtest deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
