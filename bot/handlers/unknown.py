from telegram import Update, User
from telegram.ext import ContextTypes

from bot.templater import render_template
from bot.utils import logger


async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when unknown command is issued."""
    user: User = update.effective_user

    logger.info("User (usename='%s' id='%s') specified unknown command", user.username, user.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_template(name="wrong_command.tpl", values=dict(is_command=True)),
    )
