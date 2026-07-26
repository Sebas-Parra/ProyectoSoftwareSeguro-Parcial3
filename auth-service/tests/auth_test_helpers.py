import types

from repositories import role_repository, user_repository
from services import jwt_service, user_service


def bearer(token):
    return types.SimpleNamespace(credentials=token)


async def make_admin_context(db):
    """Crea el rol 'administrador' (id=1, igual que en insert.sql), un
    usuario con ese rol, y devuelve un access token real y valido firmado
    con la misma llave RSA que usan los tests de jwt_service."""
    role = await role_repository.insert_role(db, "administrador", "rol admin", "pi-crown", None, None)
    assert role.id == 1  # primera fila insertada en la BD en memoria -> id=1

    hashed = user_service._hash_password("Vikingofarifor123.")
    user = await user_repository.insert_user(db, "administrador", hashed, None, None)
    await role_repository.asign_role_to_user(db, user.id, role.id, None, None)

    access_token, refresh_token = await jwt_service.generar_tokens(
        user.id, user.username, role.name, role.id
    )
    return user, role, access_token, refresh_token
