from celery import Celery
from flask import Flask

celery_app = Celery(__name__, broker="redis://localhost:6379/0")


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with self.app.app_context():
            return self.run(*args, **kwargs)


def init_celery(app: Flask):
    celery_app.config_from_object(app.config)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
