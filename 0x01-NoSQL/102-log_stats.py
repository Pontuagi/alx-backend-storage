#!/usr/bin/env python3

"""
This module contains the improvement for 12-log_stats.py
"""


from pymongo import MongoClient


def log_stats():
    """
    Function that enhance the script 12-log_stats.py to display the top 10 most
    present IPs in the nginx collection of the logs database
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

    # Count IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip_info in top_ips:
        ip = ip_info["_id"]
        count = ip_info["count"]
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    log_stats()
