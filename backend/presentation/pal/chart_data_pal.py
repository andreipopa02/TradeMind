from typing import Dict
from presentation.pao.interfaces.chart_data_pao_interface import ChartDataPAOInterface

class ChartDataPAL:
    def __init__(self, chart_data_pao: ChartDataPAOInterface):
        self.chart_data_pao = chart_data_pao

    def get_chart_data(self, data: Dict) -> Dict:
        return self.chart_data_pao.get_chart_data(data)
