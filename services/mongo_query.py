from pymongo import MongoClient
from datetime import datetime

# MongoDB setup (update credentials as needed)
client = MongoClient(" your mongouri")
db = client["test_db"]

# Known collections
VALID_COLLECTIONS = ["coal", "water", "local", "environment"]

def parse_mongo_filter(filter_dict):
    """
    Converts structured filter dict into a MongoDB-compatible filter.
    Supports timestamp (after/before), status_code, and flat fields.
    """
    mongo_filter = {}

    for key, value in filter_dict.items():
        if key == "timestamp":
            time_conditions = {}
            if isinstance(value, dict):
                if "after" in value:
                    try:
                        time_conditions["$gt"] = datetime.strptime(value["after"], "%Y-%m-%d")
                    except ValueError:
                        pass
                if "before" in value:
                    try:
                        time_conditions["$lt"] = datetime.strptime(value["before"], "%Y-%m-%d")
                    except ValueError:
                        pass
                if time_conditions:
                    mongo_filter["timestamp"] = time_conditions

        elif key == "status_code":
            if isinstance(value, list):
                mongo_filter["status_code"] = {"$in": value}
            else:
                mongo_filter["status_code"] = value

        else:
            # Treat other fields as exact match
            mongo_filter[key] = value

    return mongo_filter

def fetch_data_from_mongo(collection_names, filter_dict):
    """
    Queries one or more MongoDB collections using parsed filters.
    If collection_names is empty, use all known collections.
    """
    if not collection_names:
        collection_names = VALID_COLLECTIONS

    mongo_query = parse_mongo_filter(filter_dict)
    all_docs = []

    for name in collection_names:
        if name not in VALID_COLLECTIONS:
            continue  # skip unknown collections
        collection = db[name]
        docs = list(collection.find(mongo_query, {"_id": 0}))
        all_docs.extend(docs)

    return all_docs
