from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from response_parser import Report
from consts import DATABASE_URL, DATABASE_CRED_PATH

cred = credentials.Certificate(DATABASE_CRED_PATH)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL
})

# Reference reports to the root of your database
reports_ref = db.reference("/reports")  # Reference to Firebase database


def save_report(report: Report):
    new_data_ref = reports_ref.push({
        'id': report.user_id,
        'realtime': report.is_realtime,
        'location': report.location,
        'description': report.description
    })


