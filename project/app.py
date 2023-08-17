import datetime
import os
import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict

from response_parser import Report
import requests
from flask import Flask, request, Response
from database import save_report
from chatAPI import events_description, send_question, received_answer, \
    summary_event_description, get_conversation_history

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Telegram Bot API
telegram_token = os.getenv("TELEGRAM_TOKEN")
webhook_url = os.getenv("WEBHOOK_URL")

logger.debug("Telegram Token: %s", telegram_token)
logger.debug("Webhook URL: %s", webhook_url)

# Create an app
app = Flask(__name__)


class State(Enum):
    START = auto()
    REPORT = auto()
    LOCATION = auto()
    EXPLAIN = auto()
    ANSWER = auto()


@dataclass
class UserState:
    chat_id: int
    state: State
    location: (float, float)
    explanation: str
    conversation_history: list

    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.state = State.START
        self.location = (0, 0)
        self.explanation = ''
        self.conversation_history = get_conversation_history()


# Create a dictionary to store user states
current_users: Dict[int, UserState] = {}


def state_start(message_text, chat_id):
    if message_text.startswith('/start'):
        response_text = "Welcome to the Agricultural Crime Reporting Bot! Please choose an option: /report"
        current_users[chat_id].state = State.REPORT
    else:
        response_text = "in status start, try again."
    send_response(chat_id, response_text)


def state_report(message_text, chat_id):
    if message_text.startswith('/report'):
        response_text = "Please send the location of the incident where you saw the crime. " \
                        "You can use the GPS location feature."
        current_users[chat_id].state = State.LOCATION
    else:
        response_text = "in status report, try again."
    send_response(chat_id, response_text)


def state_location(location, chat_id):
    if current_users[chat_id].state == State.LOCATION:
        current_users[chat_id].location = (location['latitude'], location['longitude'])
        current_users[chat_id].state = State.EXPLAIN

        response_text = "Location received and saved. now please provide some explanation: "
    else:
        response_text = "in status added location, try again."
    send_response(chat_id, response_text)


def state_explain(message_text, chat_id):
    # sending to function that communicates with GPT
    conv = current_users[chat_id].conversation_history
    events_description(conv, message_text)
    question = send_question(conv)
    current_users[chat_id].state = State.ANSWER
    send_response(chat_id, question)


def state_answer(message_text, chat_id):
    conv = current_users[chat_id].conversation_history
    received_answer(conv, message_text)
    current_users[chat_id].explanation = summary_event_description(conv)
    report = Report(user_id=chat_id,
                    is_realtime=True,
                    timestamp=datetime.datetime.now(),
                    location=current_users[chat_id].location,
                    description=current_users[chat_id].explanation)

    del current_users[chat_id]
    save_report(report)
    response_text = "Report was received and saved.\n" \
                    "For a new report please enter /report! "
    # current_users[chat_id].state = State.REPORT
    send_response(chat_id, response_text)


# Create a /message route to handle incoming messages
@app.route('/message', methods=["POST"])
def handle_message():
    data = request.json
    print("Received data:", data)  # Print the received data for debugging

    if 'message' not in data:
        return Response("No message data received", status=400)  # Return an error response if no 'message' key

    chat_id = data['message']['chat']['id']

    if chat_id not in current_users:
        # Create a Report instance for saving the information
        current_users[chat_id] = UserState(chat_id)

    if 'text' in data['message']:
        message_text = data['message']['text']
        logger.debug("Received a text message from Telegram: %s", message_text)

        if current_users[chat_id].state == State.START:
            state_start(message_text, chat_id)
        elif current_users[chat_id].state == State.REPORT:
            state_report(message_text, chat_id)
        elif current_users[chat_id].state == State.EXPLAIN:
            state_explain(message_text, chat_id)
        elif current_users[chat_id].state == State.ANSWER:
            state_answer(message_text, chat_id)
        else:
            response_text = "restarting the chat, enter /start for a new report"
            current_users[chat_id].state = State.REPORT
            send_response(chat_id, response_text)

    elif 'location' in data['message']:
        state_location(data['message']['location'], chat_id)

    else:
        response_text = "Got it."
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


# Create a /sanity route
@app.route('/sanity')
def sanity_check():
    return 'Server is running'


if __name__ == "__main__":
    # Set up the webhook here
    # requests.get(webhook_url)
    app.run()
