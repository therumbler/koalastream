"""test the auth module"""
from uuid import uuid4
from koalastream.auth import get_password_hash, create_user
from koalastream.models.login import Signup


def test_get_password_hash():
    """test the basic hash function"""
    iterations = 100
    password = "letmein"
    resp1 = get_password_hash(password, iterations)
    salt = resp1.salt_hex
    resp2 = get_password_hash(password, iterations, salt)

    assert resp1.password_hash == resp2.password_hash


def test_create_user_success():
    email = f"{uuid4()}@example.com"
    password1 = "letmein"
    password2 = "letmein"
    signup = Signup(email=email, password1=password1, password2=password2)
    user = create_user(signup)

    assert user.verification_token is not None
