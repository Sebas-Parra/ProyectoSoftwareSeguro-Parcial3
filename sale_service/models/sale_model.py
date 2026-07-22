from sqlalchemy import Column, Integer, String, Boolean, DateTime, Double
from config.database import Base
from sqlalchemy.sql import func

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    total = Column(Double, nullable=False)
    
    # Estado 
    status = Column(Boolean, default=True, nullable=False)

    # Fecha de registro
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Fecha de actualización
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    created_by = Column(Integer, index=True)
    updated_by = Column(Integer, index=True)    