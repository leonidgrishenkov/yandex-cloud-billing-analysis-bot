from telegram import Update
from telegram.ext import ContextTypes


async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="It's not a command. 🤷 Please, use one of available commands.",
    )
