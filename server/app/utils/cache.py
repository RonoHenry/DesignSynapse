from redis import Redis
from typing import Any, Optional
import json
from functools import wraps
import os

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

# Initialize Redis client
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def cache_key_builder(*args, **kwargs) -> str:
    """Build a cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def cache(prefix: str, expire: int = 3600):
    """Cache decorator for functions/methods"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            cache_key = f"{prefix}:{cache_key_builder(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(
                cache_key,
                expire,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

def invalidate_cache(prefix: str, *patterns):
    """Invalidate cache entries matching the given patterns"""
    for pattern in patterns:
        keys = redis_client.keys(f"{prefix}:{pattern}")
        if keys:
            redis_client.delete(*keys)

class CacheManager:
    @staticmethod
    def get(key: str) -> Optional[str]:
        """Get value from cache"""
        return redis_client.get(key)
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 3600):
        """Set value in cache with expiration"""
        redis_client.setex(key, expire, json.dumps(value))
    
    @staticmethod
    def delete(key: str):
        """Delete value from cache"""
        redis_client.delete(key)
    
    @staticmethod
    def delete_pattern(pattern: str):
        """Delete all keys matching pattern"""
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
