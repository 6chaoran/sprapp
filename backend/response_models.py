from pydantic import BaseModel
from typing import Union, Any

class CRUDStatus(BaseModel):
    status: str

class AddStatus(BaseModel):
    status: str
    id: str

class UserExist(BaseModel):
    username: str
    exist: bool

class PRRecord(BaseModel):
    id: str
    username: str
    email: Union[str, None]
    description: str
    description_en: Union[str, None] = ''
    status: str
    applied_date: Any
    closed_date: Any
    update_ts: Any
    duration: int

class MatchedPRRecord(PRRecord):
    distance: float
    
class Matches(BaseModel):
    matches: list[MatchedPRRecord]
    odds: float
    pred_decision: str
    pred_duration: float
