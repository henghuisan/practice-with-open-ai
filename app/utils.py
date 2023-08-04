import openai
from openai.error import InvalidRequestError
import configparser

config = configparser.ConfigParser()
config.read("credential.ini")
openai.api_key = "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"

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


def generate_content(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=1000
        )
        content = response["choices"][0]["text"]
        result = f"<p>{content.replace('/n', '</p><p>')}</p>"
        return "success", result
    except InvalidRequestError as e:
        return "fail", str(e)


def generate_ai_chatbot_response(messages):
    try:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = completion.choices[0].message.content
        messages.append({"role": "system", "content": reply})
        return "success", messages    
    except InvalidRequestError as e:
            return "fail", str(e)

def generate_corrected_transcript(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
            result = transcript.text
            return "success", result  
    except InvalidRequestError as e:
        return "fail", str(e)