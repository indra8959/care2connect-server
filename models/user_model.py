# models/user_model.py

from database import users_collection
from bson.objectid import ObjectId
from datetime import datetime

def find_user_by_phone(phone):
    return users_collection.find_one({"phone": phone})

def verify_password(email,password):
    user=users_collection.find_one({"email": email})
    if user and user.get('password')==password:
        return user
    else:
        return None
    
def verify_user_password(phone,password):
    user=users_collection.find_one({"phone": phone})
    if user and user.get('password')==password:
        return user
    else:
        return None

def create_user(phone,name,data):
    user = {
        **data,
        "phone": phone,
        "name": name,
        "is_verified": True,
        "created_at": datetime.utcnow()
    }
    return users_collection.insert_one(user)

def complete_user_profile(user_id, data):
    print(data)
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    print(result.modified_count)
    return result.modified_count > 0


def get_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})
