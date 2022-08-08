import logging
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from tweepy.client import Client
from tweepy.errors import Forbidden

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY", "")
TWITTER_API_BEARER = os.getenv("TWITTER_API_BEARER", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_API_ACCESS_KEY = os.getenv("TWITTER_API_ACCESS_KEY", "")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY", "")

twitter: Client | None = None

ALLOWED_URLS = {
    "https://gitlab.com/",
    "https://www.gitlab.com/",
    "https://github.com/",
    "https://www.github.com/",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    if not twitter:
        raise RuntimeError("No twitter account set")

    if not any(text.startswith(x) for x in ALLOWED_URLS):
        logging.warning("Not tweeting %s", text)
        return

    try:
        twitter.create_tweet(text=text)
    except Forbidden as exc:
        logging.warning("Cannot create tweet: %s. Reason: %s", text, exc)
    else:
        logging.info("Tweeted %s", text)


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    global twitter

    twitter = Client(
        bearer_token=TWITTER_API_BEARER,
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_API_ACCESS_KEY,
        access_token_secret=TWITTER_API_SECRET_KEY,
    )

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
