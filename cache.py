import os
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
    """Will be implemented in the next step."""
    pass

if USE_REDIS:
    cache = RedisCache(redis_client)
else:
    cache = MemoryTTLCache()