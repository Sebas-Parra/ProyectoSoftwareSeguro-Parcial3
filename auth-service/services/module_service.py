from sqlalchemy.orm import Session
from repositories import module_repository

async def get_all_modules_service(db: Session):
    return await module_repository.get_all_modules(db)

async def insert_module_service(db: Session, name: str, icon: str, description: str, created_by: int, updated_by: int):
    return await module_repository.insert_module(db, name, icon, description, created_by, updated_by)

async def update_module_service(db: Session, module_id: int, name: str, icon: str, description: str, status: bool, updated_by: int):
    return await module_repository.update_module(db, module_id, name, icon, description, status, updated_by)

async def delete_module_service(db: Session, module_id: int, updated_by: int):
    return await module_repository.delete_module(db, module_id, updated_by)

async def assign_module_to_role_service(db: Session, role_id: int, module_id: int, created_by: int, updated_by: int):
    return await module_repository.assign_module_to_role(db, role_id, module_id, created_by, updated_by)