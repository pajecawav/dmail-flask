import random
from string import ascii_lowercase

from flask import Blueprint, request

from dmail.config import MAIL_ROUTE
from dmail.extensions import db
from dmail.models import Mailbox, Message
from dmail.telegram_bot import bot

blueprint = Blueprint("", __name__)

custom_handlers = {
    "telegram": bot.handle_message,
}


@blueprint.route("/", methods=["POST"])
def index():
    address = "".join(random.choices(ascii_lowercase, k=8))
    mailbox = Mailbox.get(address)
    if mailbox is not None:
        mailbox.messages.clear()
    else:
        mailbox = Mailbox(address=address)
    db.session.add(mailbox)
    db.session.commit()
    return mailbox.full_address


@blueprint.route(MAIL_ROUTE, methods=["POST"])
def new_mail_route():
    form = request.form
    address = form["to"].split("@")[0].lstrip("<")
    message = Message(
        from_user=form["from"],
        to_user=address,
        subject=form["subject"],
        text=form["text"],
    )
    handle_message(address, message)
    return ""


@blueprint.route("/<string:address>", methods=["GET"])
def get_mail(address):
    mailbox = Mailbox.query.get(address)

    if not mailbox:
        return "No mailbox found"

    result = ""
    for message in mailbox.messages:
        result += "\n".join(
            [
                message.from_user,
                message.subject,
                message.text.rstrip("\n"),
            ]
        )
        result += "\n" + "=" * 30 + "\n"

    return result or "Empty"


def handle_message(address, message):
    mailbox = Mailbox.query.get(address)

    if not mailbox:
        print(f"Got email for unknown address {address}")
        return

    mailbox.add_message(message)
    handler = custom_handlers.get(mailbox.method)
    handler(mailbox, message)
