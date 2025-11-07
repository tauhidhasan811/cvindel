import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from asset.helper.commonfecture import get_next_sequence_value

load_dotenv()
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fashion_db"]
shoes_collection = db["shoes"]
counters_collection = db["counters"]


def insert_shoes(data: dict, userid: int = 0):

    new_shoe_id = get_next_sequence_value(sequence_name="shoe_id", counters_collection=counters_collection)

    if new_shoe_id is None:
        print("Failed to generate an integer ID. Aborting insert.")
        return None

    try:
        record = {
            "_id": new_shoe_id,  
            "dress_id": data.get("drid"),
            "closure": data.get("closure"),
            "heel_height": data.get("heel_height"),
            "sole_type": data.get("sole_type"),
            "userid": userid
        }
        
        result = shoes_collection.insert_one(record)
        
        print(f"Data inserted successfully with integer _id: {new_shoe_id}")
        return new_shoe_id
        
    except Exception as e:
        print("Error:", e)
        return None

def get_all_shoes():
    data = []
    try:
        data = list(shoes_collection.find())
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_shoeid(id: int): 
    data = None
    try:
        data = shoes_collection.find_one({"_id": id}) 
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_userid(userid: int):
    data = []
    try:
        data = list(shoes_collection.find({"userid": userid}))
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data