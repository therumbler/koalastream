import logging
import os

import aiofiles
from fastapi import FastAPI, Response, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import HTMLResponse



from koalastream.koalastream import ffmpeg, create_local_docker, delete_local_docker, STREAMS
from koalastream.models.login import Login
from koalastream.models.signup import Signup
from koalastream.models.server import Server
from koalastream.auth import create_user, do_login, verify_user, verify_with_token


OPEN_API_PREFIX = os.getenv("KS_OPEN_API_PREFIX", "")
logger = logging.getLogger(__name__)

def make_web():
    """make external web app"""
    app = FastAPI(title="Koala Stream", openapi_prefix=OPEN_API_PREFIX)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./users/token")

    @app.get("/")
    async def index():
        async with aiofiles.open("static/index.html") as f:
            content = await f.read()
        return HTMLResponse(content)

    @app.get("/login")
    async def login_static():
        async with aiofiles.open("static/login.html") as f:
            content = await f.read()
        return HTMLResponse(content)

    @app.get("/app")
    async def app_static():
        async with aiofiles.open("static/app.html") as f:
            content = await f.read()
        return HTMLResponse(content)

    @app.get("/signup")
    async def signup_static():
        async with aiofiles.open("static/signup.html") as f:
            content = await f.read()
        return HTMLResponse(content)

    @app.get("/survey")
    async def signup_static():
        async with aiofiles.open("static/survey.html") as f:
            content = await f.read()
        return HTMLResponse(content)


    @app.post("/server")
    @verify_with_token()
    async def create_server(response: Response, server: Server, token: str = Depends(oauth2_scheme)):
        """create rtmp server"""
        resp = await create_local_docker(server)
        if "error" in resp:
            response.status_code = 409
        return resp

    @app.delete("/server/{container_id}")
    @verify_with_token()
    async def delete_server(
        response: Response, container_id: str, token: str = Depends(oauth2_scheme)
    ):
        """delete the rtmp server"""
        resp = await delete_local_docker(container_id)
        if "error" in resp:
            response.status_code = 400
            if "No such container" in resp["error"]:
                response.status_code = 404
        return resp

    @app.post("/users/login")
    async def user_login(*, response: Response, login: Login):
        try:
            token = await do_login(login)
        except ValueError as ex:
            logger.error("unable to log in %s", str(ex))
            response.status_code = 401
            return {"error": str(ex)}
        logger.info("login success")
        return token

    @app.post("/users/token")
    async def user_token(
        *, response: Response, username: str = Form(...), password: str = Form(...)
    ):
        """oauth2 style form login"""
        login = Login(email=username, password=password)
        try:
            token = await do_login(login)
        except ValueError as ex:
            logger.error("unable to log in %s", str(ex))
            response.status_code = 401
            return {"error": str(ex)}
        logger.info("login success")
        return {"access_token": token.token, "token_type": "bearer"}

    @app.post("/users/signup")
    async def user_signup(*, response: Response, signup: Signup):
        logger.info("user signup %s", signup)
        try:
            await create_user(signup)
        except ValueError as ex:
            response.status_code = 400
            return {"error": str(ex)}
        return {"success": True}

    @app.get("/users/verify")
    async def user_verify(*, response: Response, user: str, token: str):
        logger.info("user_verify user %s, token %s", user, token)
        try:
            await verify_user(user_id=user, verification_token=token)
        except ValueError as ex:
            response.status_code = 401
            return {"error": str(ex)}
        return {"success": True}

    return app
