from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from presentation.controllers.user_controller import router as user_router
from presentation.controllers.trading_account_controller import router as accounts_router
from presentation.controllers.trade_controller import router as trade_router
from presentation.controllers.statistic_controller import router as statistic_router
from presentation.controllers.backtest_controller import router as backtest_router
from presentation.controllers.strategy_controller import router as strategy_router
from presentation.controllers.chart_data_controller import router as chart_data_router

from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(accounts_router)
app.include_router(trade_router)
app.include_router(statistic_router)
app.include_router(backtest_router)
app.include_router(strategy_router)
app.include_router(chart_data_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
