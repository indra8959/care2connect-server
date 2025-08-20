from database import db
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from collections import Counter
from zoneinfo import ZoneInfo

doctors = db["doctors"] 
appointment = db["appointments"] 
templog = db["logs"] 
disableslot = db["disableslots"]

disableslot_collection = db["disableslots"]  # or whatever name you want

def insert_or_update_slot(slot_data):
    try:
        disableslot_collection.insert_one(slot_data)
    except:
        disableslot_collection.update_one({"_id": slot_data["_id"]}, {"$set": slot_data})
    return slot_data["_id"]

def get_all_disabled_slots():
    slots = list(disableslot_collection.find({}))
    for slot in slots:
        slot["_id"] = str(slot["_id"])
    return slots

 

def dateandtime(dt,doctor_id=None):
    if dt == 'date':
        doc_id = ObjectId(doctor_id)
        document = doctors.find_one({"_id": doc_id})
        datas = document
        def get_next_7_days():
            today = datetime.now(ZoneInfo("Asia/Kolkata"))
            dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(8)]
            return dates

        disabled_dates = get_next_7_days()

        data = datas.get('date', {}).get('disabledate', [])
        # data = datas['date']['disabledate']
        data_names = {item["name"] for item in data}
        formatted_output = [
            {"id": date, "title": date, "enabled": False} if date in data_names else {"id": date, "title": date}
            for date in disabled_dates
        ]

        current_time = datetime.now(ZoneInfo("Asia/Kolkata")).time()
        cutoff_time = datetime.strptime("08:30AM", "%I:%M%p").time()

        if current_time >= cutoff_time and data:
            formatted_output.pop(0)

        return formatted_output

    else:
        doc_id = ObjectId(doctor_id)
        document = doctors.find_one({"_id": doc_id})
        datas = document

        appoint_cursor = appointment.find(
        {
            "doctor_phone_id": doctor_id,
            "date_of_appointment": dt,
            "amount": {"$gt": -1}
        },
        {"_id": 0}
        )
        appoint = list(appoint_cursor)  

        if appoint:
            time_slots = [entry['time_slot'] for entry in appoint]
            time_counts = Counter(time_slots)
            result = [{"time": time, "number": count} for time, count in time_counts.items()]
            xslot = datas.get('slots', {}).get('slotsvalue', [])
            # xslot = datas['slots']['slotsvalue']

            formatted_output = [
                {
                    "id": datetime.strptime(item["slot"]["stime"], "%H:%M").strftime("%I:%M %p") + " - " + datetime.strptime(item["slot"]["etime"], "%H:%M").strftime("%I:%M %p"),
                    "title": datetime.strptime(item["slot"]["stime"], "%H:%M").strftime("%I:%M %p") + " - " + datetime.strptime(item["slot"]["etime"], "%H:%M").strftime("%I:%M %p"),
                    "maxno": item["maxno"]
                }
                for item in xslot
            ]

            time_counts = {item['time']: item['number'] for item in result}
            result = [
                {
                    "id": item['id'],
                    "title": item['title'],
                    "enabled": False if time_counts.get(item['title'], 0) >= int(item['maxno']) else True
                }
                for item in formatted_output
            ]

            for obj in result:
                if obj["enabled"]:
                    del obj["enabled"]

            documentsst = list(disableslot.find({'date': dt}))

            if not documentsst:  
                disabled_set = set()   # No documents found, so no disabled slots  
            else:
                disabled_set = {item["slot"] for item in documentsst if not item.get("enable", True)}

            updated_slots = []
            for slot in result:
                if slot["id"] in disabled_set:
                    updated_slots.append({**slot, "enabled": False})
                else:
                    updated_slots.append(slot)

            return updated_slots

        else:
            xslot = datas.get('slots', {}).get('slotsvalue', [])
            formatted_output = [
                {
                    "id": datetime.strptime(item["slot"]["stime"], "%H:%M").strftime("%I:%M %p") + " - " + datetime.strptime(item["slot"]["etime"], "%H:%M").strftime("%I:%M %p"),
                    "title": datetime.strptime(item["slot"]["stime"], "%H:%M").strftime("%I:%M %p") + " - " + datetime.strptime(item["slot"]["etime"], "%H:%M").strftime("%I:%M %p")
                }
                for item in xslot
            ]

            documentsst = list(disableslot.find({'date': dt}))
            disabled_set = {item["slot"] for item in documentsst if not item["enable"]}
            updated_slots = []
            for slot in formatted_output:
                if slot["id"] in disabled_set:
                    updated_slots.append({**slot, "enabled": False})
                else:
                    updated_slots.append(slot)

            return updated_slots

