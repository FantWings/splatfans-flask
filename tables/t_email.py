from utils.database import db
from sqlalchemy.sql import functions
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship, backref


class Email(db.Model):
    """邮箱表"""
    __tablename__ = "t_email"
    email = Column(String(32), primary_key=True, nullable=False, comment="邮箱")
    active = Column(Integer, nullable=False, default=0, comment="邮箱已验证")
    create_time = Column(DateTime,
                         nullable=False,
                         server_default=functions.now(),
                         comment="创建时间")
    update_time = Column(
        db.DateTime,
        nullable=False,
        server_default=functions.now(),
        comment="修改时间",
        onupdate=functions.now(),
    )
    owner = relationship("Users", backref=backref('email'))
