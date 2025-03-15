import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'players.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "ASDASDSADASDADAS"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'img')
    MAX_CONTENT_LENGTH = 60 * 1024 * 1024 
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'gif',  # Зображення
    }