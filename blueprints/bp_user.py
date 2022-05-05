from flask import Blueprint
from utils.response import json_response
from crud.user import get_user_info

blueprint = Blueprint("user", __name__)


@blueprint.route('userinfo', methods=['GET'])
def userInfo():
    """获取用户信息"""
    # body = request.get_json()
    result = get_user_info()
    return json_response(**result)
