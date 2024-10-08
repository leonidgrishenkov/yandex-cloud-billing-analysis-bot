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


async def log_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Specified command raised an error 😔"
    )

    logger.error(f"Update {update} caused an error: {context.error}")
