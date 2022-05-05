from os import path, urandom, getenv


class FlaskConfig(object):
    """FLASK配置"""
    # 安全密钥（随机生成）
    SECRET_KEY = urandom(24)


class RedisConfig(object):
    """Redis配置"""
    REDIS_HOST = getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = getenv("REDIS_PORT", "6379")
    REDIS_DB = getenv("REDIS_DB", "0")
    REDIS_SESSION_TIMELIFE = getenv("REDIS_SESSION_TIMELIFE", "172800")


class DBConfig(object):
    """数据库配置"""
    # 设置每次请求结束后会自动提交数据库中的改动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 如果设置为True，Flask-SQLAlchemy将跟踪对象的修改并发出信号。默认值为None
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 设置线程池最大链接时长（秒）
    SQLALCHEMY_POOL_RECYCLE = 1800

    if getenv("SQL_ENGINE", "sqlite") == "mysql":
        # 使用MySQL数据库
        SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s" % (
            getenv("SQL_USER", "root"),
            getenv("SQL_PASS", ""),
            getenv("SQL_HOST", "127.0.0.1"),
            getenv("SQL_PORT", "3306"),
            getenv("SQL_BASE", "BaseName"),
        )
    else:
        # 使用SQLite数据库
        base_dir = path.abspath(path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
            base_dir, "sqlite.db")


class SMTPFlask(object):
    """ SMTP配置 """
    SMTP_USER = getenv("SMTP_USER", "noreply@yourdomain.com")
    SMTP_PASS = getenv("SMTP_PASS", "SUPERPASSWD")
    SMTP_HOST = getenv("SMTP_HOST", "smtp.example.com")
    SMTP_PORT = getenv("SMTP_PORT", "465")
