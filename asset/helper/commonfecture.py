model_name = "gemini-2.5-flash"


def get_next_sequence_value(sequence_name, counters_collection):
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
    
