from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy.sql import func

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    url = Column(String, nullable=True) # Solo en nodos hoja
    modulo_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("menus.id"), nullable=True)
    
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

    # Relación con el módulo padre
    module = relationship("Module", back_populates="menus")
    
    # Autorelación para jerarquía
    parent = relationship("Menu", remote_side=[id], back_populates="children")
    children = relationship("Menu", back_populates="parent")

    # NUEVA: Relación muchos a muchos con Role
    roles = relationship("Role", secondary="role_menus", back_populates="menus")