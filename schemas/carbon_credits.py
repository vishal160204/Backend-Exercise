from pydantic import BaseModel
from typing import List

class RegisterCredit(BaseModel):
    project_name : str
    registry : str
    vintage : int
    quantity : int
    serial_number : str

class CreditEvents(BaseModel):
    id : str
    event_type : str
    timestamp : str
    class config:
        orm_mode = True


class RecordOut(BaseModel):
    id :str 
    project_name : str
    registry : str
    vintage : int 
    quantity : int
    History : List[CreditEvents]

    class config:
        orm_mode = True