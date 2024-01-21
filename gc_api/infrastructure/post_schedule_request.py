from pydantic import BaseModel
from datetime import datetime as DateTime

class PostScheduleRequest(BaseModel):
    category: str
    start: DateTime
    end: DateTime
    title: str
    detail: str
