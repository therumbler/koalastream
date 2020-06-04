import binascii
import hashlib
import logging
import os
from pydantic import BaseModel, EmailStr, validator


logger = logging.getLogger(__name__)


class Password(BaseModel):
    password_hash: str
    iterations: int
    salt_hex: str


class User(BaseModel):
    email: EmailStr
    email_sent: bool = False
    verified: bool = False
    password: Password
    verification_token: str = None
    user_id: str = None

    @validator("verification_token", always=True)
    def create_verification_token(cls, val):
        """Set a default value"""
        if val:
            return val
        random_value = os.urandom(32)
        val = binascii.b2a_hex(random_value).decode()
        logger.error("val types = %s", type(val))
        return val

    @validator("user_id", always=True)
    def create_user_id(cls, v, values):
        if "email" in values:
            user_id = hashlib.sha256(values["email"].encode()).hexdigest()
            logger.info("user_id = %s", user_id)
            return user_id
