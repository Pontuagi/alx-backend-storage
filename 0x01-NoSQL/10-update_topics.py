#!/usr/bin/env python3

"""
This module contains a python function update_topics
Pymongo collection
"""


def update_topics(mongo_collection, name, topics):
    """
    A function that changes all topics of a school documents based on the name

    mongo_collection: pymongo collection object
    name: school name to update
    topics: List of topics approached in the school
    """
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}
    result = mongo_collection.update_many(query, new_values)

    return result.modified_count
