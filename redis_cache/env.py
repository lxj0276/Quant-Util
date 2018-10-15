import redis

from redis_cache.cons import *


class GLOBAL_CONNECTION:
    c = None

    @classmethod
    def get_global_connection(cls):
        if cls.c is None:
            cls.c = redis.StrictRedis(host=HOST, port=PORT)
        return cls.c
