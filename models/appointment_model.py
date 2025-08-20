from database import appointments_collection,doctors_collection
from bson import ObjectId
from datetime import datetime



def create_appointment(current_user,data):
    print(current_user)
    # Convert string IDs to ObjectId
    if "hospital_id" in data:
        data["hospital_id"] = ObjectId(data["hospital_id"])
    if "doctor_phone_id" in data:
        data["doctor_phone_id"] = ObjectId(data["doctor_phone_id"])
    if "_id" in current_user:
        data["user_id"] = ObjectId(current_user["_id"])
        data["whatsapp_number"] = current_user["phone"]

    data["created_at"] = datetime.utcnow()
    data["timestamp"] = datetime.utcnow()
    result = appointments_collection.insert_one(data)
    return str(result.inserted_id)

def get_appointment_by_id(appointment_id):
    appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
    if appointment:
        # doctor = doctors_collection.find_one({"_id": appointment["doctor_phone_id"]})
        # if doctor:
        #     appointment["doctor_name"] = doctor.get("name", "")
        #     appointment["doctor_speciality"] = doctor.get("speciality", "")
        appointment["_id"] = str(appointment["_id"])
        appointment["doctor_phone_id"] = str(appointment["doctor_phone_id"])
        appointment["user_id"] = str(appointment["user_id"])
        return appointment
    return None 

def update_appointment(appointment_id, updated_data):
    if "hospital_id" in updated_data:
        updated_data["hospital_id"] = ObjectId(updated_data["hospital_id"])
    if "doctor_id" in updated_data:
        updated_data["doctor_id"] = ObjectId(updated_data["doctor_id"])
    if "user_id" in updated_data:
        updated_data["user_id"] = ObjectId(updated_data["user_id"])

    result = appointments_collection.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": updated_data}
    )
    return result.modified_count > 0


def get_all_appointments(current_user):
    appointments = []
    user_id = current_user["_id"]

    # Admin can see all appointments
    if current_user.get("role") == "admin":
        for appt in appointments_collection.find():
            appt["_id"] = str(appt["_id"])
            appt["user_id"] = str(appt["user_id"])

            # Get doctor info (handle None case safely)
            doctor = doctors_collection.find_one({"_id": appt["doctor_phone_id"]})
            if doctor:
                appt["doctor_phone_id"] = str(doctor["_id"])
                appt["doctor_name"] = doctor.get("name", "")
                appt["doctor_speciality"] = doctor.get("speciality", "")
            else:
                appt["doctor_name"] = "Unknown"
                appt["doctor_speciality"] = "Unknown"

            appointments.append(appt)

    else:
        # Non-admin: return only appointments for that user
        for appt in appointments_collection.find({"user_id": user_id}):
            appt["_id"] = str(appt["_id"])
            appt["user_id"] = str(appt["user_id"])

            doctor = doctors_collection.find_one({"_id": appt["doctor_phone_id"]})
            if doctor:
                appt["doctor_phone_id"] = str(doctor["_id"])
                appt["doctor_name"] = doctor.get("name", "")
                appt["doctor_speciality"] = doctor.get("speciality", "")
            else:
                appt["doctor_name"] = "Unknown"
                appt["doctor_speciality"] = "Unknown"

            appointments.append(appt)

    return appointments
