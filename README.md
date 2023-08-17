# Agricultural Crime Reporting Bot

The Agricultural Crime Reporting Bot is a Telegram bot designed to simplify the process of reporting agricultural incidents. This bot assists users in describing incidents, provides guidance for accurate descriptions, and generates informative summaries using AI-powered language models.

## Features

- **Dynamic Interaction:** Engage in natural conversations with the bot to describe incidents and answer relevant questions.
- **AI-Enhanced Descriptions:** Utilize the power of the GPT-3.5 Turbo model to enhance incident descriptions and generate comprehensive summaries.
- **Location Tracking:** Provide incident locations using GPS coordinates or textual descriptions.
- **Database Integration:** Store incident reports, including descriptions and locations, for future reference.
- **Real-Time Reporting:** Instantly report incidents with the option for real-time submissions.

## Table of Contents

- [Usage](#usage)
- [Code Structure](#code-structure)
- [Setup](#setup)
- [Database Configuration](#database-configuration)
- [Note](#note)
- [Credits](#credits)

## Usage

1. Start a conversation with the bot by sending the command `/start`.
2. Choose to report an incident using the command `/report`.
3. Provide incident details, including a description and location.
4. Engage in a dynamic conversation with the bot to enhance your incident description.
5. Receive an informative summary of the incident.
6. Confirm and submit the incident report.

## Code Structure

- `app.py`: The main application file that handles user interactions and communication with the GPT-3.5 Turbo model.
- `response_parser.py`: Defines the `Report` class for parsing and storing incident reports.
- `database.py`: Manages the storage of incident reports in a Firebase database.
- `chatGPT.py`: Communicates with the GPT-3.5 Turbo model to generate dynamic responses.

## Setup

1. Create a Telegram bot and obtain the bot token.
2. Set up a webhook URL for receiving Telegram updates.
3. Install the required packages using the following command:pip install flask requests firebase-admin openai
4. Set environment variables `TELEGRAM_TOKEN`, `WEBHOOK_URL`, `DATABASE_URL`, and `DATABASE_CRED_PATH`.
5. Run the Flask app using: python app.py


## Database Configuration

- The bot uses a Firebase database to store incident reports. Make sure to set up Firebase and obtain the necessary credentials.
- Store the Firebase database URL in the `DATABASE_URL` environment variable.
- Store the path to your Firebase service account JSON file in the `DATABASE_CRED_PATH` environment variable.

## Note

- This bot is created for educational purposes and is not meant to be used in real-world emergencies.
- Ensure that you have the required dependencies, environment variables, and permissions set up before running the bot.

## Credits

This project was developed by RUTY ROSENBER, Tamar Ivgi, Yiska Levi and Ruty Rosenber.
.

