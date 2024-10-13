import sys

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot import config
from bot.handlers import error, start, help, message, unknown, callback, weekly, daily
from bot.utils import logger


def main() -> ...:
    logger.info("Starting a bot")
    # Create the Application.
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Commands handlers.
    app.add_handler(CommandHandler("start", start.handle_start_command))
    app.add_handler(CommandHandler("help", help.handle_help_command))
    app.add_handler(CommandHandler("daily_report", daily.handle_daily_report))
    app.add_handler(CommandHandler("weekly_report", weekly.handle_weekly_report))

    # Messages handlers.
    app.add_handler(MessageHandler(filters.COMMAND, unknown.handle_unknown_command))
    app.add_handler(MessageHandler(filters.TEXT, message.handle_any_message))

    # Erros handlers.
    app.add_error_handler(error.handle_error)

    # Callback query handlers.
    app.add_handler(CallbackQueryHandler(callback.handle_callback_query_buttons))

    logger.info("Start to polling")
    app.run_polling(
        # Time to wait between polling updates from Telegram in seconds.
        poll_interval=1,
        # Run the bot until the user presses Ctrl-C
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logger.exception(err)
        sys.exit(1)
