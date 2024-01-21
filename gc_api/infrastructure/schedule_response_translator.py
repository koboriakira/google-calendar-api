from datetime import timedelta
from datetime import datetime as DateTime
from datetime import date as Date
from datetime import time as Time
from infrastructure.schedule_response import ScheduleResponse
from infrastructure.description_translator import DescriptionTranslator

CATEGORY_ACHIVEMENT = "実績"

class ScheduleResponseTranslator:
    def __init__(self, filter_achievement_enabled: bool):
        self.filter_achievement_enabled = filter_achievement_enabled

    def convert(self, data: list[dict], start_date: Date, end_date: Date) -> list[ScheduleResponse]:
        # 「予定」をとるのか「実績」をとるのかを判別する
        filtered_data = self._filter_achivement(data)

        # 日時のバリデーション
        start_datetime = DateTime.combine(start_date, Time(0, 0, 0))
        end_datetime = DateTime.combine(end_date, Time(23, 59, 59))
        filtered_data = self._filter_valid_datetime_range(filtered_data, start_datetime, end_datetime)

        # 変換
        return [self._convert_schedule(schedule) for schedule in filtered_data]


    def _convert_schedule(self, schedule: dict) -> ScheduleResponse:
        start = DateTime.fromisoformat(schedule["start"]) + timedelta(hours=9)
        end = DateTime.fromisoformat(schedule["end"]) + timedelta(hours=9)
        description = DescriptionTranslator.translate(schedule)
        return ScheduleResponse(
            category=schedule["category"],
            start=start.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
            end=end.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
            title=schedule["title"],
            description=description
        )

    def _filter_achivement(self, data: list[dict]) -> list[dict]:
        if self.filter_achievement_enabled:
            return [schedule for schedule in data if schedule["category"] == CATEGORY_ACHIVEMENT]
        else:
            return [schedule for schedule in data if schedule["category"] != CATEGORY_ACHIVEMENT]

    def _filter_valid_datetime_range(self, data: list[dict], start_datetime: DateTime, end_datetime: DateTime) -> list[dict]:
        result = []
        for schedule in data:
            # 日時のバリデーション
            start = DateTime.fromisoformat(schedule["start"]) + timedelta(hours=9)
            end = DateTime.fromisoformat(schedule["end"]) + timedelta(hours=9)
            if not (start_datetime.timestamp() <= start.timestamp() and end.timestamp() <= end_datetime.timestamp()):
                continue
            result.append(schedule)
        return result
