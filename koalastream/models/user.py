import binascii
import hashlib
import logging
import os
from pydantic import BaseModel, EmailStr, validator, Field


logger = logging.getLogger(__name__)


def create_verification_token():
    random_value = os.urandom(32)
    return binascii.b2a_hex(random_value).decode()


class Password(BaseModel):
    password_hash: str
    iterations: int
    salt_hex: str


class User(BaseModel):
    email: EmailStr
    email_sent: bool = False
    verified: bool = False
    password: Password
    verification_token: str = Field(default_factory=create_verification_token)
    user_id: str = None

    @validator("user_id", always=True)
    def create_user_id(cls, v, values):
        if "email" in values:
            user_id = hashlib.sha256(values["email"].encode()).hexdigest()
            logger.info("user_id = %s", user_id)
            return user_id
