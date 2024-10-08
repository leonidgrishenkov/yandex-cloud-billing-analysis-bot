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
import pandas as pd


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the /start command", user.username)

    await update.message.reply_html(
        text=rf"Hi {user.mention_html()}! Please, use one of available commands",
        reply_markup=ForceReply(selective=True),
    )


async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the /help command", user.username)
    await update.message.reply_text(text="This is a help page")


# async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = " ".join(context.args).upper()
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User | None = update.effective_user
    logger.info("User `%s` specified unknown command", user.username)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Please, use one of available commands",
    )


async def handle_test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the /test command", user.username)

    data = {
        "fruit": ["apple", "banana", "grapes", "orange"],
        "colour": ["red", "yellow", "green", "orange"],
        "quantity": [2, 1, 1, 3],
        "price": [80, 40, 100, 75],
    }
    df = pd.DataFrame(data)
    text_table = f"<pre>{df.to_string(index=False)}</pre>"

    await update.message.reply_text(text_table, parse_mode="HTML")
