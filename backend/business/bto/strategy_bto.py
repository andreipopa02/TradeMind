from typing import Optional, Dict
from datetime import datetime
from persistence.entities.utils_entity import StrategyType


class StrategyBTO:
    def __init__(self,
                 id: Optional[int],
                 name: str,
                 type: StrategyType,
                 description: Optional[str] = None,
                 parameters: Optional[Dict] = None,
                 is_public: Optional[bool] = True,
                 created_by: Optional[int] = None,
                 created_at: Optional[datetime] = None
                 ):
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.parameters = parameters
        self.is_public = is_public
        self.created_by = created_by
        self.created_at = created_at
