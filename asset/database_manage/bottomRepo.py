import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#from bson import ObjectId
from asset.helper.commonfecture import get_next_sequence_value
from dotenv import load_dotenv

#uri = "mongodb+srv://tauhidhasanslu_db_user:jgay7RLJLZI9FNcF@cvindel.9ndye01.mongodb.net/fashion_db?retryWrites=true&w=majority"
load_dotenv()
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fashion_db"]
bottoms_collection = db["bottoms"]
counters_collection = db["counters"]
'''
def get_next_sequence_value(sequence_name):
    try:
        sequence_document = counters_collection.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=True 
        )
        return sequence_document.get('sequence_value')
    except Exception as e:
        print(f"Error getting next sequence value: {e}")
        return None
'''
def insert_bottoms(data: dict, fit_type='slim-fit', userid: int = 0):
    new_bottom_id = get_next_sequence_value(sequence_name="bottom_id", counters_collection=counters_collection)

    if new_bottom_id is None:
        print("Failed to generate an integer ID. Aborting insert.")
        return None

    try:
        record = {
            "_id": new_bottom_id, 
            "dress_id": data.get("drid"),
            "length": data.get("length"),
            "waist_type": data.get("waist_type"),
            "fit_type": fit_type,
            "userid": userid
        }
        
        result = bottoms_collection.insert_one(record)
        
        print(f"Data inserted successfully with integer _id: {new_bottom_id}")
        return new_bottom_id
        
    except Exception as e:
        print("Error inserting data:", e)
        return None

def get_all_bottoms():
    try:
        bottoms = list(bottoms_collection.find())
        print(f"Retrieved {len(bottoms)} records successfully!")
        return bottoms
    except Exception as e:
        print("Error retrieving data:", e)
        return []

def get_by_bottomid(id: int): 
    try:
        bottom = bottoms_collection.find_one({"_id": id}) 
        if bottom:
            print("Data retrieved successfully!")
        else:
            print("No data found for this ID.")
        return bottom
    except Exception as e:
        print("Error retrieving by ID:", e)
        return None

def get_by_userid(userid: int):
    try:
        bottoms = list(bottoms_collection.find({"userid": userid}))
        print(f"Retrieved {len(bottoms)} records for user {userid}")
        return bottoms
    except Exception as e:
        print("Error retrieving by user ID:", e)
        return []