from pydantic import BaseModel, EmailStr, validator


class Login(BaseModel):
    email: EmailStr
    password: str


    @validator('email')
    def email_to_lowercase(cls, val):
        return val.lower()
