# 1 - Setup GROQ API key and environment
import os  # For accessing environment variables
from dotenv import load_dotenv  # To load variables from .env file
from groq import Groq  # GROQ client to interact with the LLM API

# Load environment variables from a .env file
load_dotenv()

# Retrieve the GROQ API key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# 2 - Function to convert image to base64 format for API use
import base64  # For encoding binary image data to base64

# Function to encode an image file into base64 format
def encode_image(image_path):
    # Open image file in binary read mode
    image_file = open(image_path, "rb")
    # Read the binary content of the file
    image = image_file.read()
    # Encode it to base64 and return it as a UTF-8 string
    return base64.b64encode(image).decode("utf-8")


# 3 - Function to send image and text prompt to the GROQ multimodal model
def analyze_image_with_query(query, encoded_image, model="llama-3.2-90b-vision-preview"):
    # Initialize the Groq client using the API key
    client = Groq(api_key=GROQ_API_KEY)

    # Create a message payload that includes a text query and the base64-encoded image
    messages = [
        {
            'role': "user",  # Role can be "user" or "assistant"; here it's the user asking
            "content": [
                {
                    "type": "text",  # First part of the message is the text query
                    "text": query
                },
                {
                    "type": "image_url",  # Second part is the image data in base64 format
                    "image_url": {
                        # Format: data:[<MIME-type>][;base64],<data>
                        "url": f"data:jpeg/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]

    # Send the message to the chat completion endpoint
    response = client.chat.completions.create(messages=messages, model=model)

    # Return only the content of the assistant's response
    return response.choices[0].message.content
