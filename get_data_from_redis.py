import redis

if __name__ == '__main__':
    redis_db = redis.StrictRedis()
    print(redis_db.lrange('resolvers', 0, -1))
