from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
)
from telegram.ext import ContextTypes

from bot import config
from bot.templater import render_template
from bot.utils import logger


async def handle_weekly_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User = update.effective_user

    if user.id in config.AUTHORIZED_USERS:
        logger.info(
            "User (usename='%s' id='%s') triggered the `/weekly_report` command",
            user.username,
            user.id,
        )

        keyboard = [
            [InlineKeyboardButton(text="By Service", callback_data="weekly_by_service")],
            [InlineKeyboardButton("By Product", callback_data="weekly_by_product")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        logger.info("Waiting for `%s` user to click the button", user.username)
        await update.message.reply_text(
            text=render_template(name="selection_prompt.tpl"), reply_markup=reply_markup
        )
    else:
        logger.warning(
            "Unauthorized user (usename='%s' id='%s') triggered the `/weekly_report` command!",
            user.username,
            user.id,
        )

        await update.message.reply_text(
            text=render_template(
                name="unauthorized.tpl",
            ),
        )
