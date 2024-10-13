from telegram import Update
from telegram.ext import ContextTypes

from bot.templater import render_template


async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=render_template(name="wrong_command.tpl", values=dict(is_command=False)),
    )
