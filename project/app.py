import datetime
import os
import logging
from response_parser import Report
import requests
from flask import Flask, request, Response
from database import save_report

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Telegram Bot API
telegram_token = os.getenv("TELEGRAM_TOKEN")
webhook_url = os.getenv("WEBHOOK_URL")
#requests.get(webhook_url)

logger.debug("Telegram Token: %s", telegram_token)
logger.debug("Webhook URL: %s", webhook_url)

# Create an app
app = Flask(__name__)


# Create a /sanity route
@app.route('/sanity')
def sanity_check():
    return 'Server is running'


# Create a dictionary to store user states
user_states = {}


# Create a /message route to handle incoming messages
@app.route('/message', methods=["POST"])
def handle_message():
    data = request.json
    print("Received data:", data)  # Print the received data for debugging
    if 'message' not in data:
        return Response("No message data received", status=400)  # Return an error response if no 'message' key

    chat_id = data['message']['chat']['id']

    if chat_id not in user_states:
        # # Create a Report instance for saving the information
        # report = Report(user_id=chat_id)
        #print("report.user_id =", report.user_id)
        #print("report.description =", report.description)
        user_states[chat_id] = "start"

    if 'text' in data['message']:
        message_text = data['message']['text']
        logger.debug("Received a text message from Telegram: %s", message_text)

        if user_states[chat_id] == "start":
            if message_text.startswith('/start'):
                response_text = "Welcome to the Agricultural Crime Reporting Bot! Please choose an option: /report"
                user_states[chat_id] = "report"
                send_response(chat_id, response_text)
            else:
                response_text = "in status start, try again."
                send_response(chat_id, response_text)

        elif user_states[chat_id] == "report":
            if message_text == "/report":
                response_text = "Please send the location of the incident where you saw the crime. You can use the GPS " \
                                "location feature."
                user_states[chat_id] = "added location"
                send_response(chat_id, response_text)
            else:
                response_text = "in status report, try again."
                send_response(chat_id, response_text)
        else:
            response_text = "restarting the chat, press /start for a new report"
            user_states[chat_id] = "report"
            send_response(chat_id, response_text)

    elif 'location' in data['message']:
        if user_states[chat_id] == "added location":
            location = data['message']['location']
            latitude = location['latitude']
            longitude = location['longitude']
                #loc = (latitude, longitude)
                # report.set_location(loc)
                # print("report.location =", report.location)
            report = Report(user_id=chat_id, is_realtime=True, timestamp=datetime.datetime.now(),
                                location=(latitude, longitude), description="somethinggggg")
            user_states[chat_id] = "saving  report"
            save_report(report)

            response_text = "Location received and saved. Thank you!"
            send_response(chat_id, response_text)
        else:
            response_text = "in status added location, try again."
            send_response(chat_id, response_text)
    else:
        response_text = "Got it."
        send_response(chat_id, response_text)

    # elif 'location' in data['message']:
    #     location = data['message']['location']
    #     latitude = location['latitude']
    #     longitude = location['longitude']
    #
    #     # Create a Report instance for saving the information
    #     report = Report(user_id=chat_id, is_realtime=True, timestamp=datetime.datetime.now(),
    #                     location=(latitude, longitude), description="something")
    #     save_report(report)
    #
    #     response_text = "Location received and saved. Thank you!"
    #     send_response(chat_id, response_text)

    return Response("success", status=200)


def send_response(chat_id, response_text):
    api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': response_text
    }
    response = requests.post(api_url, json=payload)
    logger.debug("Response sent: %s", response.json())


# def send_response_with_keyboard(chat_id, response_text, keyboard_options):
#     api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
#     reply_markup = {
#         'keyboard': [[option] for option in keyboard_options],
#         'one_time_keyboard': True,
#         'resize_keyboard': True
#     }
#     payload = {
#         'chat_id': chat_id,
#         'text': response_text,
#         'reply_markup': reply_markup
#     }
#     response = requests.post(api_url, json=payload)
#     logger.debug("Response with keyboard sent: %s", response.json())


if __name__ == "__main__":
    # Set up the webhook here
    requests.get(webhook_url)
    # Start the bot
    app.run()
