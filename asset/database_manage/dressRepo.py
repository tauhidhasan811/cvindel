import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from asset.helper.commonfecture import get_next_sequence_value

load_dotenv()

uri = os.getenv('MONGO_URI')

client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fashion_db"]
dresses_collection = db["dresses"]
tops_collection = db["tops"]
bottoms_collection = db["bottoms"]
shoes_collection = db["shoes"]
counters_collection = db["counters"]


def insert_dress(data: dict, id=True):

    new_dress_id = get_next_sequence_value(sequence_name="dress_id", counters_collection=counters_collection)

    if new_dress_id is None:
        print("Failed to generate an integer ID. Aborting insert.")
        return None
        
    try:
        record = {
            "_id": new_dress_id, 
            "type": data["type"],
            "color": data["color"],
            "pattern": data["pattern"],
            "material": data["material"],
            "fit": data["fit"],
            "season": data["season"],
            "preference": data["preference"],
            "style": data["style"],
            "image": data["image"],
            "features": data["features"],
            "uid": data["uid"],
            "category": data["category"]
        }

        result = dresses_collection.insert_one(record)
        
        print(f"Data inserted successfully with integer _id: {new_dress_id}")
        
    except Exception as e:
        print("Error:", e)
        return None
        
    if id:
        return new_dress_id 

def get_all():
    data = []
    try:
        data = list(dresses_collection.find())
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_dressid(id: int):
    data = None
    allowed = ["tops", "bottoms", "shoes"]
    try:
        dress = dresses_collection.find_one({"_id": id})
        
        if not dress:
            return None
            
        category = dress.get("category")
        if category in allowed:
            related_collection = db[category]
            related = related_collection.find_one({"dress_id": str(dress["_id"])}) 
            if related:
                data = {**dress, **related}
            else:
                data = dress
        else:
            data = dress
            
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_userid(userid: int):
    data = []
    try:
        data = list(dresses_collection.find({"uid": userid}))
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_dress_by_user_id(userid: int, dressid: int, category):
    data = []
    try:
        d = dresses_collection.find_one({"_id": dressid, "uid": userid})
        
        if not d:
            return []
        related = list(db[category].find({"dress_id": str(d["_id"])})) 
        
        if related:
            for r in related:
                data.append({**d, **r})
        else:
            data.append(d)
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_by_catergory(category):
    data = []
    try:
        dresses = list(dresses_collection.find({"category": category}))
        related_collection = db[category] if category in ["tops", "bottoms", "shoes"] else None
        
        if related_collection:
            for d in dresses:
                related = related_collection.find_one({"dress_id": str(d["_id"])}) 
                if related:
                    data.append({**d, **related})
                else:
                    data.append(d)
        else:
            data = dresses
            
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data

def get_user_dress_by_category(userid: int, category):
    data = []
    try:
        if category not in ["tops", "bottoms", "shoes"]:
            data = list(dresses_collection.find({"uid": userid, "category": category}))
        else:
            dresses = list(dresses_collection.find({"uid": userid}))
            for d in dresses:
                related = db[category].find_one({"dress_id": str(d["_id"])}) 
                if related:
                    item = {}
                    for k, v in {**d, **related}.items():
                        if "id" not in k or "category" not in k: 
                             item[k] = v
                    data.append(item)
                    
        print("Data retrieved successfully!")
    except Exception as e:
        print("Error:", e)
    return data