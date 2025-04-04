# 1 - Setup GROQ api key
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2 - Convert image to required format
import base64

# image_path = "data/acne.jpg"
def encode_image(image_path):
    image_file = open(image_path, "rb")
    image = image_file.read()
    return base64.b64encode(image).decode("utf-8")

# 3 - Setup multimodal LLM

def analyze_image_with_query(query, encoded_image, model="llama-3.2-90b-vision-preview"):
    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {
            'role': "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        #        data:[<MIME-type>][;base64],<data>
                        "url": f"data:jpeg/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]

    response = client.chat.completions.create(messages=messages, model=model)

    return response.choices[0].message.content