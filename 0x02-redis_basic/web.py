#!/usr/bin/env python3

import requests
import redis
from functools import wraps

redis_client = redis.Redis()


def count_calls(fn):
    """
    Decorator to count method calls and increment a counter in Redis.

    Args:
    - method: The method to be decorated.

    Returns:
    - wrapper: The wrapper function that increments the call count.
    """
    @wraps(fn)
    def wrapper(url):
        """
        Wrapper function that caches HTTP requests and counts URL accesses.

        Args:
        - url: The URL to be accessed.

        Returns:
        - str: The response content from the URL if successful, an empty
        string otherwise.
        """
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        redis_client.expire(count_key, 10)

        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')

        try:
            result = fn(url)
            redis_client.setex(f"cached:{url}", 10, result)
            return result
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Function to retrieve HTML content of a URL and cache the result.

    Args:
    - url: The URL to fetch.

    Returns:
    - str: The HTML content fetched from the URL.
    """
    response = requests.get(url)
    return response.text
