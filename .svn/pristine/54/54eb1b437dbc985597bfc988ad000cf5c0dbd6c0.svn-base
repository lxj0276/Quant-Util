import hashlib
from redis_cache.env import GLOBAL_CONNECTION
def hash_args(*args, **kwargs):
    string = ''.join(sorted(str(x) for x in args)) + ''.join(sorted(str(x) for x in kwargs.items()))
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def flush():
    GLOBAL_CONNECTION.get_global_connection().flushall()
