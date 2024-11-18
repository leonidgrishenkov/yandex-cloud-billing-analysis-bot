from typing import cast

from telegram import Update, User
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.handlers import validator
from bot.logger import logger
from bot.templater import render_template
from bot.yc import get_balance


@validator.validate_user
async def handle_balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User = cast(User, update.effective_user)

    logger.info("User triggered the %s command. %s", update.message.text, user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_template(name="balance.tpl", values=dict(balance=get_balance())),
        parse_mode=ParseMode.HTML,
    )
