import os

DOMAIN = os.environ["DOMAIN"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
MAIL_ROUTE = os.environ["MAIL_ROUTE"]
DATABASE_PATH = os.environ.get("DATABASE_PATH", "sqlite:///./db.sqlite")
