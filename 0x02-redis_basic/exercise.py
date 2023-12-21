#!/usr/bin/env python3

"""
This module contains a class Cache for implementing Redis in python
"""


import redis
import uuid
import functools
import inspect
from typing import Union


def count_calls(method):
    """
    Decorator to count method calls and increment a counter in Redis.

    Args:
    - method: The method to be decorated.

    Returns:
    - wrapper: The wrapper function that increments the call count.
    """
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls and invoke the original method.

        Args:
        - self: The instance of the class.
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - The result returned by the original method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method):
    """
    Decorator to store the history of inputs and outputs for function in Redis

    Args:
    - method: The method to be decorated.

    Returns:
    - wrapper: The wrapper function that stores input and output history.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history in Redis.

        Args:
        - self: The instance of the class.
        - *args: Positional arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - The result returned by the original method.
        """
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        # Store input arguments in Redis as strings
        self._redis.rpush(inputs_key, str(args))

        # Execute the original method to get the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


def replay(redis_instance, method):
    """
    Function to display the history of calls for a particular function.

    Args:
    - redis_instance: Redis instance.
    - method: The qualified name of the method.

    Returns:
    - List of tuples representing inputs and outputs.
    """
    key = method.__qualname__
    inputs_key = f"{key}:inputs"
    outputs_key = f"{key}:outputs"

    # Get the number of calls made for the specified method
    num_calls = cache._redis.llen(inputs_key)

    print(f"{key} was called {num_calls} times:")

    # Retrieve inputs and outputs from Redis and display them
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        input_str = eval(input_data.decode()) if isinstance(
            input_data, bytes
            ) else input_data.decode()
        output_str = output_data.decode() if isinstance(
            output_data, bytes) else output_data
        print(f"{key}{input_str} -> {output_str}")


class Cache:
    """
    A class that defines methods for writing to redis
    """
    def __init__(self):
        """ initializing the redis client """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Method to generate a random key"""
        key = str(uuid.uuid4())
        if not self._redis.exists(key):
            self._redis.set(key, data)
            return key

    def get(self, key: str, fn=None) -> Union[str, bytes, int, float]:
        """ Method to retrieve data from Redis with optional conversion"""
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """ Method to retrieve data from Redis and convert to string"""
        return self.get(key, fn=lambda d: d.decode("utf-8") if d else None)

    def get_int(self, key: str) -> int:
        """ Method to retrieve data from Redis and convert to integer"""
        return self.get(key, fn=int)
