from typing import Dict
from business.bao.interfaces.chart_data_bao_interface import ChartDataBAOInterface

class ChartDataBAL:
    def __init__(self, bao_service: ChartDataBAOInterface):
        self.bao_service = bao_service

    def get_chart_data(self, data: Dict) -> Dict:
        return self.bao_service.get_chart_data(data)
