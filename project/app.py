import datetime
import os
import logging
from response_parser import Report
import requests
from flask import Flask, request, Response
from dotenv import load_dotenv
from database import save_report


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram Bot API
telegram_token = os.getenv("TELEGRAM_TOKEN")
webhook_url = os.getenv("WEBHOOK_URL")
requests.get(webhook_url)

logger.debug("Telegram Token: %s", telegram_token)
logger.debug("Webhook URL: %s", webhook_url)

# Create an app
app = Flask(__name__)


# Create a /sanity route
@app.route('/sanity')
def sanity_check():
    return 'Server is running'


# Create a /message route to handle incoming messages
@app.route('/message', methods=["POST"])
def handle_message():
    data = request.json
    chat_id = data['message']['chat']['id']
    #message_text = data['message']['text']
    #logger.debug("Received a message from Telegram: %s", message_text)


    if 'text' in data['message']:
        message_text = data['message']['text']
        logger.debug("Received a text message from Telegram: %s", message_text)
        if message_text.startswith('/start'):
            response_text = "Welcome to the Agricultural Crime Reporting Bot! Please choose an option:"
            send_response_with_keyboard(chat_id, response_text, ["report/"])

        elif message_text == "report/":
            response_text = "Please send the location of the incident where you saw the crime. You can use the GPS location feature."
            send_response(chat_id, response_text)

        else:
            response_text = "Got it."
            send_response(chat_id, response_text)

    elif 'location' in data['message']:
        location = data['message']['location']
        latitude = location['latitude']
        longitude = location['longitude']

        # Create a Report instance for saving the information
        report = Report(user_id=chat_id, is_realtime=True, timestamp=datetime.datetime.now(),
                        location=(latitude, longitude), description="something")
        save_report(report)

        response_text = "Location received and saved. Thank you!"
        send_response(chat_id, response_text)

    return Response("success", status=200)


def send_response(chat_id, response_text):
    api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': response_text
    }
    response = requests.post(api_url, json=payload)
    logger.debug("Response sent: %s", response.json())

def send_response_with_keyboard(chat_id, response_text, keyboard_options):
    api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    reply_markup = {
        'keyboard': [[option] for option in keyboard_options],
        'one_time_keyboard': True,
        'resize_keyboard': True
    }
    payload = {
        'chat_id': chat_id,
        'text': response_text,
        'reply_markup': reply_markup
    }
    response = requests.post(api_url, json=payload)
    logger.debug("Response with keyboard sent: %s", response.json())


if __name__ == "__main__":
    # Start the bot
    app.run()
