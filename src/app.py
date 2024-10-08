from telegram import (
    ForceReply,
    User,
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    WebAppInfo,
    InlineKeyboardButton,
)
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from utils import logger
from handlers import command, error, message
import sys
import os
import dotenv

POLL_INTERVAL = 1  # seconds


def main() -> ...:
    dotenv.load_dotenv()

    logger.info("Starting a bot")
    # Create the Application.
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add commands handlers.
    app.add_handler(CommandHandler("start", command.handle_start_command))
    app.add_handler(CommandHandler("help", command.handle_help_command))
    app.add_handler(CommandHandler("test", command.handle_test_command))
    app.add_handler(CommandHandler("costByProduct", command.handle_cost_by_product))
    app.add_handler(CommandHandler("costByService", command.handle_cost_by_service))
    # app.add_handler(CommandHandler("caps", caps))

    # Add messages handlers.
    app.add_handler(MessageHandler(filters.COMMAND, command.handle_unknown_command))
    app.add_handler(MessageHandler(filters.TEXT, message.handle_any_message))

    # Add erros handlers
    app.add_error_handler(error.log_error)

    logger.info("Running polling with %s seconds poll interval", POLL_INTERVAL)
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
