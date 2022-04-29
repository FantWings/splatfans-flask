from flask import make_response
from time import time


def json_response(data=None,
                  msg: str = None,
                  status: int = 0,
                  code: int = 200):
    """
    接口统一函数
    data:   回调数据
    msg:    附加消息
    status: 返回码
    """
    response = {
        "status": status,
        "msg": msg,
        "data": data,
        "timestep": int(round(time() * 1000))
    }
    return make_response(response, code)
