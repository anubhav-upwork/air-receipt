import datetime
from sqlalchemy import Column, types, ForeignKey
from app.db.base_class import Base


class User_Login(Base):
    __tablename__ = "user_login"
    user_id = Column(types.Integer, ForeignKey('user_info.id'), nullable=False, unique=True)
    access_token = Column(types.String(450), primary_key=True)
    refresh_token = Column(types.String(450), nullable=False)
    status = Column(types.Boolean, nullable=False, default=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    updated_at = Column(types.DateTime(timezone=True), nullable=True, onupdate=datetime.datetime.now())

    def __repr__(self):
        return f"User_Login({self.user_id}, {self.status}, {self.created_at})"
