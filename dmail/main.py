import logging

from dotenv import load_dotenv

load_dotenv("./.env")

from flask import Flask

from dmail import views
from dmail.config import DATABASE_PATH
from dmail.extensions import db, scheduler
from dmail.telegram_bot import bot

logging.getLogger("apscheduler").setLevel(logging.ERROR)


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    bot.init_app(app)


def register_blueprints(app):
    app.register_blueprint(views.blueprint)


app = create_app()
scheduler.add_job(bot.process_updates, "interval", seconds=1)


@app.cli.command("init-db")
def init_db():
    """Initialize database"""
    db.create_all()


if __name__ == "__main__":
    app.run()
