"""Koala Stream FastAPI web service"""
import asyncio
import logging
import os

import aiofiles
from fastapi import FastAPI, Response, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import HTMLResponse

from koalastream.koalastream import ffmpeg, create_local_docker, delete_local_docker
logger = logging.getLogger(__name__)

KS_STREAM_KEY = os.environ["KS_STREAM_KEY"]


def make_api():
    """create the internal Docker FastAPI api"""

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
        if name != KS_STREAM_KEY:
            logger.error("invalid stream key %s", KS_STREAM_KEY)
            response.status_code = 403
            return {"success": False}

        logger.debug("valid stream key")
        asyncio.create_task(ffmpeg())
        return {"sucess": True}

    return api

internal_api = make_api()

