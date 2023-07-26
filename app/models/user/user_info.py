import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, types, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base

class Users_Info(Base):
    __tablename__ = "users_info"
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.String(50), nullable=False)
    user_name = Column(types.String(150), nullable=False)
    user_email = Column(types.String(255), unique=True, nullable=False)
    user_mobile = Column(types.String(20), unique=True, nullable=False)
    user_location = Column(types.String(255), nullable=False)
    user_password = Column(types.Text, nullable=False)
    user_role = Column(types.Integer, ForeignKey('user_roles.id'))
    user_type = Column(types.Integer, ForeignKey('user_types.id'))
    user_credit = Column(types.Float, nullable=False)
    user_is_deleted = Column(types.Boolean, nullable=False)
    user_is_active = Column(types.Boolean, nullable=False)
    created_at = Column(types.DateTime, default=datetime.datetime.now)
    updated_at = Column(types.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    u_type = relationship("User_Types", back_populates="u_info")
    u_role = relationship("User_Roles", back_populates="u_info")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('user_name'),
        UniqueConstraint('user_email')
    )

    def set_password(self, password):
        """Create hashed password."""
        self.user_password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.user_password, password)