# app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration settings from config.py
    app.config.from_object('config')

    # Register blueprints for different parts of the app
    from .routes import main_bp, image_gen_bp, content_gen_bp, ai_chatbot_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(image_gen_bp, url_prefix='/image-generator')
    app.register_blueprint(content_gen_bp, url_prefix='/content-generator')
    app.register_blueprint(ai_chatbot_bp, url_prefix='/ai-chatbot')

    return app
