from pydantic import BaseModel, EmailStr, validator

MAX_PASSWORD_LENGTH = 128


class Signup(BaseModel):
    email: EmailStr
    password1: str
    password2: str

    @validator("password2")
    def check_passwords(cls, password2, values):
        """ensure passwords are the same"""
        if "password1" in values and password2 != values["password1"]:
            raise ValueError("passwords do not match")
        if len(password2) > MAX_PASSWORD_LENGTH:
            raise ValueError(
                f"password cannot be longer than {MAX_PASSWORD_LENGTH} characters"
            )
        return password2
