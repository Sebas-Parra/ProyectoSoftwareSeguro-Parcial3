from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.sql import func

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)

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
    
    # Relación M:N con Roles
    roles = relationship("Role", secondary="role_modules", back_populates="modules")
    # Relación 1:N con Menús
    menus = relationship("Menu", back_populates="module")