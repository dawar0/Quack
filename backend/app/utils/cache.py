import json
import pickle
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import redis
from flask import current_app, request


# Initialize Redis client
def get_redis_client(decode_responses=True):
    """
    Get Redis client instance using application configuration
    """
    app_config = current_app.config
    return redis.Redis(
        host=app_config.get("REDIS_HOST", "localhost"),
        port=app_config.get("REDIS_PORT", 6379),
        db=app_config.get("REDIS_CACHE_DB", 1),
        decode_responses=decode_responses,
    )


def get_default_expiration():
    """
    Get default expiration time from application configuration
    """
    return current_app.config.get("REDIS_DEFAULT_EXPIRATION", 3600)


def get_cache(key: str) -> Optional[str]:
    """
    Get a value from the cache
    """
    return get_redis_client().get(key)


def set_cache(key: str, value: str, expiration: int = None) -> bool:
    """
    Set a value in the cache with expiration in seconds (default from config)
    """
    if expiration is None:
        expiration = get_default_expiration()
    return get_redis_client().setex(key, expiration, value)


def delete_cache(key: str) -> bool:
    """
    Delete a value from the cache
    """
    return get_redis_client().delete(key) > 0


def delete_pattern(pattern: str) -> int:
    """
    Delete all keys matching a pattern
    """
    client = get_redis_client()
    keys = client.keys(pattern)
    if keys:
        return client.delete(*keys)
    return 0


def get_or_set_cache(key: str, callback: Callable, expiration: int = None) -> Any:
    """
    Get value from cache or set it if it doesn't exist
    """
    cached = get_cache(key)
    if cached is not None:
        return json.loads(cached)

    # Get fresh data from callback
    data = callback()

    # Cache the data
    if expiration is None:
        expiration = get_default_expiration()
    set_cache(key, json.dumps(data), expiration)

    return data


def cache_result(prefix: str, expiration: int = None, args_as_key: bool = False):
    """
    Decorator to cache function results

    Args:
        prefix: Prefix for the cache key
        expiration: Cache expiration time in seconds (default from config)
        args_as_key: Whether to include function arguments in the cache key
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a cache key
            if args_as_key and args:
                key_parts = [prefix, func.__name__] + [str(arg) for arg in args]
                key = ":".join(key_parts)
            else:
                key = f"{prefix}:{func.__name__}"

            # For API endpoints, add request path and query params to the key
            if request:
                query_string = request.query_string.decode("utf-8")
                if query_string:
                    key += f":{request.path}?{query_string}"
                else:
                    key += f":{request.path}"

            # Try to get from cache
            cached = get_cache(key)
            if cached is not None:
                return json.loads(cached)

            # Call the function
            result = func(*args, **kwargs)

            # Cache the result
            if expiration is None:
                exp = get_default_expiration()
            else:
                exp = expiration
            set_cache(key, json.dumps(result), exp)

            return result

        return wrapper

    return decorator


def cache_complex_object(key: str, obj: Any, expiration: int = None) -> bool:
    """
    Cache complex Python objects using pickle
    """
    if expiration is None:
        expiration = get_default_expiration()
    pickled_obj = pickle.dumps(obj)
    return get_redis_client(decode_responses=False).setex(key, expiration, pickled_obj)


def get_complex_object(key: str) -> Any:
    """
    Retrieve a complex object from cache
    """
    pickled_obj = get_redis_client(decode_responses=False).get(key)
    if pickled_obj:
        return pickle.loads(pickled_obj)
    return None
