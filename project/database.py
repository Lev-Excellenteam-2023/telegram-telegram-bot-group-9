import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase
firebase_cred = credentials.Certificate("path/to/your/firebase-credentials.json")
firebase_admin.initialize_app(firebase_cred, {"databaseURL": "your-firebase-database-url"})
firebase_ref = db.reference("/messages")  # Reference to Firebase database

# Save user message to the database
def save_user_message(user_id, message):
    firebase_ref.child(user_id).push({"user": message})

# Save bot response to the database
def save_bot_response(user_id, response):
    firebase_ref.child(user_id).push({"bot": response})
