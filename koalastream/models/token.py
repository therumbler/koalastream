from pydantic import BaseModel, Field
from .user import create_verification_token


class Token(BaseModel):
    """an API token"""

    token: str = Field(default_factory=create_verification_token)
    user_id: str
