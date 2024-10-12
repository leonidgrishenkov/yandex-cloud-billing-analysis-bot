import sys

import config
from handlers import command, error, message
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from utils import logger


def main() -> ...:
    logger.info("Starting a bot")
    # Create the Application.
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Commands handlers.
    app.add_handler(CommandHandler("start", command.handle_start_command))
    app.add_handler(CommandHandler("help", command.handle_help_command))
    app.add_handler(CommandHandler("daily_report", command.handle_daily_report))
    app.add_handler(CommandHandler("weekly_report", command.handle_weekly_report))

    # Messages handlers.
    app.add_handler(MessageHandler(filters.COMMAND, command.handle_unknown_command))
    app.add_handler(MessageHandler(filters.TEXT, message.handle_any_message))

    # Erros handlers.
    app.add_error_handler(error.handle_error)

    # Callback query handlers.
    app.add_handler(CallbackQueryHandler(command.handle_callback_query_buttons))

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
