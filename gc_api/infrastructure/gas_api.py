from datetime import date as DateObject
from datetime import timedelta
from typing import Optional
import requests
import os
import json
from infrastructure.schedule_response_translator import ScheduleResponseTranslator
import logging

GAS_DEPLOY_ID = os.environ.get("GAS_DEPLOY_ID")
GAS_CALENDAR_API_URI = f"https://script.google.com/macros/s/{GAS_DEPLOY_ID}/exec"


class GasApi:
    def get(self, start_date: DateObject, end_date: DateObject, achievement: Optional[bool] = False):
        # UTC+00:00で検索してしまうため、ちょっと広めに検索して、あとで絞る
        replaced_start_date = start_date - timedelta(days=1)
        url = f"{GAS_CALENDAR_API_URI}?startDate={replaced_start_date}&endDate={end_date}"
        response = requests.get(url)

        # \xa0が入っているので、置換する
        data = json.loads(response.text.replace("\xa0", " "))
        translator = ScheduleResponseTranslator(achievement)
        return translator.convert(data, start_date, end_date)

    def post_schedule(self, data: dict):
        response = requests.post(GAS_CALENDAR_API_URI, json=data)
        logging.info(response.status_code)
        return response.text
