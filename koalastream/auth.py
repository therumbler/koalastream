"""Is this a bad idea?"""
import binascii
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Optional

import aiofiles
from .models.user import Password, User
from .models.signup import Signup
from .models.login import Login
from .models.token import Token
from .email import sendmail

DB_PATH = f"{Path(__file__).parent}/db"
ITERATIONS = 100000

HOSTNAME = os.environ["HOSTNAME"]
KS_EMAIL = os.environ["KS_EMAIL"]
logger = logging.getLogger(__name__)


def get_password_hash(password: str, iterations: int, salt_hex: Optional[str] = None):
    """create a hash"""
    if not salt_hex:
        # must be for a new hash
        # this is a pretty weak random number generator
        salt = os.urandom(32)
        salt_hex = binascii.b2a_hex(salt)
    else:
        salt = binascii.a2b_hex(salt_hex.encode())
    key: bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    password_hash = binascii.hexlify(key).decode()
    return Password(
        iterations=iterations, password_hash=password_hash, salt_hex=salt_hex
    )


async def create_user(signup: Signup) -> User:
    """create a user, and save to db"""
    user = await read_user(signup.email)
    if user:
        raise ValueError("user already exists")

    password = get_password_hash(signup.password1, ITERATIONS)
    user = User(email=signup.email, password=password)
    await save_user(user)
    await send_user_email(user)
    return user


async def create_api_token(user: User):
    pass


async def verify_user(user_id: str, verification_token: str) -> bool:
    user: User = await read_user_by_user_id(user_id)
    if not user:
        raise ValueError("user not found")
    if user.verified:
        raise ValueError("invalid token")
    if user.verification_token != verification_token:
        raise ValueError("invalid token")

    user.verified = True
    await save_user(user)

    return True


async def send_user_email(user: User):
    message_body = f"""

    click here to verify your email

    {HOSTNAME}/users/verify?user={user.user_id}&token={user.verification_token}
    """
    try:
        await sendmail(
            message_body, [user.email,], "Koala Stream Verification", KS_EMAIL,
        )
    except Exception as ex:
        logger.exception(ex)
        logger.error("unable to send email to %s", user.email)
        return False
    user.email_sent = True
    await save_user(user)
    return True


async def do_login(login: Login) -> User:
    user: Optional[User] = await read_user(login.email)
    if not user:
        logger.error("user %s does not exist", login.email)
        raise ValueError("invalid email or password")
    password: Password = get_password_hash(
        login.password, ITERATIONS, user.password.salt_hex
    )

    if password.password_hash != user.password.password_hash:
        logger.error(
            "no match %s %s", password.password_hash, user.password.password_hash
        )
        raise ValueError("invalid email or password")
    if not user.verified:
        raise ValueError("please check your email for verification email")
    token = Token(user_id=user.user_id)
    await save_token(token)
    return token


def _get_user_filepath(email: str):
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    filepath = f"{DB_PATH}/users/{email_hash}.json"
    return filepath


async def read_user_by_user_id(user_id: str):
    filepath = f"{DB_PATH}/users/{user_id}.json"
    try:
        async with aiofiles.open(filepath) as f:
            file_dict = json.loads(await f.read())
    except FileNotFoundError:
        logger.error("cannot find user id %s", user_id)
        return None
    return User(**file_dict)


async def read_user(email) -> Optional[User]:
    filepath = _get_user_filepath(email)
    try:
        async with aiofiles.open(filepath) as f:
            file_dict = json.loads(await f.read())
    except FileNotFoundError:
        return None
    return User(**file_dict)


def _get_token_filepath(token: Token):
    filepath = f"{DB_PATH}/users/{token.token}.json"
    return filepath


async def save_token(token: Token):
    filepath = _get_token_filepath(token)
    parent = Path(filepath).parent
    if not os.path.isdir(parent):
        os.makedirs(parent)
    logger.info("saving token to %s", filepath)
    async with aiofiles.open(filepath, "w") as f:
        await f.write(json.dumps(token.dict()))


async def save_user(user: User):
    filepath = _get_user_filepath(user.email)
    logger.info("saving to %s", filepath)
    parent = Path(filepath).parent
    if not os.path.isdir(parent):
        os.makedirs(parent)
    async with aiofiles.open(filepath, "w") as f:
        await f.write(json.dumps(user.dict()))
