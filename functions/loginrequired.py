from flask import request
from utils.redis import Redis


def loginRequired(fn):
    """
    装饰器函数，用来装饰需要登录之后才可执行的函数，返回用户token给调用他的函数
    """

    def get_user_id_from_redis(*args, **xargs) -> object:
        # 从HEADER取得TOKEN
        token = request.headers.get("token")
        # 使用token从redis中读取用户ID
        uid = Redis.read("session/{}".format(token))
        if uid:
            # 刷新Token有效期
            Redis.expire("session/{}".format(token))
            return fn(uid, *args, **xargs)
        else:
            return {"status": 10, "msg": "需要登录"}

    return get_user_id_from_redis
