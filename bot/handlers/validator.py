from typing import cast

from telegram import Update, User
from telegram.ext import ContextTypes

from bot import db
from bot.templater import render_template
from bot.utils import logger


def validate_user(handler):
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user: User = cast(User, update.effective_user)

        authusers: list[int] = await db.get_auth_users()

        if user.id not in authusers:
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
