from redis import Redis
from typing import Optional, Any
import json
import os
import pickle
from datetime import timedelta

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Cache TTL defaults
DEFAULT_CACHE_TTL = timedelta(minutes=15)
LONG_CACHE_TTL = timedelta(hours=24)

class RedisCache:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True  # Automatically decode responses to Python strings
            )
        return cls._instance

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[timedelta] = DEFAULT_CACHE_TTL) -> bool:
        """Set value in cache with optional TTL"""
        try:
            return self.client.set(
                key,
                json.dumps(value),
                ex=int(ttl.total_seconds()) if ttl else None
            )
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    def invalidate_pattern(self, pattern: str) -> bool:
        """Invalidate all keys matching pattern"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                return bool(self.client.delete(*keys))
            return True
        except Exception as e:
            print(f"Redis pattern invalidation error: {e}")
            return False

# Cache key patterns
USER_KEY_PATTERN = "user:{user_id}"
PROJECT_KEY_PATTERN = "project:{project_id}"
PRODUCT_KEY_PATTERN = "product:{product_id}"
USER_PROJECTS_KEY_PATTERN = "user:{user_id}:projects"

# Cache instance
cache = RedisCache()
