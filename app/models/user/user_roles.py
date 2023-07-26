import datetime
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base


class User_Roles(Base):
    __tablename__ = "user_roles"
    id = Column(types.Integer, primary_key=True)
    user_role = Column(types.String(50), nullable=False)
    created_at = Column(types.DateTime, default=datetime.datetime.now)
    u_info = relationship("User_Info",back_populates="u_role")

    def __repr__(self):
        return f"User_Roles({self.id}, {self.user_role}, {self.created_at})"
    
    @property
    def to_json(self):
        return {
            'id': self.id,
            'user_role': self.user_role,
            'created_at': self.created_at
        }
    
    