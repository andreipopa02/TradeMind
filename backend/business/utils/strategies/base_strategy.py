from typing import List, Dict

class BaseStrategy:
    def generate_trades(self, candles: List[Dict], parameters: Dict) -> List[Dict]:
        pass
