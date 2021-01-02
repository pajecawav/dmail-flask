Disposable mail server that uses [Sendgrid](https://sendgrid.com/) for mail
routing.

# Installation

Clone repository and install dependencies:

```
git clone https://github.com/pajecawav/dmail
poetry install
```

Set environment variables (or modify `.env.example` file):

-   `DATABASE_PATH` -- where to store sqlite database (default is
    `sqlite:///db.sqlite3`)
-   `MAIL_ROUTE` -- route for Sendgrid mail webhook (follow [this
    tutorial](https://sendgrid.com/docs/for-developers/parsing-email/setting-up-the-inbound-parse-webhook/))
-   `DOMAIN` -- your mail domain
-   `BOT_TOKEN` -- Telegram bot token

Start development server:

```
FLASK_APP=dmail/main poetry run flask run
```

Or use a better web server like `gunicorn`.
