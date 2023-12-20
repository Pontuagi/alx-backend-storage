#!/usr/bin/env python3

import requests
import redis
import functools


def count_calls(method):
    """
    Decorator to count method calls and increment a counter in Redis.

    Args:
    - method: The method to be decorated.

    Returns:
    - wrapper: The wrapper function that increments the call count.
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        """
        Wrapper function to count method calls and invoke the original method.

        Args:
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - The result returned by the original method.
        """
        url = args[0]
        count_key = f"count:{url}"
        r = redis.Redis()
        r.incr(count_key)
        r.expire(count_key, 10)  # Set expiration time of 10 seconds for count
        return method(*args, **kwargs)
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
