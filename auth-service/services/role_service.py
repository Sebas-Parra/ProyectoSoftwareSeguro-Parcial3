from sqlalchemy.orm import Session
from repositories import role_repository

async def get_all_roles_service(db: Session):
    return await role_repository.get_all_roles(db)

async def insert_role_service(db: Session, name: str, description: str, icon: str, created_by: int, updated_by: int):
    return await role_repository.insert_role(db, name, description, icon, created_by, updated_by)

async def update_role_service(db: Session, role_id: int, name: str, icon: str, description: str, status: bool, updated_by: int):
    return await role_repository.update_role(db, role_id, name, icon, description, status, updated_by)

async def delete_role_service(db: Session, role_id: int, updated_by: int):
    return await role_repository.delete_role(db, role_id, updated_by)

async def asign_role_to_user_service(db: Session, user_id: int, role_id: int, created_by: int, updated_by: int):
    return await role_repository.asign_role_to_user(db, user_id, role_id, created_by, updated_by)

async def desasign_role_from_user_service(db: Session, user_id: int, role_id: int):
    return await role_repository.desasign_role_from_user(db, user_id, role_id)

