import redis

def createConnect():
    return redis.Redis(host='127.0.0.1', port=6379)