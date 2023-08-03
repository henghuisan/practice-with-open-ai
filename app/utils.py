import openai
from openai.error import InvalidRequestError
import configparser

config = configparser.ConfigParser()
config.read("credential.ini")
openai.api_key = "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"

def generate_image(prompt):
    images = []
    response = openai.Image.create(prompt=prompt, n=1, size="512x512", response_format="url")
    for image in response["data"]:
        images.append(image.url)
    return images[0]

def generate_content(prompt):
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
    content = response["choices"][0]["text"]
    result = f"<p>{content.replace('/n', '</p><p>')}</p>"
    return result

def generate_ai_chatbot_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )        
    reply = completion.choices[0].message.content
    return reply
