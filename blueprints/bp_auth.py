from flask import Blueprint, request
from utils.response import json_response
from crud.auth import userLogin, registerNewAccount, logoutUser

blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")


@blueprint.route('login', methods=['POST'])
def login():
    """登录函数"""
    body = request.get_json()
    result = userLogin(**body)
    return json_response(**result)


@blueprint.route('register', methods=['POST'])
def register():
    """注册函数"""
    body = request.get_json()
    result = registerNewAccount(**body)
    return json_response(**result)


@blueprint.route('logout', methods=['DELETE'])
def logout():
    """注销函数"""
    token = request.headers.get("token")
    result = logoutUser(token)
    return json_response(**result)
