#!/usr/bin/env python3

"""
This module contains a python function insert_school
pymongo
"""


def insert_school(mongo_collection, **kwargs):
    """
    A python function that inserts a new document in a collection
    based on kwargs
    """
    new_doc = kwargs
    result = mongo_collection.insert_one(new_doc)

    return result.inserted_id
