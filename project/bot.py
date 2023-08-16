import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from chatgpt import generate_response
from database import save_user_message, save_bot_response

# Load environment variables from .env file
load_dotenv()

# Initialize Telegram Bot API
telegram_token = os.getenv("TELEGRAM_TOKEN")
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

# Command handler for /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm your ChatGPT bot. Send me a message!")

# Message handler for user messages
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message_text = update.message.text

    # Save user message to the database
    save_user_message(user_id, message_text)

    # Generate a response using ChatGPT
    response = generate_response(message_text)

    # Save bot response to the database
    save_bot_response(user_id, response)

    # Send the response back to the user
    update.message.reply_text(response)

# Error handler
def error(update: Update, context: CallbackContext):
    logging.error(f"Update {update} caused error {context.error}")

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dispatcher.add_error_handler(error)

if __name__ == "__main__":
    # Start the bot
    updater.start_polling()
    updater.idle()
