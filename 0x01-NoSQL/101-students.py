#!/usr/bin/env python3

"""
This module contains a function top_students(mongo_collection)
pymongo
"""


def top_students(mongo_collection):
    """
    A function that returns all students sorted bu average score

    mongo_collection: pymongo collection object
    """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]

    top_students = list(mongo_collection.aggregate(pipeline))

    return top_students
