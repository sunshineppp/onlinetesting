from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import question_blueprint as api_question
    app.register_blueprint(api_question)

    from app.api import testpaper_blueprint as api_testpaper
    app.register_blueprint(api_testpaper)

    return app

from app.model import models