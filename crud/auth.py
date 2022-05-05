from uuid import uuid1

# utils
from utils.database import session
from utils.redis import Redis
from utils.generator import gen_token, gen_md5_password
# from utils.smtp import sendmail

# Databases
from tables.t_user import Users
from tables.t_email import Email

from hashlib import md5

from time import time


def userLogin(username: str, password: str) -> object:
    """登录函数"""
    if not username or not password:
        return {"status": 1, "msg": "用户名和密码不可为空"}
    QUERY_RESULT = Users.query.filter_by(username=username,
                                         disabled=False).first()
    if QUERY_RESULT is None:
        return {"status": 1, "msg": "用户名不存在"}
    if gen_md5_password(password) != QUERY_RESULT.password:
        return {"status": 1, "msg": "用户名或密码错误"}
    TOKEN = gen_token(32)
    Redis.write("session/{}".format(TOKEN), QUERY_RESULT.uid)
    return {
        "data": {
            "token": TOKEN,
            "expTime": int(round(time() * 1000)) + 172800000
        }
    }


def registerNewAccount(email: str, password: str, username: str) -> object:
    """
    注册函数
    """
    # 参数检查
    if email is None or password is None:
        return {"status": 1, "msg": "必要参数缺失！"}

    # 检查用户名是否已使用
    if Users.query.filter_by(username=username).first():
        return {"status": 1, "msg": "用户名已被占用"}

    # 检查邮箱是否已使用
    if Email.query.filter_by(email=email).first() is None:
        # 写入邮箱到数据库
        addEmail = Email(email=email)
        session.add(addEmail)

    # 写入用户名到数据库
    NEW_USER = Users(
        uid=uuid1().hex,
        password=gen_md5_password(password),
        username=username,
        email_addr=email,
        avatar="https://cn.gravatar.com/avatar/{}".format(
            md5(email.encode("utf-8")).hexdigest()),
    )
    session.add(NEW_USER)
    # session.flush()
    session.commit()

    token = gen_token(32)
    Redis.write("session/{}".format(token), NEW_USER.uid)
    return {
        "data": {
            "token": token,
            "expTime": int(round(time() * 1000)) + 172800000
        }
    }


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


def logoutUser(token: str) -> None:
    Redis.delete("session/{}".format(token))
    return {}
