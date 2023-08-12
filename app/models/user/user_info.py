import datetime
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User_Info(Base):
    __tablename__ = "user_info"
    id = Column(types.Integer, primary_key=True, index=True)
    user_name = Column(types.String(150), unique=True, nullable=False)
    user_email = Column(types.String(255), unique=True, nullable=False)
    user_mobile = Column(types.String(20), unique=True, nullable=False)
    user_location = Column(types.String(255))
    user_password = Column(types.Text, nullable=False)
    user_role = Column(types.Integer, ForeignKey('user_roles.id'), nullable=False)
    user_type = Column(types.Integer, ForeignKey('user_types.id'), nullable=False)
    user_credit = Column(types.Numeric(12, 2), nullable=False)
    user_is_deleted = Column(types.Boolean, nullable=False, default=False)
    user_is_active = Column(types.Boolean, nullable=False, default=True)
    user_is_superuser = Column(types.Boolean, nullable=False, default=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())
    updated_at = Column(types.DateTime(timezone=True), nullable=True, onupdate=datetime.datetime.now())

    userLogin = relationship("User_Login", primaryjoin="User_Info.id == User_Login.user_id",
                             cascade="all, delete-orphan")
    user_audit = relationship("User_Audit_Trail", primaryjoin="User_Info.id == User_Audit_Trail.user_id",
                              cascade="all, delete-orphan")

    # document_usr = relationship("Document_User", primaryjoin="User_Info.id == Document_User.id",
    #                             cascade="all, delete-orphan")
    # user role and type relationships
    # u_type = relationship("User_Types", back_populates="user_info")
    # u_role = relationship("User_Roles", back_populates="user_info")

    # __table_args__ = (
    #     PrimaryKeyConstraint('id', name='user_pk'),
    #     UniqueConstraint('user_name'),
    #     UniqueConstraint('user_email')
    # )

    def __repr__(self):
        return f"User_Info({self.id}, {self.user_name}, {self.user_credit}, {self.created_at})"
