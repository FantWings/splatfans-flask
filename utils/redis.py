import redis
from flask import current_app

###################################################
#           Redis SDK For Python Flask            #
#        for more infomation please visit:        #
#   https://github.com/FantWings/flask-redis_sdk  #
###################################################


class Redis(object):

    @staticmethod
    def _get_r():
        host = current_app.config["REDIS_HOST"]
        port = current_app.config["REDIS_PORT"]
        db = current_app.config["REDIS_DB"]
        r = redis.StrictRedis(host, port, db)
        return r

    @classmethod
    def write(cls, key, value=None, expire=None):
        r = cls._get_r()
        expire_in_seconds = int(current_app.config["REDIS_SESSION_TIMELIFE"])
        r.set(key, value, ex=expire or expire_in_seconds)

    @classmethod
    def read(cls, key):
        r = cls._get_r()
        value = r.get(key)
        return value.decode("utf-8") if value else value

    @classmethod
    def hset(cls, name, key, value):
        r = cls._get_r()
        r.hset(name, key, value)

    @classmethod
    def hmset(cls, key, *value):
        r = cls._get_r()
        value = r.hmset(key, *value)
        return value

    @classmethod
    def hget(cls, name, key):
        r = cls._get_r()
        value = r.hget(name, key)
        return value.decode("utf-8") if value else value

    @classmethod
    def hgetall(cls, name):
        r = cls._get_r()
        return r.hgetall(name)

    @classmethod
    def delete(cls, *names):
        r = cls._get_r()
        r.delete(*names)

    @classmethod
    def hdel(cls, name, key):
        r = cls._get_r()
        r.hdel(name, key)

    @classmethod
    def expire(cls, name, expire=None):
        r = cls._get_r()
        expire_in_seconds = int(current_app.config["REDIS_SESSION_TIMELIFE"])
        r.expire(name, expire or expire_in_seconds)
