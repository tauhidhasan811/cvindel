import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from asset.helper.commonfecture import get_next_sequence_value
load_dotenv()
uri = os.getenv('MONGO_URI')

client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fashion_db"]
users_collection = db["users"]
counters_collection = db["counters"]


def insert_user(data: dict):

    new_user_id = get_next_sequence_value(sequence_name = "user_id", counters_collection=counters_collection) 

    if new_user_id is None:
        print("Failed to generate an integer ID. Aborting insert.")
        return None

    try:
        record = {
            "_id": new_user_id, 
            "age": data.get("age"),
            "gender": data.get("gender"),
            "skin_tone": data.get("skin_tone"),
            "image": data.get("image"),
            "race": data.get("race")
        }
        
        result = users_collection.insert_one(record)
        
        print(f"Data inserted successfully with ID: {new_user_id}!")
        return record
        
    except Exception as e:
        print("Error:", e)
        return None


def get_all_user():
    data = []
    try:
        data = list(users_collection.find())
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_userinfo(userid: int): 
    data = None
    try:
        data = users_collection.find_one({"_id": userid})
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data
