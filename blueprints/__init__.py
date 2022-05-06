from flask import Blueprint
from utils.database import session

from .bp_schedules import blueprint as schedules
from .bp_onlineshop import blueprint as onlineshop
from .bp_auth import blueprint as auth
from .bp_user import blueprint as user
from .bp_iksm import blueprint as iksm

blueprint = Blueprint('index', __name__)


@blueprint.teardown_request
def proccess(error):
    if error:
        print(error)
    session.close()


# 蓝图
blueprint.register_blueprint(schedules, url_prefix="/schedules")
blueprint.register_blueprint(onlineshop, url_prefix="/onlineshop")
blueprint.register_blueprint(auth, url_prefix="/auth")
blueprint.register_blueprint(user, url_prefix="/user")
blueprint.register_blueprint(iksm, url_prefix="/iksm")
