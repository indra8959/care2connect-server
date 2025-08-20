# models/otp_model.py

from database import otp_collection
from datetime import datetime, timedelta
from config import OTP_EXPIRY_SECONDS

def store_otp(phone, otp_code):
    otp_entry = {
        "phone": phone,
        "otp": otp_code,
        "expires_at": datetime.utcnow() + timedelta(seconds=OTP_EXPIRY_SECONDS),
        "created_at": datetime.utcnow()
    }
    otp_collection.insert_one(otp_entry)

def verify_otp(phone, otp_code):
    record = otp_collection.find_one({"phone": phone, "otp": otp_code})
    if record and record["expires_at"] > datetime.utcnow():
        return True
    return False

def delete_otp(phone):
    otp_collection.delete_many({"phone": phone})