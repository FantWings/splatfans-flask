from flask import make_response


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
    response = {"status": status, "msg": msg, "data": data}
    return make_response(response, code)
