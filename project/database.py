from datetime import datetime
import logging
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from response_parser import Report


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

database_url = os.getenv("DATABASE_URL")
database_cred_path = os.getenv("DATABASE_CRED_PATH")

logger.debug("database URL: %s", database_url)
logger.debug("database URL: %s", database_cred_path)

cred = credentials.Certificate(database_cred_path)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': database_url
})

# Reference reports to the root of your database
reports_ref = db.reference("/reports")  # Reference to Firebase database


def save_report(report: Report):
    new_data_ref = reports_ref.push({
        'id': report.user_id,
        'realtime': report.is_realtime,
        'timestamp_of_reporting': report.timestamp,
        'location': report.location,
        'description': report.description
    })




