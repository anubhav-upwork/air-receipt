import datetime
from sqlalchemy import Column, types, ForeignKey
from app.db.dbconnect import Base


class User_Login(Base):
    __tablename__ = "user_login"
    id = Column(types.Integer, primary_key=True, index=True)
    user_id = Column(types.Integer, ForeignKey('user_info.id'), nullable=False)
    token = Column(types.Text(500), nullable=False)
    is_logged_in = Column(types.Boolean, nullable=False, default=False)
    is_expired = Column(types.Boolean, nullable=False, default=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())
    updated_at = Column(types.DateTime(timezone=True), nullable=True, onupdate=datetime.datetime.now())

    def __repr__(self):
        return f"User_Login({self.id}, {self.user_id}, {self.is_expired}, {self.is_logged_in})"
