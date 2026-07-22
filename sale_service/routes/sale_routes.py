from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from controllers import sale_controller
from dtos.sale_dto import SaleDTO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter(prefix="/api/sale", tags=["Sales"])

@router.post("", response_model=SaleDTO, status_code=201)
async def create_sale(sale_data: SaleDTO, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    return await sale_controller.create_sale_controller(db, sale_data, credentials)

@router.get("")
async def get_all_sales(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    return await sale_controller.get_all_sales_controller(db, page, limit, credentials)

@router.put("/{sale_id}", response_model=SaleDTO)
async def update_sale(sale_id: int, sale_data: SaleDTO, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    return await sale_controller.update_sale_controller(db, sale_id, sale_data, credentials)

@router.delete("/{sale_id}")
async def delete_sale(sale_id: int, db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    return await sale_controller.delete_sale_controller(db, sale_id, credentials)