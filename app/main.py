from mangum import Mangum
from fastapi import FastAPI

APP = FastAPI(
    title="Example Test API",
    description="Describe API documentation to be served; types come from "
    "pydantic, routes from the decorators, and docs from the fastapi internal",
    version="0.0.1",
)

@APP.get("/hello")
def hello():
    """
    Return a greeting
    """
    return {
        'status': 'ok',
    }



@APP.get("/v1/items")
def list_items():
    """
    Return a collection of items
    """
    return {
        'message': 'Hello, world!'
    }


handler = Mangum(APP, lifespan="off")
