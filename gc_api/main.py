from mangum import Mangum
from fastapi import FastAPI, Header
import os
from datetime import date as DateObject
from typing import Optional
from custom_logger import get_logger
from infrastructure.gas_api import GasApi
from infrastructure.schedule_response import ScheduleResponse

logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

GAS_DEPLOY_ID = os.environ.get("GAS_DEPLOY_ID")

gas_api = GasApi()

def valid_authorization(access_token: Optional[str]) -> None:
    # GASのデプロイIDを使って、アクセストークンを検証する
    if access_token is None:
        raise Exception("access_token is None")
    right_access_token = f"Bearer {GAS_DEPLOY_ID}"
    if access_token != right_access_token:
        raise Exception("invalid access_token: " + access_token)


app = FastAPI(
    title="My Google Calendar API",
    version="0.0.1",
)

@app.get("/list", response_model=list[ScheduleResponse])
def get_calendar(start_date: DateObject = DateObject.today(),
                 end_date: DateObject = DateObject.today(),
                 achievement: Optional[bool] = False,
                 access_token: Optional[str] = Header(None)):
    logger.info(f"get_calendar: {start_date} - {end_date} achievement: {achievement}")
    valid_authorization(access_token)
    return gas_api.get(start_date, end_date, achievement)


@app.get("/healthcheck")
def hello():
    logger.info("healthcheck")
    logger.debug("healthcheck")
    return {
        'status': 'ok',
    }


handler = Mangum(app, lifespan="off")
