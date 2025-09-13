from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, DatabaseError

from configurations.jws_authentification import get_current_user
from database import get_db

from business.bal.statistic_bal import StatisticBAL
from business.bao.services.statistic_bao_service import StatisticBAOService
from persistence.dal.statistic_dal import StatisticDAL
from presentation.pao.services.statistic_pao_service import StatisticPAOService
from presentation.pal.statistic_pal import StatisticPAL


router = APIRouter()


db = next(get_db())
statistic_dal = StatisticDAL(db)
statistic_bao = StatisticBAOService(db, statistic_dal)
statistic_bal = StatisticBAL(statistic_bao)
statistic_pao = StatisticPAOService(statistic_bal)
statistic_pal = StatisticPAL(statistic_pao)


@router.post("/api/trademind/statistics/create")
def create_statistic(statistic_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        # statistic_data["user_id"] = current_user["user_id"]
        return statistic_pal.create_statistic(statistic_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Database constraint violation.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/statistics/{statistic_id}")
def get_statistic_by_id(statistic_id: int, current_user: dict = Depends(get_current_user)):
    try:
        statistic = statistic_pal.get_statistic_by_id(statistic_id)
        if not statistic:
            raise HTTPException(status_code=404, detail="Statistic not found.")
        return statistic
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/api/trademind/statistics/user/{user_id}")
def get_statistics_by_user(user_id: int, current_user: dict = Depends(get_current_user)):
    # if current_user["user_id"] != user_id:
    #     raise HTTPException(status_code=403, detail="Not authorized to view these statistics.")
    try:
        stats = statistic_pal.get_statistics_by_user(user_id)
        if not stats:
            raise HTTPException(status_code=404, detail="No statistics found for this user.")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.put("/api/trademind/statistics/update/{statistic_id}")
def update_statistic(statistic_id: int, statistic_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        stat = statistic_pal.get_statistic_by_id(statistic_id)
        if not stat:
            raise HTTPException(status_code=404, detail="Statistic not found.")
        if stat["user_id"] != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="Not authorized to update this statistic.")

        statistic_data["user_id"] = current_user["user_id"]
        return statistic_pal.update_statistic(statistic_id, statistic_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.delete("/api/trademind/statistics/{statistic_id}")
def delete_statistic(statistic_id: int, current_user: dict = Depends(get_current_user)):
    try:
        stat = statistic_pal.get_statistic_by_id(statistic_id)
        if not stat:
            raise HTTPException(status_code=404, detail="Statistic not found.")
        if stat["user_id"] != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="Not authorized to delete this statistic.")

        success = statistic_pal.delete_statistic(statistic_id)
        return {"message": "Statistic deleted successfully"}
    except HTTPException as e:
        raise e
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Database error while deleting statistic.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.post("/api/trademind/statistics/generate")
def generate_statistic(statistic_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        # statistic_data["user_id"] = current_user["user_id"]
        return statistic_pal.generate_statistics(statistic_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


