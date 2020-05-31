"""test the auth module"""
from koalastream.auth import get_password_hash, create_user


def test_get_password_hash():
    """test the basic hash function"""
    iterations = 100
    password = "letmein"
    resp1 = get_password_hash(password, iterations)
    salt = resp1.salt_hex
    resp2 = get_password_hash(password, iterations, salt)

    assert resp1.password_hash == resp2.password_hash


def test_create_user_success():
    email = "fake@example.com"
    password1 = "letmein"
    password2 = "letmein"

    user = create_user(email, password1, password2)

    assert user.verification_token is not None
