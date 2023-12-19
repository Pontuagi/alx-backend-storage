#!/usr/bin/python3

"""
This module contains a function list_all only
"""


def list_all(mongo_collection):
    # Python function that lists all documents in a collection

    # Find all documents in the collection
    all_documents = list(mongo_collection.find({}))

    return all_documents if all_documents else []
