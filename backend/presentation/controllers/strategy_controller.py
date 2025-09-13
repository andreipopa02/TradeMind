from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, DatabaseError
from business.bal.strategy_bal import StrategyBAL
from business.bao.services.strategy_bao_service import StrategyBAOService
from configurations.jws_authentification import get_current_user
from persistence.dal.strategy_dal import StrategyDAL
from presentation.pao.services.strategy_pao_service import StrategyPAOService
from presentation.pal.strategy_pal import StrategyPAL
from database import get_db

router = APIRouter()

db = next(get_db())
strategy_dal = StrategyDAL(db)
strategy_bao = StrategyBAOService(db, strategy_dal)
strategy_bal = StrategyBAL(strategy_bao)
strategy_pao = StrategyPAOService(strategy_bal)
strategy_pal = StrategyPAL(strategy_pao)


@router.post("/api/trademind/strategies/create")
def create_strategy(strategy_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        strategy_data["user_id"] = current_user["user_id"]
        return strategy_pal.create_strategy(strategy_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Database constraint violation.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/strategies/strategy/{strategy_id}")
def get_strategy_by_id(strategy_id: int, current_user: dict = Depends(get_current_user)):
    try:
        strategy = strategy_pal.get_strategy_by_id(strategy_id)
        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found.")
        return strategy
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/strategies/user/{user_id}")
def get_strategies_by_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these strategies.")
    try:
        return strategy_pal.get_strategies_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/strategies/public")
def get_public_strategies():
    try:
        return strategy_pal.get_public_strategies()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/strategies/public/by-type/{strategy_type}")
def get_public_strategy_by_type(strategy_type: str):
    try:
        strategy = strategy_pal.get_public_strategy_by_type(strategy_type)
        if not strategy:
            raise HTTPException(status_code=404, detail="Public strategy not found.")
        return strategy
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))



@router.put("/api/trademind/strategies/update/{strategy_id}")
def update_strategy(strategy_id: int, strategy_data: dict):
    try:
        updated = strategy_pal.update_strategy(strategy_id, strategy_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Strategy not found.")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.delete("/api/trademind/strategies/{strategy_id}")
def delete_strategy(strategy_id: int):
    try:
        success = strategy_pal.delete_strategy(strategy_id)
        if not success:
            raise HTTPException(status_code=404, detail="Strategy not found.")
        return {"message": "Strategy deleted successfully"}
    except HTTPException as e:
        raise e
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Database error while deleting strategy.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
