import openai

# Generate a response using ChatGPT
def generate_response(input_text: str) -> str:
    return main()

# Set your OpenAI API key
api_key_file = 'api_key_file.txt'  # Replace with the path to your API key file

with open(api_key_file, 'r') as file:
    openai.api_key = file.read().strip()


def generate_chatgpt_response(conversation_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    return response.choices[0].message["content"]


def main():
    conversation_history = []

    # Bot starts the conversation
    conversation_history.append({"role": "assistant",
                                 "content": "Welcome to our reporting bot. Please provide a description of the agricultural incident you observed. I want to ask a question that are not related to the event time and location."})
    user_description = "I saw two people breaking into the farm, the people looked armed and came with a big truck."
    conversation_history.append({"role": "user", "content": user_description})

    num_questions = 3  # Counter for asked questions

    # Start dynamic question asking loop
    for i in range(num_questions):
        dynamic_question = generate_chatgpt_response(conversation_history)
        conversation_history.append({"role": "assistant", "content": dynamic_question})
        print(dynamic_question)

        # Collect user's answer to the question
        user_answer = input("User answer:\n")
        conversation_history.append({"role": "user", "content": user_answer})

    user_answer = "Please provide a detailed summary of the event based on the information provided. Include all relevant details from the answers to the questions asked and the initial description. Exclude any information related to the event's location and time. If any details are missing, indicate that they are unknown."

    conversation_history.append({"role": "user", "content": user_answer})

    # Generate enhanced event description based on all inputs
    enhanced_description_response = generate_chatgpt_response(conversation_history)
    conversation_history.append({"role": "assistant", "content": enhanced_description_response})
    print("------------------------")
    print(enhanced_description_response)
    return enhanced_description_response


if __name__ == "__main__":
    main()