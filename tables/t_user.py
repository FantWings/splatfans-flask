from sqlalchemy.sql import func
from utils.database import db

# 外键表
from tables.t_email import Email


class Users(db.Model):
    """用户表"""
    __tablename__ = "t_users"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="索引")
    uuid = db.Column(db.String(64), nullable=False, comment="用户UUID")
    nickname = db.Column(db.String(16), nullable=False, comment="用户名")
    password = db.Column(db.String(32), comment="密码")
    phone = db.Column(
        db.String(11),
        nullable=False,
        comment="手机号",
        unique=True,
    )
    avatar = db.Column(db.String(256), nullable=True, comment="头像")
    qq = db.Column(db.String(13), comment="QQ号")
    create_time = db.Column(db.DateTime,
                            nullable=False,
                            server_default=func.now(),
                            comment="创建时间")
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        comment="修改时间",
        onupdate=func.now(),
    )
    # 邮箱（外键）
    email_addr = db.Column(db.String(32),
                           db.ForeignKey(Email.email),
                           nullable=False,
                           comment="邮箱")
    email = db.relationship(Email, backref="email_of_user")
