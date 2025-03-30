from typing import Dict, List, Optional, Tuple
from flask import current_app
from .cache import get_redis_client


def get_cache_stats() -> Dict[str, int]:
    client = get_redis_client()
    info = client.info()
    stats = {
        "total_keys": client.dbsize(),
        "used_memory_human": info.get("used_memory_human", ""),
        "connected_clients": info.get("connected_clients", 0),
        "uptime_in_days": info.get("uptime_in_days", 0),
    }
    return stats


def list_cache_keys(pattern: str = "*") -> List[str]:
    client = get_redis_client()
    return client.keys(pattern)


def get_key_info(key: str) -> Dict[str, str]:
    client = get_redis_client()
    ttl = client.ttl(key)

    info = {
        "key": key,
        "ttl": (
            str(ttl) + " seconds"
            if ttl > 0
            else "No expiration" if ttl == -1 else "Key does not exist"
        ),
        "type": (
            client.type(key).decode("utf-8") if client.exists(key) else "Does not exist"
        ),
    }

    # Add extra info based on type
    if info["type"] == "string" and client.exists(key):
        info["size"] = str(len(client.get(key) or "")) + " bytes"

    return info


def clear_cache(pattern: str = "*") -> int:
    client = get_redis_client()
    keys = client.keys(pattern)
    if keys:
        return client.delete(*keys)
    return 0


def get_cache_usage_by_prefix() -> List[Dict[str, any]]:
    client = get_redis_client()
    all_keys = client.keys("*")

    # Group keys by prefix
    prefix_groups = {}
    for key in all_keys:
        # Extract prefix (everything before the first colon)
        parts = key.split(":")
        prefix = parts[0] if parts else key

        if prefix not in prefix_groups:
            prefix_groups[prefix] = []
        prefix_groups[prefix].append(key)

    # Calculate stats for each prefix
    result = []
    for prefix, keys in prefix_groups.items():
        result.append(
            {
                "prefix": prefix,
                "count": len(keys),
                "examples": keys[:3],  # First 3 examples
            }
        )

    # Sort by count (descending)
    result.sort(key=lambda x: x["count"], reverse=True)

    return result


def renew_cache_ttl(key: str, new_ttl: int) -> bool:
    client = get_redis_client()
    if client.exists(key):
        return client.expire(key, new_ttl)
    return False
