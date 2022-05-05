from sqlalchemy.sql import functions
from utils.database import db
from sqlalchemy import (Column, String, ForeignKey, DateTime, Boolean, TEXT)


class Users(db.Model):
    """用户表"""
    __tablename__ = "t_users"
    uid = Column(String(64),
                 nullable=False,
                 primary_key=True,
                 comment="用户UUID")
    username = Column(String(16), nullable=False, comment="用户名")
    nickname = Column(String(16), nullable=True, comment="昵称")
    password = Column(String(32), comment="密码")
    phone = Column(
        String(11),
        nullable=True,
        comment="手机号",
        unique=True,
    )
    disabled = Column(Boolean,
                      nullable=False,
                      comment="账号是否已注销",
                      default=False)
    avatar = Column(String(256), nullable=True, comment="头像")
    qq = Column(String(13), comment="QQ号")
    create_time = Column(DateTime,
                         nullable=False,
                         server_default=functions.now(),
                         comment="创建时间")
    update_time = Column(
        DateTime,
        nullable=False,
        server_default=functions.now(),
        comment="修改时间",
        onupdate=functions.now(),
    )
    session_token = Column(String(40), comment="session密钥")
    cookie = Column(TEXT(320), comment="cookie")
    # 邮箱（外键）
    email_addr = Column(String(32),
                        ForeignKey("t_email.email"),
                        nullable=False,
                        comment="邮箱")
