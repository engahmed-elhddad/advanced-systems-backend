import time

CACHE = {}
CACHE_TTL = 300  # 5 minutes

def get_cache(key):
    data = CACHE.get(key)
    if not data:
        return None

    value, timestamp = data

    if time.time() - timestamp > CACHE_TTL:
        del CACHE[key]
        return None

    return value


def set_cache(key, value):
    CACHE[key] = (value, time.time())