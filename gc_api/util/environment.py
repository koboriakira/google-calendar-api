import os
from typing import Optional
from fastapi import HTTPException

GAS_DEPLOY_ID = os.environ.get("GAS_DEPLOY_ID")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

class Environment(object):
    @staticmethod
    def validate_access_token(access_token: Optional[str]) -> None:
        if Environment.is_dev():
            return
        # GASのデプロイIDを使って、アクセストークンを検証する
        if access_token is None:
            raise HTTPException(status_code=401, detail="access_token is None")
        right_access_token = f"Bearer {GAS_DEPLOY_ID}"
        if access_token != right_access_token:
            raise HTTPException(status_code=401, detail="invalid access_token: " + access_token)

    @staticmethod
    def is_dev() -> bool:
        return ENVIRONMENT == "dev"
