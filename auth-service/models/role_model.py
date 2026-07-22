from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.sql import func

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)

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
    
    # Relaciones M:N existentes
    users = relationship("User", secondary="user_roles", back_populates="roles")
    modules = relationship("Module", secondary="role_modules", back_populates="roles")

    # NUEVA: Relación muchos a muchos con Menu
    menus = relationship("Menu", secondary="role_menus", back_populates="roles")