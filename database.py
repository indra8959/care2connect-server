# database.py

from pymongo import MongoClient
from config import MONGO_URI
import gridfs


client = MongoClient(MONGO_URI)
db = client["care2connect"] # If URI has a DB, it picks it
fs = gridfs.GridFS(db) 

# Collections we'll use
users_collection = db['users']
otp_collection = db['otp_verifications']
hospital_collection = db['hospitals']
appointments_collection = db["appointments"]
doctors_collection = db["doctors"]
onboarding_collection = db["onboarding"]
