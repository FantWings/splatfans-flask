from utils.database import db
from sqlalchemy.sql import func


class Email(db.Model):
    """邮箱表"""
    __tablename__ = "t_email"
    email = db.Column(db.String(32),
                      primary_key=True,
                      nullable=False,
                      comment="邮箱")
    verifyed = db.Column(db.Integer,
                         nullable=False,
                         default=0,
                         comment="邮箱已验证")
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
