from flask import Flask
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    app.config.update(config_overrides)

    db.init_app(app)

    from main.views import main_app
    app.register_blueprint(main_app)

    from init.views import init_app
    app.register_blueprint(init_app)

    return app
