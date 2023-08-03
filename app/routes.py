from flask import Blueprint, render_template, redirect, url_for, request, jsonify 
from openai.error import InvalidRequestError
from .utils import generate_image, generate_content, generate_ai_chatbot_response

main_bp = Blueprint("main", __name__)
image_gen_bp = Blueprint("image_gen", __name__)
content_gen_bp = Blueprint("content_gen", __name__)
ai_chatbot_bp = Blueprint("ai_chatbot", __name__)


@main_bp.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")


@image_gen_bp.route("/", methods=("GET", "POST"))
def image_generator():
    if request.method == "POST":
        prompt = request.form["description"]
        try:
            image_url = generate_image(prompt)
            return redirect(
                url_for("image_gen.image_generator", result=image_url, prompt=prompt)
            )
        except InvalidRequestError as e:
            print(e)
    result = request.args.get("result")
    prompt = request.args.get("prompt")
    return render_template("image_generator.html", result=result, prompt=prompt)


@content_gen_bp.route("/", methods=("GET", "POST"))
def content_generator():
    if request.method == "POST":
        prompt = request.form["content"]
        try:
            content = generate_content(prompt)
            return redirect(
                url_for("content_gen.content_generator", result=content, prompt=prompt)
            )
        except InvalidRequestError as e:
            print(e)
    result = request.args.get("result")
    prompt = request.args.get("prompt")
    return render_template("content_generator.html", result=result, prompt=prompt)


@ai_chatbot_bp.route("/", methods=("GET", "POST"))
def ai_chatbot():
    messages = [
        {"role": "system", "content": "What can I help you today?"},
    ]
    if request.args.get("messages"):
        messages = request.args.get("messages")
    if request.method == "POST":
        prompt = request.form["input"]
        messages.append({"role": "user", "content": prompt})
        try:
            reply = generate_ai_chatbot_response(messages)
            messages.append({"role": "user", "content": reply})
            return jsonify(messages)
        except InvalidRequestError as e:
            print(e)
    return render_template("ai_chatbot.html", messages=messages)
