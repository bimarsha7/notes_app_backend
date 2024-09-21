from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from celery import Celery, Task
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv(override=True)
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
# celery = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'), 
#                 backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'))


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # celery.conf.update(app.config)

    celery_init_app(app)
    from . import routes
    app.register_blueprint(routes.bp)

    return app

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('config.Config')
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
