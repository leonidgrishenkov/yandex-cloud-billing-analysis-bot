from typing import cast

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
)
from telegram.ext import ContextTypes

from bot.handlers import validator
from bot.templater import render_template
from bot.utils import logger


@validator.validate_user
async def handle_monthly_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User = cast(User, update.effective_user)

    logger.info("User triggered the %s command. %s", update.message.text, user)

    keyboard = [
        [InlineKeyboardButton(text="By Service", callback_data="monthly_by_service")],
        [InlineKeyboardButton("By Product", callback_data="monthly_by_product")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info("Waiting for `%s` user to click the button", user.username)
    await update.message.reply_text(
        text=render_template(name="selection_prompt.tpl"), reply_markup=reply_markup
    )
