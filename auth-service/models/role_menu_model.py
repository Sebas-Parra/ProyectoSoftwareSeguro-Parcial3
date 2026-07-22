from sqlalchemy import Column, Integer, ForeignKey
from config.database import Base

class RoleMenu(Base):
    __tablename__ = "role_menus"
    
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)