from typing import Optional, Dict
from pydantic import BaseModel
from datetime import datetime


class StatisticDTO(BaseModel):
    id:         Optional[int]
    user_id:    int

    name:       str
    params:     Optional[Dict]
    is_active:  Optional[bool] = True

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
