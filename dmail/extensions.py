import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))
