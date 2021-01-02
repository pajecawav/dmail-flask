from dmail.config import DOMAIN
from dmail.extensions import db


class Mailbox(db.Model):
    address = db.Column(db.String, primary_key=True)
    user = db.Column(db.String, nullable=False)
    method = db.Column(db.String, nullable=True)
    messages = db.relationship(
        "Message", backref="mailbox", cascade="delete", lazy="dynamic"
    )

    @property
    def full_address(self):
        return f"{self.address}@{DOMAIN}"

    def add_message(self, message):
        self.messages.append(message)
        db.session.add(message)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String, nullable=False)
    to_user = db.Column(db.String, db.ForeignKey(Mailbox.address), nullable=False)
    subject = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
