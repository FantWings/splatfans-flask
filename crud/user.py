from functions.loginrequired import loginRequired
from tables.t_user import Users


@loginRequired
def get_user_info(uid):
    """获取用户信息"""
    QUERY_RESULT = Users.query.get(uid)
    if QUERY_RESULT is None:
        return {"status": 1, "msg": "用户不存在或者状态不正常"}
    if QUERY_RESULT.disabled is True:
        return {"status": 1000, "msg": "用户账号已注销"}

    iksm_status = True if QUERY_RESULT.session_token and \
        QUERY_RESULT.cookie else False

    return {
        "data": {
            "username": QUERY_RESULT.username,
            "uuid": QUERY_RESULT.uuid,
            "avatar": QUERY_RESULT.avatar,
            "iksm": iksm_status,
            "qq": QUERY_RESULT.qq,
            "phone": QUERY_RESULT.phone,
            "email": QUERY_RESULT.email.email,
            "register_time": QUERY_RESULT.create_time
        }
    }
