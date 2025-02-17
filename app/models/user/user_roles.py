import datetime
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User_Roles(Base):
    __tablename__ = "user_roles"
    id = Column(types.Integer, primary_key=True, index=True)
    user_role = Column(types.String(50), unique=True, nullable=False)
    user_access_level = Column(types.SmallInteger, nullable=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())

    # user role and info relationship
    # u_info = relationship("User_Info", back_populates="u_role")
    users = relationship("User_Info", primaryjoin="User_Roles.id == User_Info.user_role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User_Roles({self.id}, {self.user_role}, {self.user_acess_level}, {self.created_at})"

    @property
    def to_json(self):
        return {
            'id': self.id,
            'user_role': self.user_role,
            'user_access_level': self.user_acess_level,
            'created_at': self.created_at
        }
