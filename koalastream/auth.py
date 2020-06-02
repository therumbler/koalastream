"""Is this a bad idea?"""
import binascii
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Optional
from .models.user import Password, User
from .models.login import Signup

DB_PATH = f"{Path(__file__).parent}/db"
ITERATIONS = 100000
MAX_PASSWORD_LENGTH = 128
logger = logging.getLogger(__name__)


def get_password_hash(password: str, iterations: int, salt_hex: Optional[bytes] = None):
    """create a hash"""
    if not salt_hex:
        # must be for a new hash
        # this is a pretty weak random number generator
        salt = os.urandom(32)
        salt_hex = binascii.b2a_hex(salt)
    else:
        salt = binascii.a2b_hex(salt_hex)
    key: bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    password_hash = binascii.hexlify(key).decode()
    return Password(
        iterations=iterations, password_hash=password_hash, salt_hex=salt_hex
    )


def create_user(signup: Signup) -> User:
    """create a user, and save to db"""
    user = read_user(signup.email)
    if user:
        raise ValueError("user already exists")
    if signup.password1 != signup.password2:
        raise ValueError("unmatched passwords")

    if len(signup.password1) > MAX_PASSWORD_LENGTH:
        raise ValueError(
            "password is too long. Cannot be over %s characters" % MAX_PASSWORD_LENGTH
        )
    password = get_password_hash(signup.password1, ITERATIONS)
    user = User(email=signup.email, password=password)
    save_user(user)
    return user


async def login(email: str, password: str):
    user = read_user(email)
    if not user:
        raise ValueError("invalid email or password")


def _get_user_filepath(email: str):
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    filepath = f"{DB_PATH}/users/{email_hash}.json"
    return filepath


def read_user(email) -> Optional[User]:
    filepath = _get_user_filepath(email)
    try:
        with open(filepath) as f:
            file_dict = json.load(f)
    except FileNotFoundError:
        return None
    return User(**file_dict)


def save_user(user: User):
    filepath = _get_user_filepath(user.email)
    logger.info("saving to %s", filepath)
    parent = Path(filepath).parent
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with open(filepath, "w") as f:
        f.write(json.dumps(user.dict()))
