import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from openai.error import InvalidRequestError
from .utils import generate_image, generate_content, generate_ai_chatbot_response, generate_corrected_transcript

main_bp = Blueprint("main", __name__)
image_gen_bp = Blueprint("image_gen", __name__)
content_gen_bp = Blueprint("content_gen", __name__)
ai_chatbot_bp = Blueprint("ai_chatbot", __name__)
speech_to_text_bp = Blueprint("speech_to_text", __name__)


@main_bp.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")


@image_gen_bp.route("/", methods=("GET", "POST"))
def image_generator():
    if request.method == "POST":
        prompt = request.form["description"]
        status, result = generate_image(prompt)
        return redirect(
            url_for(
                "image_gen.image_generator",
                status=status,
                result=result,
                prompt=prompt,
            )
        )
    args = request.args
    status, result, prompt = args.get("status"), args.get("result"), args.get("prompt")
    return render_template(
        "image_generator.html", status=status, result=result, prompt=prompt
    )


@content_gen_bp.route("/", methods=("GET", "POST"))
def content_generator():
    if request.method == "POST":
        prompt = request.form["content"]
        status, result = generate_content(prompt)
        return redirect(
            url_for(
                "content_gen.content_generator",
                status=status,
                result=result,
                prompt=prompt,
            )
        )
    args = request.args
    status, result, prompt = args.get("status"), args.get("result"), args.get("prompt")
    return render_template(
        "content_generator.html", status=status, result=result, prompt=prompt
    )


@ai_chatbot_bp.route("/", methods=("GET", "POST"))
def ai_chatbot():
    messages = (
        request.args.get("messages")
        if request.args.get("messages")
        else [{"role": "system", "content": "What can I help you today?"}]
    )
    if request.method == "POST":
        prompt = request.form["input"]
        messages.append({"role": "user", "content": prompt})
        status, messages = generate_ai_chatbot_response(messages)
        return jsonify(status=status, messages=messages)
    return render_template("ai_chatbot.html", messages=messages)


@speech_to_text_bp.route("/", methods=("GET", "POST"))
def speech_to_text():
    if request.method == "POST":
        if "audio" in request.files:
            audio_file = request.files["audio"]
            if audio_file:
                # Generate a unique filename for the audio file
                filename = f"{str(uuid.uuid4())}.wav"
               # Save the audio file to the "static/audio" directory
                audio_file_path = os.path.join("app", "static", "audio", filename)
                audio_file.save(audio_file_path)
                # Check if the file exists before generating the transcript
                if os.path.isfile(audio_file_path):
                    status, result = generate_corrected_transcript(audio_file_path)
                    # Close the file
                    audio_file.close()
                    # Delete the file
                    os.remove(audio_file_path)
                    return jsonify(status=status, result=result)
        return jsonify({"status": "error", "message": "No audio file received."})
    return render_template("speech_to_text.html")

