from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class Signup(BaseModel):
    email: EmailStr
    password1: str
    password2: str
