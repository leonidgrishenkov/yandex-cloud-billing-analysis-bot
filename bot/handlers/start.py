from telegram import ForceReply, Update, User
from telegram.ext import ContextTypes

from bot import config
from bot.templater import render_template
from bot.utils import logger


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when the command /start is issued."""
    user: User = update.effective_user

    if user.id in config.AUTHORIZED_USERS:
        logger.info(
            "User (usename='%s' id='%s') triggered the `/start` command", user.username, user.id
        )
        await update.message.reply_html(
            text=render_template(
                name="start.tpl",
                values=dict(user=user.mention_html()),
            ),
            reply_markup=ForceReply(selective=True),
        )
    else:
        logger.warning(
            "Unauthorized user (usename='%s' id='%s') triggered the `/start` command!",
            user.username,
            user.id,
        )
        await update.message.reply_text(
            text=render_template(
                name="unauthorized.tpl",
            ),
        )
