from sqlalchemy.orm import Session
from repositories import user_repository, module_repository
from services.jwt_service import generar_tokens, generar_temptoken
import bcrypt


async def login_user_service(db: Session, username: str, password: str):
    user = await user_repository.get_user_by_name(db, username)
    if user and _verify_password(password, user.password):
        return await generar_temptoken(user.id, user.username), await user_repository.get_user_roles(db, user.id)
    return None

async def select_role_service(db: Session, user_id: int, role_id: int):
    
    user = await user_repository.get_user_by_id(db, user_id)

    if not user:
        return None

    roles = await user_repository.get_user_roles(db, user_id)
    if not any(role['id'] == role_id for role in roles):
        return None

    modules = await module_repository.get_module_names_by_role(db, role_id)

    return await generar_tokens(
        user.id, user.username, next(role['name'] for role in roles if role['id'] == role_id), role_id,
        modules=modules,
    )


def _verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )