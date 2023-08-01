# import datetime
# from sqlalchemy import Column, types, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
# from sqlalchemy.orm import relationship
# from app.db.dbconnect import Base



# class User_Login(Base):
#     __tablename__ = "user_login"
#     id = Column(types.Integer, primary_key=True)
#     user_id = Column(types.String(50), nullable=False)
#     user_name = Column(types.String(150), nullable=False)
#     user_token = Column(types.Text(500), nullable=False)
#     user_token_expired
#     created_at = Column(types.DateTime, default=datetime.datetime.now)
#     updated_at = Column(types.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
#     u_type = relationship("User_Types", back_populates="u_info")
#     u_role = relationship("User_Roles", back_populates="u_info")

#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='user_pk'),
#         UniqueConstraint('user_name'),
#         UniqueConstraint('user_email')
#     )