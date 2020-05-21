"""Koala Stream FastAPI web service"""
import logging
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def make_api():
    """create a FastAPI app"""

    api = FastAPI()

    @api.get("/")
    async def index():
        return {"hello": "world"}

    @api.get("/token")
    async def token(
        app: str,
        flashver: str,
        swfurl: str,
        tcurl: str,
        pageurl: str,
        addr: str,
        clientid: str,
        call: str,
        name: str,
        type: str,
    ):
        # logger.info("kwargs: %s", kwargs)
        return {"sucess": True}

    return api
