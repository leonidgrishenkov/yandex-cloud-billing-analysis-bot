from typing import cast

from telegram import Update, User
from telegram.ext import ContextTypes

from bot import config
from bot.logger import logger
from bot.templater import render_template


def validate_user(handler):
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user: User = cast(User, update.effective_user)

        if user.id not in config.AUTH_USERS:
            logger.warning(
                "Unauthorized user triggered the %s command! %s", update.message.text, user
            )
            await update.message.reply_text(
                text=render_template(
                    name="unauthorized.tpl",
                ),
            )
            return
        await handler(update, context)

    return wrapped
