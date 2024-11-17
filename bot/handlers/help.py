from typing import cast

from telegram import Update, User
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.templater import render_template
from bot.logger import logger


async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when the command /help is issued."""
    user: User = cast(User, update.effective_user)

    logger.info("User triggered the %s command. %s", update.message.text, user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_template(name="help.tpl"),
        parse_mode=ParseMode.HTML,
    )
