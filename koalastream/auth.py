"""Is this a bad idea?"""
import binascii
import hashlib
import logging
import os
from pathlib import Path
from typing import Optional

DB_PATH = f"{Path(__file__).parent}"
ITERATIONS = 100000
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
    return {
        "password_hash": password_hash,
        "iterations": iterations,
        "salt_hex": salt_hex,
    }
