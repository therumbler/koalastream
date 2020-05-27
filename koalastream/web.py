"""Koala Stream FastAPI web service"""
import asyncio
import logging
import os

from koalastream.koalastream import ffmpeg, create_local_docker, delete_local_docker

from fastapi import FastAPI, Response

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


def make_web():
    """make external web app"""
    app = FastAPI(title="Koala Stream")

    @app.post("/server")
    async def create_server(response: Response,):
        """create rtmp server"""
        resp = await create_local_docker()
        if "error" in resp:
            response.status_code = 409
        return resp

    @app.delete("/server/{container_id}")
    async def delete_server(container_id: str):
        """delete the rtmp server"""
        resp = await delete_local_docker(container_id)
        return resp

    return app
