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
    logger.error(f"Update {update} caused an error: {context.error}")
