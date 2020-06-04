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

DB_PATH = f"{Path(__file__).parent}/db"
ITERATIONS = 100000
MAX_PASSWORD_LENGTH = 128
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


async def send_user_email(user: User):
    pass


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
    return user


def _get_user_filepath(email: str):
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    filepath = f"{DB_PATH}/users/{email_hash}.json"
    return filepath


async def read_user(email) -> Optional[User]:
    filepath = _get_user_filepath(email)
    try:
        async with aiofiles.open(filepath) as f:
            file_dict = json.loads(await f.read())
    except FileNotFoundError:
        return None
    return User(**file_dict)


async def save_user(user: User):
    filepath = _get_user_filepath(user.email)
    logger.info("saving to %s", filepath)
    parent = Path(filepath).parent
    if not os.path.isdir(parent):
        os.makedirs(parent)
    async with aiofiles.open(filepath, "w") as f:
        await f.write(json.dumps(user.dict()))
