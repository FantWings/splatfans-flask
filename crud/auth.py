from flask import request
from uuid import uuid1

# utils
from utils.database import db
from utils.redis import Redis
from utils.generator import gen_token, gen_md5_password
# from utils.smtp import sendmail

# Databases
from tables.t_user import Users
from tables.t_email import Email

from hashlib import md5

from time import time


def loginRequired(fn):
    """
    装饰器函数，用来装饰需要登录之后才可执行的函数，返回用户token给调用他的函数
    """

    def getUserId(*args, **xargs):
        # 从HEADER取得TOKEN
        token = request.headers.get("token")
        # 使用token从redis中读取用户ID
        userId = Redis.read("session/{}".format(token))
        if userId:
            # 刷新Token有效期
            Redis.expire("session/{}".format(token))
            return fn(int(userId), *args, **xargs)
        else:
            return {"status": 10, "msg": "需要登录"}

    return getUserId


def registerNewAccount(email: str, password: str, nickname: str):
    """
    注册一个新账户
    """
    # 参数检查
    if email is None or password is None:
        return {"status": 1, "msg": "必要参数缺失！"}

    # 检查邮箱是否已使用
    if Email.query.filter_by(email=email).first():
        return {"status": 1, "msg": "邮箱已被占用"}
    # 写入邮箱到数据库
    addEmail = Email(email=email)
    db.session.add(addEmail)

    # 写入用户名到数据库
    addUser = Users(
        password=gen_md5_password(password),
        nickname=nickname,
        email_addr=email,
        avatar="https://cn.gravatar.com/avatar/{}".format(
            md5(email.encode("utf-8")).hexdigest()),
        uuid=uuid1(),
    )
    db.session.add(addUser)
    db.session.commit()

    query = (Users.query.with_entities(Users.id).filter_by(email_addr=email,
                                                           deleted=0).first())
    token = gen_token(32)
    Redis.write("session_{}".format(token), query.id)
    return {"data": {"token": token}}


# @loginRequired
# def sendCodeByEmail(uid, email):
#     query = t_user.query.filter_by(id=uid).first()
#     if query is None:
#         return {"status": 1, "msg": "UID无效！"}
#     verifyCode = genRandomCode(lenguth=6)
#     Redis.write("verify_{}".format(uid), verifyCode, expire=300)
#     log("VerifyEmail sended to: {} for uid {}".format(email, uid))
#     log("uid {} verify code is: {}".format(uid, verifyCode), "debug")
#     sendmail(
#         """
#         您的本次注册验证码为：
#         {0}
#         """.format(
#             verifyCode
#         ),
#         email,
#         "账户注册",
#         current_app.config.get("SITE_NAME"),
#     )
#     return {"msg": "验证码已发送"}

# @loginRequired
# def add2FAToAccount(uid, verifyCode):
#     query = t_user.query.filter_by(id=uid).first()
#     correctCode = Redis.read("verify_{}".format(uid))
#     if verifyCode != correctCode:
#         log(
#             "User {} input a invaild code [{}], it should be [{}]".format(
#                 query.username, verifyCode, correctCode
#             ),
#             "debug",
#         )
#         return {"status": 1, "msg": "验证码不正确"}

#     if query is None:
#         log("User {} input a invaild args", "warn")
#         return {"status": 1, "msg": "参数有误！"}
#     query.vaild = True
#     db.session.commit()
#     log("user {} is account is now active".format(query.username))
#     Redis.delete("verify_{}".format(uid))
#     return {"msg": "邮箱绑定成功"}


def userLogin(username, password):
    if not username or not password:
        return {"status": 1, "msg": "用户名和密码不可为空"}
    query = (Users.query.with_entities(
        Users.id, Users.password).filter_by(email_addr=username).first())
    if query is None:
        return {"status": 1, "msg": "用户名或密码错误"}
    if gen_md5_password(password) != query.password:
        return {"status": 1, "msg": "用户名或密码错误"}

    token = gen_token(32)
    Redis.write("session/{}".format(token), query.id)
    return {
        "data": {
            "token": token,
            "expTime": int(round(time() * 1000)) + 172800000
        }
    }


def logoutUser(token: str):
    Redis.delete("session/{}".format(token))
    return {}
