import os

import openai


openai.api_key = os.getenv("API_CHATGPT_KEY")

conversation_history = []
conversation_history.append({"role": "assistant",
                             "content": "Welcome to our reporting bot. Please provide a description of the agricultural incident you observed. I want to ask a question that are not related to the event time and location."})


def generate_chatgpt_response(conversation_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    return response.choices[0].message["content"]


def events_description(user_description: str):
    """
    The function receives the description of the event and sends it to the chat
    :param user_description:
    :return:
    """
    conversation_history.append({"role": "user", "content": user_description})


def send_question() -> str:
    dynamic_question = generate_chatgpt_response(conversation_history)
    conversation_history.append({"role": "assistant", "content": dynamic_question})
    return dynamic_question


def received_answer(user_answer: str):
    conversation_history.append({"role": "user", "content": user_answer})


def summary_event_description() -> str:
    explanation_of_what_the_summary_will_contain = "Please provide a detailed summary of the event based on the information provided. Include all relevant details from the answers to the questions asked and the initial description. Exclude any information related to the event's location and time. If any details are missing, indicate that they are unknown."
    conversation_history.append({"role": "user", "content": explanation_of_what_the_summary_will_contain})
    enhanced_description_response = generate_chatgpt_response(conversation_history)
    return enhanced_description_response


def main():
    user_description = "I saw two people breaking into the farm, the people looked armed and came with a big truck."
    events_description(user_description)

    num_questions = 3  # Counter for asked questions

    # Start dynamic question asking loop
    for i in range(num_questions):
        print(send_question())
        user_answer = input("User answer:\n")
        received_answer(user_answer)

    print("------------------------")
    print(summary_event_description())


if __name__ == "__main__":
    main()
