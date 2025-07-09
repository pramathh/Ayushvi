import csv
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

# Initialize Firebase using JSON stored in env variable
firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
firebase_json = firebase_json.replace('\\n', '\n')
cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Twilio credentials
account_sid = os.getenv("ACCOUNT_SID") or "AC508185bf8a1709823760e885d45ab0ec"
auth_token = os.getenv("AUTH_TOKEN") or "0a5acdab43730175c40ac99242a27a30"
client = Client(account_sid, auth_token)

def load_messages_from_csv(filepath):
    messages = {}
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            messages[int(row['day'])] = row['message']
    return messages

def get_day_index(start_date):
    today = datetime.today().date()
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    return (today - start).days + 1

def fetch_users_from_firestore():
    users_ref = db.collection("users")
    docs = users_ref.stream()
    return [doc.to_dict() for doc in docs]

def send_messages_to_users(users, messages):
    for user in users:
        phone = f"whatsapp:{user['phone']}"
        day = get_day_index(user['start_date'])

        if day in messages:
            body = messages[day]
            try:
                client.messages.create(
                    from_='whatsapp:+14155238886',
                    to=phone,
                    body=body
                )
                print(f"[OK] Sent Day {day} to {user['phone']}: {body}")
            except Exception as e:
                print(f"[ERROR] Failed to send to {user['phone']}: {e}")
        else:
            print(f"[INFO] No message for Day {day} (user: {user['phone']})")

if __name__ == "__main__":
    messages = load_messages_from_csv("messages.csv")
    users = fetch_users_from_firestore()
    send_messages_to_users(users, messages)
