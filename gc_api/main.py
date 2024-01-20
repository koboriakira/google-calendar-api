from mangum import Mangum
from fastapi import FastAPI, Header
from datetime import date as DateObject
from datetime import datetime as DateTimeObject
from datetime import time as TimeObject
from datetime import timedelta
from typing import Optional
import requests
import os
import json
import yaml
from custom_logger import get_logger

logger = get_logger(__name__)
logger.info("start")
logger.debug("debug: ON")

GAS_DEPLOY_ID = os.environ.get("GAS_DEPLOY_ID")
GAS_CALENDAR_API_URI = f"https://script.google.com/macros/s/{GAS_DEPLOY_ID}/exec"
CATEGORY_ACHIVEMENT = "実績"

def valid_authorization(access_token: Optional[str]) -> None:
    # GASのデプロイIDを使って、アクセストークンを検証する
    if access_token is None:
        raise Exception("access_token is None")
    right_access_token = f"Bearer {GAS_DEPLOY_ID}"
    if access_token != right_access_token:
        raise Exception("invalid access_token: " + access_token)


app = FastAPI(
    title="Example Test API",
    description="Describe API documentation to be served; types come from "
    "pydantic, routes from the decorators, and docs from the fastapi internal",
    version="0.0.1",
)

@app.get("/hello")
def hello():
    """
    Return a greeting
    """
    logger.info("hello")
    return {
        'status': 'ok',
    }

@app.get("/list", response_model=list[dict])
def get_calendar(start_date: DateObject,
                 end_date: DateObject,
                 achievement: Optional[bool] = False,
                 access_token: Optional[str] = Header(None)):
    logger.info(f"get_calendar: {start_date} - {end_date} achievement: {achievement}")
    logger.info(f"Authorization: {access_token}")
    valid_authorization(access_token)

    # UTC+00:00で検索してしまうため、ちょっと広めに検索して、あとで絞る
    replaced_start_date = start_date - timedelta(days=1)

    url = f"{GAS_CALENDAR_API_URI}?startDate={replaced_start_date}&endDate={end_date}"
    response = requests.get(url)
    logger.info(response.text)
    # \xa0が入っているので、置換する
    data = json.loads(response.text.replace("\xa0", " "))

    def read_yaml(content: str) -> dict:
        return yaml.safe_load(content)

    def convert(data: list[dict], start_date: DateTimeObject, end_date: DateTimeObject):
        for schedule in data:
            # 「予定」をとるのか「実績」をとるのかを判別する
            if achievement:
                if schedule["category"] != CATEGORY_ACHIVEMENT:
                    continue
            else:
                if schedule["category"] == CATEGORY_ACHIVEMENT:
                    continue

            # 日時のバリデーション
            start = DateTimeObject.fromisoformat(
                schedule["start"]) + timedelta(hours=9)
            end = DateTimeObject.fromisoformat(
                schedule["end"]) + timedelta(hours=9)
            if not (start_date.timestamp() <= start.timestamp() and end.timestamp() <= end_date.timestamp()):
                continue

            # 詳細をうまくパースする
            description = schedule["description"] if "description" in schedule else ""
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

    start_date = DateTimeObject.combine(start_date, TimeObject(0, 0, 0))
    end_date = DateTimeObject.combine(end_date, TimeObject(23, 59, 59))
    return list(convert(data,
                        start_date,
                        end_date))


handler = Mangum(app, lifespan="off")
