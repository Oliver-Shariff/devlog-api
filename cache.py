import os
import time
import threading
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

USE_REDIS = False
redis_client = None

# Attempt import + connection
try:
    import redis
    redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

    # Try pinging Redis
    try:
        redis_client.ping()
        USE_REDIS = True
        print("Redis connected successfully.")
    except redis.exceptions.ConnectionError:
        print("Redis server not reachable. Falling back to in-memory cache.")
        USE_REDIS = False

except ImportError:
    print("Redis library not installed. Using in-memory fallback.")
    USE_REDIS = False

class CacheBackend:
    """Unified interface for any cache backend (Redis or in-memory)."""

    def get(self, key: str):
        """Return value for key, or None if not present."""
        raise NotImplementedError

    def set(self, key: str, value: str, ttl: int):
        """Set value with TTL (in seconds)."""
        raise NotImplementedError

    def delete(self, key: str):
        """Delete a key from the cache."""
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        """Return whether the key exists."""
        raise NotImplementedError

class RedisCache(CacheBackend):
    def __init__(self,client):
        self.client = client

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value: str, ttl: int):
        self.client.set(key, value, ex=ttl)

    def delete(self, key: str):
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) == 1

class MemoryTTLCache(CacheBackend):
    
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def _purge_expired(self):
        """ Remove expired items"""
        now = time.time()
        expired_keys = []

        for key, (_, expire_at) in self.store.items():
            if expire_at is not None and expire_at < now:
                expired_keys.append(key)

        for key in expired_keys:
            del self.store[key]

        def get(self,key: str):
            with self.lock:
                self._purge_expired()

                if key not in self.store:
                    return None

                value, expire_at = self.store[key]

                if expire_at is not None and expire_at < time.time():
                    del self.store[key]
                    return None
                
                return value
    def set(self, key: str, value: str, ttl: int):
        expire_at = time.time() + ttl if ttl is not None else None

        with self.lock:
            self.store[key] = (value, expire_at)

    def delete (self, key: str):
        with self.lock:
            if key in self.store:
                del self.store[key]

    def exists(self,key:str):
        with self.lock:
            self._purge_expired()
            return key in self.store

if USE_REDIS:
    cache = RedisCache(redis_client)
else:
    cache = MemoryTTLCache()