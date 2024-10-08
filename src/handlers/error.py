from telegram import Update
from telegram.ext import ContextTypes

from utils import logger


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Specified command raised an error! 😔 See bot logs for details.",
    )

    logger.error(f"Update {update} caused an error: {context.error}")
