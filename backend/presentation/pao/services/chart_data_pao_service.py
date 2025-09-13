from typing import Dict
from business.bal.chart_data_bal_service import ChartDataBAL
from presentation.pao.interfaces.chart_data_pao_interface import ChartDataPAOInterface

class ChartDataPAOService(ChartDataPAOInterface):
    def __init__(self, bal: ChartDataBAL):
        self.bal = bal

    def get_chart_data(self, data: Dict) -> Dict:
        if "symbol" not in data or "time_frame" not in data or "start_date" not in data or "end_date" not in data:
            raise ValueError("Missing required fields: symbol, time_frame, start_date, end_date.")
        return self.bal.get_chart_data(data)
