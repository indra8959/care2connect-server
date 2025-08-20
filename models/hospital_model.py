from bson import ObjectId
from datetime import datetime
from database import hospital_collection

def create_hospital(data):
    hospital_data = {
        **data,
        "created_at": datetime.utcnow()
    }
    result = hospital_collection.insert_one(hospital_data)
    return str(result.inserted_id)

def get_hospital_by_id(hospital_id):
    try:
        hospital = hospital_collection.find_one({"_id": ObjectId(hospital_id)})
        if hospital:
            hospital["_id"] = str(hospital["_id"])
        return hospital
    except:
        return None

def list_hospitals():
    hospitals = hospital_collection.find().sort("created_at", -1)
    return [{**doc, "_id": str(doc["_id"])} for doc in hospitals]
