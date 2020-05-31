"""test the auth module"""
from koalastream.auth import get_password_hash


def test_get_password_hash():
    """test the basic hash function"""
    iterations = 100000
    password = "letmein"
    resp1 = get_password_hash(password, iterations)
    salt = resp1["salt_hex"]
    resp2 = get_password_hash(password, iterations, salt)

    assert resp1["password_hash"] == resp2["password_hash"]
