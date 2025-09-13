from typing import Optional
from pydantic import BaseModel


class UserDTO(BaseModel):
    id:         Optional[int]

    first_name: str
    last_name:  str
    email:      str
    password:   Optional[str]

    phone:      str
    gender:     str
    country:    str

    is_verified: bool

    class Config:
        from_attributes = True