from typing import Dict
from business.bao.interfaces.chart_data_bao_interface import ChartDataBAOInterface
from business.utils.chart_data_loader import UniversalDataLoader

class ChartDataBAOService(ChartDataBAOInterface):
    def get_chart_data(self, data: Dict) -> Dict:
        symbol = data["symbol"]
        interval = data["time_frame"]
        start = data["start_date"]
        end = data["end_date"]

        loader, mapped_symbol = UniversalDataLoader.get_loader_and_symbol(symbol)
        _, candles = loader.get_historical_data(symbol=mapped_symbol, interval=interval, start=start, end=end)

        return {"candles": candles}
