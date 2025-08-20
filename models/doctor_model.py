from bson import ObjectId
from datetime import datetime
from database import doctors_collection,onboarding_collection  # 👈 Import your database client

def create_doctor(data):
    data = dict(data)  # Make a mutable copy
    # Ensure hospital_id is stored as ObjectId
    if "hospital_id" in data:
        data["hospital_id"] = ObjectId(data["hospital_id"])
    if "user_id" in data:
        data["user_id"] = ObjectId(data["user_id"])
    data.pop("_id", None)

    data["created_at"] = datetime.utcnow()
    result = doctors_collection.insert_one(data)
    return str(result.inserted_id)

def get_doctor_by_id(doctor_id,type="user"):
    try:
        doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
        if doctor:
            doctor["_id"] = str(doctor["_id"])
            if 'user_id' in doctor:
                doctor['user_id']=str(doctor["user_id"])
            # doctor["hospital_id"] = str(doctor["hospital_id"])
            # Remove sensitive/unwanted fields
            if type == "user":
                doctor.pop("whatsAppBusinessAccountID", None)
                doctor.pop("accessToken", None)
                doctor.pop("password", None)
                doctor.pop("confirmPassword", None)
        return doctor
    except:
        return None
def get_doctor_by_user_id(phone):
    try:
        doctor = doctors_collection.find_one({"phone": phone})
        if doctor:
            doctor["_id"] = str(doctor["_id"])
            # doctor["user_id"] = str(doctor["user_id"])
            # doctor["hospital_id"] = str(doctor["hospital_id"])
            # Remove sensitive/unwanted fields
            doctor.pop("whatsAppBusinessAccountID", None)
            doctor.pop("accessToken", None)
            doctor.pop("password", None)
            doctor.pop("confirmPassword", None)
        return doctor
    except:
        return None
    
def get_onboarding_by_id(onboard_id):
    try:
        app = onboarding_collection.find_one({"_id": ObjectId(onboard_id)})
        if app:
            app["_id"] = str(app["_id"])
            # app["user_id"] = str(app["user_id"])
        return app
    except:
        return None
def get_onboarding_by_user_id(phone):
    try:
        app = onboarding_collection.find_one({"phone": phone})
        if app:
            app["_id"] = str(app["_id"])
            # app["user_id"] = str(app["user_id"])
        return app
    except:
        return None
    
def update_doctor(doctor_id, updated_data):
    if "hospital_id" in updated_data:
        updated_data["hospital_id"] = ObjectId(updated_data["hospital_id"])
    if "user_id" in updated_data:
        updated_data["user_id"] = ObjectId(updated_data["user_id"])
    print(updated_data)
    updated_data.pop("_id", None)
    result = doctors_collection.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": updated_data}
    )
    return result.modified_count > 0

def update_doctor_application(onboard_id, updated_data):
    print(updated_data)
    updated_data.pop("_id", None)
    result = onboarding_collection.update_one(
        {"_id": ObjectId(onboard_id)},
        {"$set": updated_data}
    )
    return result.modified_count > 0

def list_doctors():
    doctors = doctors_collection.find().sort("created_at", -1)
    doctor_list = []

    for doc in doctors:
        doc["_id"] = str(doc["_id"])
        if 'user_id' in doc:
            doc['user_id']=str(doc["user_id"])

        # Remove sensitive/unwanted fields
        doc.pop("whatsAppBusinessAccountID", None)
        doc.pop("accessToken", None)
        doc.pop("passsword", None)
        doc.pop("confirmPassword", None)

        doctor_list.append(doc)

    return doctor_list

def create_doctor_onboard(data):
    data = dict(data) 
    # data["user_id"] = ObjectId(current_user["_id"])
    data["created_at"] = datetime.utcnow()
    result = onboarding_collection.insert_one(data)
    return str(result.inserted_id)
# def create_doctor_onboard(data,current_user):
#     data = dict(data) 
#     data["user_id"] = ObjectId(current_user["_id"])
#     data["created_at"] = datetime.utcnow()
#     result = onboarding_collection.insert_one(data)
#     return str(result.inserted_id)

def application_list():
    appications = onboarding_collection.find().sort("created_at", -1)
    app_list = []

    for doc in appications:
        doc["_id"] = str(doc["_id"])
        if 'user_id' in doc:
            doc["user_id"] = str(doc["user_id"])
        app_list.append(doc)
    return app_list



