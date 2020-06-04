"""Koala Stream FastAPI web service"""
import asyncio
import logging
import os

import aiofiles
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from koalastream.koalastream import ffmpeg, create_local_docker, delete_local_docker
from koalastream.models.login import Login
from koalastream.models.signup import Signup
from koalastream.auth import create_user, do_login

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
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def index():
        logger.info("in index")
        async with aiofiles.open("static/index.html") as f:
            content = await f.read()
        return HTMLResponse(content)

    @app.get("/login")
    async def index():
        async with aiofiles.open("static/login.html") as f:
            content = await f.read()
        return HTMLResponse(content)

    @app.get("/signup")
    async def index():
        async with aiofiles.open("static/signup.html") as f:
            content = await f.read()
        return HTMLResponse(content)

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

    @app.post("/users/login")
    async def user_login(*, response: Response, login: Login):
        logger.info("user login %s", login)
        try:
            await do_login(login)
        except ValueError as ex:
            logger.error("unable to log in %s", str(ex))
            response.status_code = 401
            return {"error": str(ex)}
        logger.info("success")
        return {"success": True}

    @app.post("/users/signup")
    async def user_signup(*, response: Response, signup: Signup):
        logger.info("user signup %s", signup)
        try:
            await create_user(signup)
        except ValueError as ex:
            response.status_code = 400
            return {"error": str(ex)}
        return {"success": True}

    return app
