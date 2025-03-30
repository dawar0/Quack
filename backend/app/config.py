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

    # Redis Cache Configuration
    REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
    REDIS_PORT = int(os.environ.get("REDIS_PORT") or 6379)
    REDIS_CACHE_DB = int(os.environ.get("REDIS_CACHE_DB") or 1)
    REDIS_DEFAULT_EXPIRATION = int(
        os.environ.get("REDIS_DEFAULT_EXPIRATION") or 3600
    )  # 1 hour

    # Mail Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.gmail.com"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() in ["true", "1", "t"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or "noreply@quack.com"
