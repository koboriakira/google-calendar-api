from datetime import datetime as DateTime
from datetime import date as Date
from infrastructure.gas_api import GasApi
from custom_logger import get_logger

logger = get_logger(__name__)

class FindSchedulesUsecase:
    def __init__(self):
        self.gas_api = GasApi()

    def execute(self, start_datetime: DateTime,
                 end_datetime: DateTime) -> list[dict]:
        schedules = self.gas_api.get(start_date=Date.today(), end_date=Date.today())

        result = []
        for schedule in schedules:
            logger.info(schedule)
            schedule_start_datetime = DateTime.fromisoformat(schedule.start)
            if start_datetime <= schedule_start_datetime and schedule_start_datetime <= end_datetime:
                result.append(schedule)
        return result

if __name__ == "__main__":
    # python -m usecase.find_schedules
    usecase = FindSchedulesUsecase()
    usecase.execute(start_datetime=DateTime.now(), end_datetime=DateTime.now())
