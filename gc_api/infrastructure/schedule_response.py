from pydantic import BaseModel, Field
from typing import Optional

class ScheduleResponse(BaseModel):
    category: str = Field(description="Category of the schedule")
    start: str = Field(description="Start datetime of the schedule", regex=r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:\d{2}")
    end: str = Field(description="End datetime of the schedule", regex=r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+\d{2}:\d{2}")
    title: list[str] = Field(description="Title of the schedule")
    detail: Optional[dict] = Field(description="Detail of the schedule")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, __value: 'ScheduleResponse') -> bool:
        return self.title == __value.title and self.start == __value.start and self.end == __value.end
