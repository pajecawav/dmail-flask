import random
from string import ascii_lowercase
from typing import Any

import telebot

from dmail.config import BOT_TOKEN
from dmail.extensions import db
from dmail.models import Mailbox


class MailTeleBot(telebot.TeleBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_update_id = -1
        self.app = None

    def init_app(self, app):
        self.app = app

    def process_updates(self):
        updates = self.get_updates(offset=self.last_update_id + 1)

        if not updates:
            return
        self.process_new_updates(updates)
        self._last_update_id = max(update.update_id for update in updates)

    def handle_message(self, mailbox, message):
        self.send_message(mailbox.user, self._format_message(message))

    @staticmethod
    def _format_message(message):
        return "\n\n".join(
            [
                message.from_user,
                message.subject,
                message.text.rstrip("\n"),
            ]
        )


bot = MailTeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def command_start_help(message):
    bot.reply_to(message, "Available commands: /new, /delete, /address")


@bot.message_handler(commands="new")
def command_new(message):
    user = message.from_user.id

    if not user:
        bot.reply_to(message, "Can't detect user id")
        return

    print(f"Got new email request from {user}")

    with bot.app.app_context():
        old = Mailbox.query.filter_by(user=user).first()
        if old:
            old.delete()

        address = "".join(random.choices(ascii_lowercase, k=8))
        mailbox = Mailbox(user=user, address=address, method="telegram")
        db.session.add(mailbox)
        db.session.commit()

        bot.reply_to(message, f"Your mailbox is: {mailbox.full_address}")


@bot.message_handler(commands="delete")
def command_delete(message):
    user = message.from_user.id

    with bot.app.app_context():
        mailbox = Mailbox.query.filter_by(user=user).first()
        if not mailbox:
            bot.reply_to(message, "No email associated with this account")
        else:
            mailbox.delete()


@bot.message_handler(commands="address")
def command_address(message):
    user = message.from_user.id

    with bot.app.app_context():
        mailbox = Mailbox.query.filter_by(user=user).first()
        if not mailbox:
            bot.reply_to(message, "No email associated with this account")
        else:
            bot.reply_to(message, f"Your mail address is: {mailbox.full_address}")
