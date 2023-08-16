import os
import openai

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Generate a response using ChatGPT
def generate_response(input_text: str) -> str:
    # Use the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="davinci",  # Choose the engine you prefer
        prompt=input_text,
        max_tokens=50  # Set the desired length of the response
    )
    return response.choices[0].text.strip()
