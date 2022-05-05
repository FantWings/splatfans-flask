from flask import Blueprint
from utils.response import json_response
from functions.merchandises import Merchandises

blueprint = Blueprint("onlineshop", __name__)
cookie = dict(iksm_session="263fab071ccc7f0c21cd147196e844279c8c3d3a")


@blueprint.route("/merchandises.json", methods=["GET"])
def coop():
    """查询当前打工模式的时刻表"""
    data = Merchandises(cookie).get_list()
    return json_response(data)
