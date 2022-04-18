# from flask_cors import CORS
from flask import Flask
from config import FlaskConfig, DBConfig
from utils.database import db
from blueprints.bp_index import blueprint as index

# 这是FLASK主程序，除非开发用途，否则请考虑使用wsgi.py在生产环境进行启动，详情请查看wsgi.py
# 启动命令 flask run -h [监听IP地址:监听端口号]

app = Flask(__name__)
app.config.from_object(FlaskConfig)
app.config.from_object(DBConfig)
# CORS(app, supports_credentials=True)

with app.app_context():
    # 运行时初始化数据库
    db.init_app(app)
    # 创建数据库表
    db.create_all()

# 蓝图
app.register_blueprint(blueprint=index)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
