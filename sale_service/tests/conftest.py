import os
import subprocess
import tempfile

import pytest

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_db")
os.environ.setdefault("ALGORITHM", "RS256")
os.environ.setdefault("ECUADOR_TZ", "America/Guayaquil")

_tmp_dir = tempfile.mkdtemp(prefix="jwt_test_keys_")
_private_path = os.path.join(_tmp_dir, "private.pem")
_public_path = os.path.join(_tmp_dir, "public.pem")

subprocess.run(
    ["openssl", "genpkey", "-algorithm", "RSA", "-out", _private_path, "-pkeyopt", "rsa_keygen_bits:2048"],
    check=True, capture_output=True,
)
subprocess.run(
    ["openssl", "rsa", "-in", _private_path, "-outform", "PEM", "-pubout", "-out", _public_path],
    check=True, capture_output=True,
)

# sale_service NUNCA debe tener la llave privada en producción (Zero Trust);
# aquí solo la usan las pruebas para FIRMAR tokens de prueba como si fuera el Master.
with open(_private_path, "rb") as f:
    _MASTER_PRIVATE_KEY_FOR_TESTS = f.read()

os.environ.setdefault("PUBLIC_KEY", _public_path)


@pytest.fixture
def master_private_key():
    return _MASTER_PRIVATE_KEY_FOR_TESTS
