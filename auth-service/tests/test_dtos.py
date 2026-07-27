import pytest
from pydantic import ValidationError

from dtos.auth_dto import RegisterDTO, LoginDTO


def test_register_dto_accepts_strong_password():
    dto = RegisterDTO(username="juan", password="Sup3rSecreta!")
    assert dto.password == "Sup3rSecreta!"


@pytest.mark.parametrize("weak_password", [
    "Corta1!",          # menos de 8 caracteres
    "todaminuscula1!",  # sin mayuscula
    "TODOMAYUSCULA1!",  # sin minuscula
    "SinNumeros!!!",    # sin digito
    "SinEspeciales123", # sin caracter especial
])
def test_register_dto_rejects_weak_passwords(weak_password):
    with pytest.raises(ValidationError):
        RegisterDTO(username="juan", password=weak_password)


def test_login_dto_does_not_enforce_password_strength():
    """El login debe poder recibir cualquier password (se compara contra el
    hash existente); la politica de fuerza solo aplica al crear/actualizar."""
    dto = LoginDTO(username="administrador", password="cualquier-cosa")
    assert dto.password == "cualquier-cosa"
