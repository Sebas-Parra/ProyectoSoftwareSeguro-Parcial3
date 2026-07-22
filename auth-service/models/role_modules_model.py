from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from config.database import Base

class RoleModule(Base):
    __tablename__ = "role_modules"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)

    status = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    created_by = Column(Integer)
    updated_by = Column(Integer)