import streamlit as st
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def get_payload(image):
    return {
        "model": "gpt-4o",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "Det här är en svensk parkeringsskylt. När får jag parkera här?"
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
    }

st.title('Parking app')

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def encode_picture(image):
        return base64.b64encode(image).decode('utf-8')

def get_content(response):
    return response['choices'][0]['message']['content']


tab1, tab2 = st.tabs(["File upload", "Camera"])

with tab1:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write(uploaded_file.name)
        file_name = "images/ingredients-list-from-lotion-showing-the-ingredient-ethylenediaminetetraacetic-BBRP2E.jpg"
        encoded_image = encode_image(file_name)
        print(encoded_image)
        st.image(file_name, caption='Parkeringsskylt')
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=get_payload(encoded_image))

        st.write(get_content(res.json()))

with tab2:
    picture = st.camera_input("Take a picture")

    if picture:
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=get_payload(encode_picture(picture.getvalue())))

        st.write(get_content(res.json()))

    
