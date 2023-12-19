#!/usr/bin/env python3

"""
This module contains a script that provides some stats about Nginx logs
stored in MongoDB
"""


from pymongo import MongoClient


def nginx_log_stats():
    """
    This function returns stats about Ngixs logs stored in MongoDB
    """

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client.logs
    collection = db.nginx

    # Number of documents
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # specific query count
    specific_query_count = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{specific_query_count} status check")


if __name__ == "__main__":
    nginx_log_stats()
