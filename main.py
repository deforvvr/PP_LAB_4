import os

from telegram.ext import Application, CommandHandler

from handlers import (
    movie_details,
    ping,
    popular,
    random_movie,
    search,
    start,
    top_rated,
)


def main() -> None:
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    # Python 3.12+ may not have a default event loop in the main thread.
    # Ensure one exists for python-telegram-bot's run_polling.
    import asyncio

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("popular", popular))
    app.add_handler(CommandHandler("top", top_rated))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("movie", movie_details))
    app.add_handler(CommandHandler("random", random_movie))
    app.add_handler(CommandHandler("ping", ping))
    app.run_polling()


if __name__ == "__main__":
    main()
