import os
import io
import requests
from dotenv import load_dotenv
import openai
from openai.error import InvalidRequestError
import configparser
import cloudinary
import cloudinary.uploader
import cloudinary.api
import tempfile


# Load environment variables from .flaskenv
load_dotenv()

config = configparser.ConfigParser()
config.read("credential.ini")
openai.api_key = os.getenv("OPENAI_API_KEY")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def generate_image(prompt):
    try:
        images = []
        response = openai.Image.create(
            prompt=prompt, n=1, size="512x512", response_format="url"
        )
        for image in response["data"]:
            images.append(image.url)
        return "success", images[0]
    except InvalidRequestError as e:
        return "fail", str(e)


def generate_essay1(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=1000
        )
        content = response["choices"][0]["text"]
        result = content.replace('\\n', '</p><p>')
        return "success", result
    except InvalidRequestError as e:
        return "fail", str(e)


def generate_essay(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        result = response['choices'][0]['message']['content']
        return "success", result
    except InvalidRequestError as e:
        return "fail", str(e)


def generate_ai_chatbot_response(messages):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = completion.choices[0].message.content
        messages.append({"role": "system", "content": reply})
        return "success", messages
    except InvalidRequestError as e:
        return "fail", str(e)


def generate_corrected_transcript_with_cloudinary_audio_file(audio_url):
    try:
        # Fetch the audio file as bytes using requests
        response = requests.get(audio_url)
        audio_data = response.content
        # Create a io.BufferedReader object from the bytes data and set the name attribute
        audio_buffer = io.BytesIO(audio_data)
        audio_buffer.name = "user_voice_input.wav"  # Replace with the desired filename
        # Pass the temporary file to the translate method
        transcript = openai.Audio.translate("whisper-1", audio_buffer)
        result = transcript.text
        return "success", result
    except InvalidRequestError as e:
        return "fail", str(e)


def generate_corrected_transcript_with_local_audio_file(audio_url):
    try:
        with open(audio_url, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
            result = transcript.text
            return "success", result
    except InvalidRequestError as e:
        return "fail", str(e)
