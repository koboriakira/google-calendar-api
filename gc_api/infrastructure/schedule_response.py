from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime as DateTime

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

    @staticmethod
    def convert(data: dict, start_datetime: DateTime, end_datetime: DateTime) -> 'ScheduleResponse':
        from datetime import timedelta
        # 日時のバリデーション
        start = DateTime.fromisoformat(data["start"]) + timedelta(hours=9)
        end = DateTime.fromisoformat(data["end"]) + timedelta(hours=9)
        if not (start_datetime.timestamp() <= start.timestamp() and end.timestamp() <= end_datetime.timestamp()):
            return None

        # 詳細をうまくパースする
        description = data["description"] if "description" in data else ""
        try:
            # <br>タグは改行に置換する
            description = description.replace("<br>", "\n")
            # そのほかのHTMLタグはすべて置換する
            # description = re.sub(r"<[^>]*?>", "", description)
            description = read_yaml(description)
        except:
            print("yaml parse error")
            print(description)
            description = None

        yield {
            "category": schedule["category"],
            "start": start.strftime("%Y-%m-%d %H:%M:%S+09:00"),
            "end": end.strftime("%Y-%m-%d %H:%M:%S+09:00"),
            "title": schedule["title"],
            "detail": description,
        }
