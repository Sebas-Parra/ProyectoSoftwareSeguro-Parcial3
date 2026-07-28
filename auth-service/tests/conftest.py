import os
import subprocess
import tempfile

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_db")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_DB", "0")
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

os.environ.setdefault("PRIVATE_KEY", _private_path)
os.environ.setdefault("PUBLIC_KEY", _public_path)
