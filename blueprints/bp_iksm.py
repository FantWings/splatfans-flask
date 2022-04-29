from flask import Blueprint, request
from utils.response import json_response
from functions.iksm import (get_login_url, get_cookie, get_session_token,
                            unlink_account)

blueprint = Blueprint("iksm", __name__, url_prefix="/api/iksm")


@blueprint.route('login_url', methods=['GET'])
def login_url():
    """获取登录链接"""
    result = get_login_url()
    return json_response(**result)


@blueprint.route('session_token', methods=['POST'])
def add_session_token_code():
    """写入session_token"""
    body = request.get_json()
    result = get_session_token(**body)
    return json_response(**result)


@blueprint.route('cookie', methods=['GET'])
def add_session_cookie():
    """生成Cookie"""
    result = get_cookie()
    return json_response(**result)


@blueprint.route('unlink', methods=['DELETE'])
def do_unlink_account():
    """生成Cookie"""
    result = unlink_account()
    return json_response(**result)
