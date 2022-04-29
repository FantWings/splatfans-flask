from flask import Blueprint, request
from utils.response import json_response
from crud.user import get_user_info

blueprint = Blueprint("user", __name__, url_prefix="/api/user")


@blueprint.route('userinfo', methods=['GET'])
def userInfo():
    """登录函数"""
    # body = request.get_json()
    result = get_user_info()
    return json_response(**result)
