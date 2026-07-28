import bcrypt
from services.user_service import _hash_password


def test_hash_password_uses_random_salt():
    h1 = _hash_password("Sup3rSecreta!")
    h2 = _hash_password("Sup3rSecreta!")
    assert h1 != h2


def test_hash_password_is_verifiable_with_bcrypt():
    plain = "Sup3rSecreta!"
    hashed = _hash_password(plain)
    assert bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def test_hash_password_rejects_wrong_password():
    hashed = _hash_password("Sup3rSecreta!")
    assert not bcrypt.checkpw("otra-clave".encode("utf-8"), hashed.encode("utf-8"))
