import datetime
from sqlalchemy import Column, types
from app.db.base_class import Base


class User_Denylist(Base):
    __tablename__ = "user_login"
    user_id = Column(types.Integer, primary_key=True)
    refresh_token = Column(types.String(450), nullable=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)

    def __repr__(self):
        return f"User_Login({self.user_id}, {self.created_at})"
