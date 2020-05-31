"""Is this a bad idea?"""
import binascii
import hashlib
import logging
import os
from pathlib import Path
from typing import Optional
from .models.user import Password, User

DB_PATH = f"{Path(__file__).parent}"
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
    password_hash = binascii.hexlify(key)
    return Password(
        iterations=iterations, password_hash=password_hash, salt_hex=salt_hex
    )


def create_user(email: str, password1: str, password2: str) -> User:
    """create a user, and save to db"""
    if password1 != password2:
        raise ValueError("unmatched passwords")

    if len(password1) > MAX_PASSWORD_LENGTH:
        raise ValueError(
            "password is too long. Cannot be over %s characters" % MAX_PASSWORD_LENGTH
        )
    password = get_password_hash(password1, ITERATIONS)
    return User(email=email, password=password)
