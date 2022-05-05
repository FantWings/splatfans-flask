from flask import Blueprint
from utils.response import json_response
from functions.schedules import Schedules

blueprint = Blueprint("schedules", __name__)
cookie = dict(iksm_session="263fab071ccc7f0c21cd147196e844279c8c3d3a")


@blueprint.route("/battle.json", methods=["GET"])
def battle():
    """查询当前标准模式的时刻表"""
    data = Schedules(cookie).battle()
    return json_response(data)


@blueprint.route("/coop.json", methods=["GET"])
def coop():
    """查询当前打工模式的时刻表"""
    data = Schedules(cookie).coop()
    return json_response(data)
