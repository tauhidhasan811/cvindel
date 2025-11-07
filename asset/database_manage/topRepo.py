import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from asset.helper.commonfecture import get_next_sequence_value


load_dotenv()
uri = os.getenv('MONGO_URI')


client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fashion_db"]
tops_collection = db["tops"]
counters_collection = db["counters"]




def insert_tops(data: dict, userid: int = 0):
    new_top_id = get_next_sequence_value(sequence_name="top_id", counters_collection=counters_collection)

    if new_top_id is None:
        print("Failed to generate an integer ID. Aborting insert.")
        return None

    try:
        record = {
            "_id": new_top_id,  
            "dress_id": data.get("drid"),
            "sleeve_type": data.get("sleeve_type"),
            "neck_type": data.get("neck_type"),
            "userid": userid
        }

        result = tops_collection.insert_one(record)
        
        print(f"Data inserted successfully with integer _id: {new_top_id}")
        return new_top_id
        
    except Exception as e:
        print("Error:", e)
        return None

def get_all_tops():
    data = []
    try:
        data = list(tops_collection.find())
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_topid(id: int): 
    data = None
    try:

        data = tops_collection.find_one({"_id": id}) 
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_userid(userid: int):
    data = []
    try:
        data = list(tops_collection.find({"userid": userid}))
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data
