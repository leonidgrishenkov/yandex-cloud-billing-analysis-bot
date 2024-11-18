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
from bot.handlers import (
    balance,
    callback,
    daily,
    error,
    help,
    message,
    monthly,
    start,
    unknown,
    weekly,
)
from bot.logger import logger

COMMAND_HANDLERS = dict(
    start=start.handle_start_command,
    help=help.handle_help_command,
    daily_report=daily.handle_daily_report,
    weekly_report=weekly.handle_weekly_report,
    monthly_report=monthly.handle_monthly_report,
    balance=balance.handle_balance_command,
)


def main() -> ...:
    logger.info("Calling application builder")
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    for command, handler in COMMAND_HANDLERS.items():
        app.add_handler(
            CommandHandler(
                command=command,
                callback=handler,
            ),
        )

    app.add_handler(MessageHandler(filters.COMMAND, unknown.handle_unknown_command))
    app.add_handler(MessageHandler(filters.TEXT, message.handle_any_message))

    app.add_error_handler(error.handle_error)

    app.add_handler(CallbackQueryHandler(callback.handle_callback_query_buttons))

    logger.info("Calling `run_polling`")
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
