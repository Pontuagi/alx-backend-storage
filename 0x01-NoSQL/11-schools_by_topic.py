#!/usr/bin/env python3

"""
This module contains a python function school_by_topic(mongo_collection, topic)
pymongo collection object
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function that returns a list of school having a specific topic

    mongo_collection: Pymongo collection object
    topic: topic searched
    """
    query = {"topics": {"$in": [topic] }}
    schools_with_topic = list(mongo_collection.find(query))

    return schools_with_topic
