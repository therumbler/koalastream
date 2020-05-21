"""Koala Stream FastAPI web service"""
import logging
import os

from fastapi import FastAPI, Response

logger = logging.getLogger(__name__)

KS_STREAM_KEY = os.environ["KS_STREAM_KEY"]


def make_api():
    """create a FastAPI app"""

    api = FastAPI()

    @api.get("/")
    async def index():
        return {"hello": "world"}

    @api.get("/token")
    async def token(
        response: Response,
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
        if name == KS_STREAM_KEY:
            logger.debug('valid stream key')
            return {"sucess": True}

        logger.error('invalid stream key %s', KS_STREAM_KEY)
        response.status_code = 403
        return {"success": False}


    return api
