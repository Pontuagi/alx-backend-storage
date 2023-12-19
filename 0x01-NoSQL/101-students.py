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
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "scores": 1,
                "averageScore": { "$avg": "$scores.score" }
            }
        },
        { "$sort": { "averageScore": -1 } }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))

    return top_students
