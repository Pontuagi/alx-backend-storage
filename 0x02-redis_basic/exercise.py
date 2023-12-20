#!/usr/bin/env python3

"""
This module contains a class Cache for implementing Redis in python
"""


import redis
import uuid
from typing import Union


class Cache:
    """
    A class that defines methods for writing to redis
    """
    def __init__(self):
        """ initializing the redis client """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Method to generate a random key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self,key: str, fn=None):
        """ Method to retrieve data from Redis with optional conversion"""
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str):
        """ Method to retrieve data from Redis and convert to string"""
        return self.get(key, fn=lambda d: d.decode("utf-8") if d else None)

    def get_int(self, key: str):
        """ Method to retrieve data from Redis and convert to integer"""
        return self.get(key, fn=int)


# Test Cases
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
