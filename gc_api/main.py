from mangum import Mangum
from fastapi import FastAPI, Header, HTTPException
import os
from datetime import date as DateObject
from datetime import datetime as DateTime
from datetime import timedelta
from typing import Optional
from custom_logger import get_logger
from infrastructure.gas_api import GasApi
from infrastructure.schedule_response import ScheduleResponse
from infrastructure.post_schedule_request import PostScheduleRequest
from usecase.find_schedules import FindSchedulesUsecase
from util.environment import Environment


logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

GAS_DEPLOY_ID = os.environ.get("GAS_DEPLOY_ID")

gas_api = GasApi()

def valid_authorization(access_token: Optional[str]) -> None:
    # GASのデプロイIDを使って、アクセストークンを検証する
    if access_token is None:
        raise HTTPException(status_code=401, detail="access_token is None")
    right_access_token = f"Bearer {GAS_DEPLOY_ID}"
    if access_token != right_access_token:
        raise HTTPException(status_code=401, detail="invalid access_token: " + access_token)


app = FastAPI(
    title="My Google Calendar API",
    version="0.0.1",
)

@app.get("/list", response_model=list[ScheduleResponse])
def get_calendar(start_date: DateObject = DateObject.today(),
                 end_date: DateObject = DateObject.today(),
                 achievement: Optional[bool] = False,
                 access_token: Optional[str] = Header(None)):
    """
    指定した期間のカレンダーを取得する
    """
    logger.info(f"get_calendar: {start_date} - {end_date} achievement: {achievement}")
    Environment.validate_access_token(access_token)
    return gas_api.get(start_date, end_date, achievement)

@app.get("/schedules", response_model=list[ScheduleResponse])
def find_schedules(start_datetime: DateTime = DateTime.now(),
                 end_datetime: DateTime = DateTime.now() + timedelta(minutes=5),
                 access_token: Optional[str] = Header(None)):
    """
    指定した時間帯のスケジュールを取得する
    """
    Environment.validate_access_token(access_token)
    usecase = FindSchedulesUsecase()
    result = usecase.execute(start_datetime, end_datetime)
    return result

@app.get("/next_schedules", response_model=list[ScheduleResponse])
def find_next_schedules(access_token: Optional[str] = Header(None)):
    """
    現時刻から5分後までのスケジュールを取得する
    """
    Environment.validate_access_token(access_token)
    usecase = FindSchedulesUsecase()
    start_datetime = DateTime.now() + timedelta(hours=9),
    end_datetime = start_datetime + timedelta(minutes=5),
    result = usecase.execute(start_datetime, end_datetime)
    return result


@app.post("/schedule")
def post_schedule(request: PostScheduleRequest,
                  access_token: Optional[str] = Header(None)):
    logger.info(f"post_schedule: {request}")
    Environment.validate_access_token(access_token)
    data = {
        "category": request.category,
        "startTime": request.start.isoformat(),
        "endTime": request.end.isoformat(),
        "title": request.title,
        "description": request.detail,
    }
    return gas_api.post_schedule(data)




@app.get("/healthcheck")
def hello():
    logger.info("healthcheck")
    logger.debug("healthcheck")
    return {
        'status': 'ok',
    }


handler = Mangum(app, lifespan="off")
