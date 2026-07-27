import re

from pydantic import BaseModel, field_validator

PASSWORD_MIN_LENGTH = 8


class RegisterDTO(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        """Shift-Left: rechaza contraseñas débiles en el borde de la API,
        antes de que lleguen al hashing/almacenamiento."""
        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValueError(f"La contraseña debe tener al menos {PASSWORD_MIN_LENGTH} caracteres.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe incluir al menos un número.")
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError("La contraseña debe incluir al menos un carácter especial.")
        return value


class LoginDTO(BaseModel):
    username: str
    password: str


class SelectRoleDTO(BaseModel):
    role_id: int