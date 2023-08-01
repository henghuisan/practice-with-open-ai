import configparser
import datetime
import openai
from openai.error import InvalidRequestError
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

config = configparser.ConfigParser() 
config.read('credential.ini')
openai.api_key = "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"

@app.route("/image-generator", methods=("GET", "POST"))
def image_generator():
    if request.method == "POST":
        prompt = request.form["description"]
        try:
            images = []
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size='512x512',
                response_format='url'
            )
            for image in response['data']:
                images.append(image.url)
            return redirect(url_for("image_generator", result=images[0], prompt=prompt))
        except InvalidRequestError as e:
            print(e)
    result = request.args.get("result")
    prompt = request.args.get("prompt")
    return render_template("image_generator.html", result=result, prompt=prompt)

if __name__ == '__main__':
    app.run()


# https://medium.com/@nohanabil/how-to-deploy-flask-app-using-vercel-885ce034624
