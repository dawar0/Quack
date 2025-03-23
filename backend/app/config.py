import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = (
        os.environ.get("CELERY_BROKER_URL") or "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND = (
        os.environ.get("CELERY_RESULT_BACKEND") or "redis://localhost:6379/0"
    )
    RESTX_MASK_SWAGGER = False
