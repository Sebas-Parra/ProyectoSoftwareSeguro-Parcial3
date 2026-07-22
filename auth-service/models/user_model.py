from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    # Datos Generales
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

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

    created_by = Column(Integer, nullable=True, index=True)
    updated_by = Column(Integer, nullable=True, index=True)

    roles = relationship("Role", secondary="user_roles", back_populates="users")