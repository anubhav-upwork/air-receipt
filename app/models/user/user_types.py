import datetime
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User_Types(Base):
    __tablename__ = "user_types"
    id = Column(types.Integer, primary_key=True, index=True)
    user_type = Column(types.String(50), unique=True, nullable=False)
    usage_limit_days = Column(types.Integer, nullable=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())

    # user info to user type relationship
    # u_info = relationship('User_Info', back_populates="u_type")
    users = relationship("User_Info", primaryjoin="User_Types.id == User_Info.user_type", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User_Types({self.id}, {self.user_type}, {self.usage_limit_days}, {self.created_at})"

    @property
    def to_json(self):
        return {
            'id': self.id,
            'user_type': self.user_type,
            'usage_limit_days': self.usage_limit_days,
            'created_at': self.created_at
        }
