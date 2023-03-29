import redis
from redis.exceptions import RedisError
import pickle


class Redis:
    def __init__(self):
        self._redis = redis.Redis(host='localhost', port=32768, password='redispw', db=0)

    # string
    def add_string(self, key, value, expire_time=None) -> bool:
        try:
            return self._redis.set(key, value, ex=expire_time)
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def select_string(self, key):
        try:
            result = self._redis.get(key)
            return result.decode('utf-8') if result else None
        except RedisError as e:
            print(f"Redis error: {e}")
            return None

    def update_string(self, key, value, expire_time=None) -> bool:
        try:
            if self._redis.exists(key):
                return self._redis.set(key, value, ex=expire_time)
            else:
                print(f"{key} do not exist")
                return False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def remove_string(self, key) -> bool:
        try:
            return True if self._redis.delete(key) > 0 else False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    # list
    def add_list(self, key, *values, expire_time=None) -> int:
        try:
            if expire_time:
                self._redis.expire(key, expire_time)
            for v in values:
                result = self._redis.rpush(key, pickle.dumps(v))
            return True if result >= len(values) else False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def select_list(self, key: str, index: int = None):
        try:
            if index is not None:
                return pickle.loads(self._redis.lindex(key, index))
            else:
                result = self._redis.lrange(key, 0, -1)
                return [pickle.loads(value) for value in result] if result else None
        except (RedisError, TypeError) as e:
            print(f"Redis error: {e}")
            return None
    
    def update_list(self, key, index, value, expire_time=None) -> bool:
        try:
            if expire_time:
                self._redis.expire(key, expire_time)
            return self._redis.lset(key, index, pickle.dumps(value))
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def remove_list(self, key, count:int = 0, value=None) -> bool:
        try:
            if value is None:
                return True if self._redis.delete(key) > 0 else False
            return True if self._redis.lrem(key, count, pickle.dumps(value)) > 0 else False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False
    
    # set - only support immutable objects(int, string, float, tuple)
    def add_set(self, key, *values, expire_time=None) -> bool:
        try:
            for v in values:
                result = self._redis.sadd(key, pickle.dumps(v))
            if expire_time:
                self._redis.expire(key, expire_time)
            return True if result > 0 else False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def select_set(self, key):
        try:
            result = self._redis.smembers(key)
            return {pickle.loads(value) for value in result} if result else None
        except (RedisError, TypeError) as e:
            print(f"Redis error: {e}")
            return None
    
    def remove_set(self, key, *values) -> bool:
        try:
            result = 0
            if values is None:
                return True if self._redis.delete(key) > 0 else False
            for v in values:
                result += self._redis.srem(key, pickle.dumps(v))
            return True if result == len(values) else False
        except RedisError as e:
            print(f"Redis error: {str(e)}")
            return False

    # hash
    def add_hash(self, name:str, key:str, mapping, expire_time=None) -> bool:
        try:
            result = self._redis.hset(name, key, pickle.dumps(mapping))
            if expire_time:
                self._redis.expire(name, expire_time)
            return True if result > 0 else False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def select_hash(self, name:str, key:str=None):
        try:
            if key is not None:
                return pickle.loads(self._redis.hget(name, key))
            else:
                return {k.decode('utf-8'): pickle.loads(v) for k, v in self._redis.hgetall(name).items()} 
        except (RedisError, TypeError) as e:
            print(f"Redis error: {e}")
            return None
    
    def update_hash(self, name, key, mapping, expire_time=None) -> bool:
        try:
            if self._redis.exists(name):
                self._redis.hset(name, key, pickle.dumps(mapping))
                if expire_time:
                    self._redis.expire(name, expire_time)
                return True if mapping == self.select_hash(name, key) else False
            else:
                print(f"{name} do not exist")
                return False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False

    def remove_hash(self, name, *keys) -> bool:
        try:
            if keys is None:
                return True if self._redis.delete(name) > 0 else False
            result = 0
            for k in keys:
                result += self._redis.hdel(name, k)
            return True if result == len(keys) else False
        except RedisError as e:
            print(f"Redis error: {e}")
            return False
