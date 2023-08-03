# import configparser
# import datetime
# import openai
# from openai.error import InvalidRequestError
# from flask import (
#     Flask,
#     redirect,
#     render_template,
#     request,
#     url_for,
# )

# app = Flask(__name__)

# # openai.api_key = os.getenv("OPENAI_API_KEY")
# config = configparser.ConfigParser()
# config.read("credential.ini")
# openai.api_key = "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"

# @app.route("/", methods=("GET", "POST"))
# def index():
#     return render_template("index.html")


# # ======= IMAGE GENERATOR (begin) ======= #
# @app.route("/image-generator", methods=("GET", "POST"))
# def image_generator():
#     if request.method == "POST":
#         prompt = request.form["description"]
#         try:
#             images = []
#             response = openai.Image.create(
#                 prompt=prompt, n=1, size="512x512", response_format="url"
#             )
#             for image in response["data"]:
#                 images.append(image.url)
#             return redirect(url_for("image_generator", result=images[0], prompt=prompt))
#         except InvalidRequestError as e:
#             print(e)
#     result = request.args.get("result")
#     prompt = request.args.get("prompt")
#     return render_template("image_generator.html", result=result, prompt=prompt)
# # ======= IMAGE GENERATOR (end) ======= #


# # ======= CONTENT GENERATOR (begin) ======= #
# @app.route("/content-generator", methods=("GET", "POST"))
# def content_generator():
#     if request.method == "POST":
#         prompt = request.form["content"]
#         try:
#             response = openai.Completion.create(
#                 engine="text-davinci-003", prompt=prompt, max_tokens=1000
#             )
#             print(response)
#             essay_output = response["choices"][0]["text"]
#             result = f"<p>{essay_output.replace('/n', '</p><p>')}</p>"

#             return redirect(url_for("content_generator", result=result, prompt=prompt))
#         except InvalidRequestError as e:
#             print(e)
#     result = request.args.get("result")
#     prompt = request.args.get("prompt")
#     return render_template("content_generator.html", result=result, prompt=prompt)
# # ======= CONTENT GENERATOR (end) ======= #


# # ======= AI CHATBOT (begin) ======= #
# @app.route("/at-chatbot", methods=("GET", "POST"))
# def ai_chatbot():
#     messages = [
#         {"role": "system", "content": "What can I help you today?"},
#     ]
#     if request.method == "POST":
#         prompt = request.form["input"]
#         try:
#             response = openai.Completion.create(
#                 engine="text-davinci-003", prompt=prompt, max_tokens=1000
#             )
#             print(response)
#             essay_output = response["choices"][0]["text"]
#             result = f"<p>{essay_output.replace('/n', '</p><p>')}</p>"

#             return redirect(url_for("ai_chatbot", messages=messages))
#         except InvalidRequestError as e:
#             print(e)
#     if request.args.get("messages"):
#         messages = request.args.get("messages")
#     return render_template("ai_chatbot.html", messages=messages)
# # ======= AI CHATBOT (end) ======= #


# if __name__ == "__main__":
#     app.run()



# # https://medium.com/@nohanabil/how-to-deploy-flask-app-using-vercel-885ce034624