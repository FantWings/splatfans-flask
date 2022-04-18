from flask import Blueprint
from utils.response import json_response
from functions.schedules import QuerySchedules

blueprint = Blueprint("index", __name__, url_prefix="/api/schedules")
cookie = dict(iksm_session="263fab071ccc7f0c21cd147196e844279c8c3d3a")


@blueprint.route("/battle", methods=["GET"])
def api_battle():
    """查询当前标准模式的时刻表"""
    data = QuerySchedules(cookie).query_battle()
    return json_response(data)


@blueprint.route("/coop", methods=["GET"])
def api_coop():
    """查询当前打工模式的时刻表"""
    data = QuerySchedules(cookie).query_coop()
    return json_response(data)
