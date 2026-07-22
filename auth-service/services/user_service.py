from sqlalchemy.orm import Session
from repositories import user_repository
import bcrypt

async def get_users(db: Session, username: str):
    return await user_repository.get_user_by_name(db, username)

async def get_all_users(db: Session, page: int = 1, limit: int = 10):
    return await user_repository.get_all_users(db, page, limit)

async def get_user_by_id(db: Session, user_id: int):
    user = await user_repository.get_user_by_id(db, user_id)

    if user is None:
        return None

    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at,
        "created_by": user.created_by,
        "updated_at": user.updated_at,
        "updated_by": user.updated_by,
    }

async def register_user_service(db: Session, username: str, password:str, created_by: int, updated_by: int):
    return await user_repository.insert_user(db, username, _hash_password(password), created_by, updated_by)

async def update_user_service(db: Session, user_id: int, username: str, password:str, updated_by: int):
    return await user_repository.update_user(db, user_id, username, _hash_password(password), updated_by)

async def delete_user_service(db: Session, user_id: int, updated_by: int):
    return await user_repository.delete_user(db, user_id, updated_by)

def _hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
