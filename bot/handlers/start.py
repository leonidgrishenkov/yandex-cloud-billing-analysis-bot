from typing import cast

from telegram import ForceReply, Update, User
from telegram.ext import ContextTypes

from bot.handlers import validator
from bot.templater import render_template
from bot.utils import logger


@validator.validate_user
async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when the command /start is issued."""
    user: User = cast(User, update.effective_user)

    logger.info("User triggered the %s command. %s", update.message.text, user)
    await update.message.reply_html(
        text=render_template(
            name="start.tpl",
            values=dict(user=user.mention_html()),
        ),
        reply_markup=ForceReply(selective=True),
    )
