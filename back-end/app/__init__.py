from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from sqlalchemy.engine import Engine
from sqlalchemy import event

# Flask-SQLAlchemy plugin
db = SQLAlchemy()
# Flask-Migrate plugin
migrate = Migrate()

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)

    # 注册 blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.api import question_blueprint as question_bp
    app.register_blueprint(question_bp)

    from app.api import testpaper_blueprint as testpaper_bp
    app.register_blueprint(testpaper_bp)

    from app.api import wqb
    app.register_blueprint(wqb)

    from app.api import statistics_blueprint as statistics_bp
    app.register_blueprint(statistics_bp)

    return app