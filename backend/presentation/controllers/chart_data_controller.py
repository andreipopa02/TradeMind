from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import DatabaseError
from database import get_db

from business.bal.chart_data_bal_service import ChartDataBAL
from business.bao.services.chart_data_bao_service import ChartDataBAOService
from presentation.pao.services.chart_data_pao_service import ChartDataPAOService
from presentation.pal.chart_data_pal import ChartDataPAL

router = APIRouter()

db = next(get_db())
chart_bao = ChartDataBAOService()
chart_bal = ChartDataBAL(chart_bao)
chart_pao = ChartDataPAOService(chart_bal)
chart_pal = ChartDataPAL(chart_pao)

@router.post("/api/trademind/chart-data")
def get_chart_data(payload: dict):
    try:
        return chart_pal.get_chart_data(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Database error while retrieving chart data.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
