from telegram import Update
from telegram.ext import ContextTypes

from bot.templater import render_template
from bot.logger import logger


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_template(name="error.tpl", values=dict(error=context.error)),
    )

    logger.error(f"Update {update} caused an error: {context.error}")
