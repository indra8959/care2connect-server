# auth/utils.py

import random
import requests
from config import WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID

def generate_otp(length=6):
    """Generate a random numeric OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_otp_via_whatsapp(phone, otp_code):
    """
    Sends OTP to the given phone number using WhatsApp Cloud API.
    Assumes you have a message template with 1 variable (for OTP).
    """

    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = { 
        "messaging_product": "whatsapp", 
        "to": phone,
        "type": "template", 
        "template": { 
            "name": "otp_care2connect", 
            "language": { 
                "code": "en" 
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        { "type": "text", "text": otp_code }
                    ]
                },
                {
                "type": "button",
                "index": "0",
                "sub_type": "url",
                "parameters": [
                    {
                        "type": "text",
                        "text": otp_code
                    }
                ]}
            ]} 
        }

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    return response.status_code == 200
