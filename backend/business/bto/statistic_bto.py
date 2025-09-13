from typing import Optional, Dict
from datetime import datetime

class StatisticBTO:
    def __init__(self,
                 id: Optional[int],
                 user_id: int,

                 name: str,
                 params: Optional[Dict] = None,
                 is_active: Optional[bool] = True,

                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None
                 ):
        self.id = id
        self.user_id = user_id

        self.name = name
        self.params = params
        self.is_active = is_active

        self.created_at = created_at
        self.updated_at = updated_at
