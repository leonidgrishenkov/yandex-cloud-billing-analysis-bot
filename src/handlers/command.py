import os

import boto3
import dotenv
import pandas as pd
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
    User,
    WebAppInfo,
)
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from report import daily, weekly
from utils import logger

dotenv.load_dotenv()


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user: User | None = update.effective_user

    logger.info("User `%s` triggered the /start command", user.username)

    await update.message.reply_html(
        text=rf"Hi {user.mention_html()}! Please, use one of available commands",
        reply_markup=ForceReply(selective=True),
    )


async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user: User | None = update.effective_user

    logger.info("User `%s` triggered the /help command", user.username)

    await update.message.reply_text(text="This is a help page")


# async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = " ".join(context.args).upper()
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when unknown command is issued."""
    user: User | None = update.effective_user

    logger.info("User `%s` specified unknown command", user.username)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Please, use one of available commands",
    )


# async def handle_test_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     user: User | None = update.effective_user
#     logger.info("User `%s` triggered the /test command", user.username)

#     data = {
#         "fruit": ["apple", "banana", "grapes", "orange"],
#         "colour": ["red", "yellow", "green", "orange"],
#         "quantity": [2, 1, 1, 3],
#         "price": [80, 40, 100, 75],
#     }
#     df = pd.DataFrame(data)
#     text_table = f"<pre>{df.to_string(index=False)}</pre>"

#     await update.message.reply_text(text_table, parse_mode="HTML")


async def handle_cost_by_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User | None = update.effective_user

    logger.info("User `%s` triggered the /costByProduct command", user.username)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Creating report for you, it may take a moment"
    )

    s3 = boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_ADMIN_SA_SECRET_KEY"),
    )

    df = daily.create_top_consumption_by_product_report(s3, bucket=os.getenv("BUCKET"))
    reply = [f"{row.sku_name} - {round(row.cost, 2)} RUB" for row in df.itertuples(index=False)]

    s3.close()

    await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(reply))


async def handle_cost_by_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the /costByService command", user.username)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Creating report for you, it may take a moment"
    )

    s3 = boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_ADMIN_SA_SECRET_KEY"),
    )

    df = daily.create_top_consumption_by_service_report(s3, bucket=os.getenv("BUCKET"))
    reply = [f"{row.service_name} - {round(row.cost, 2)} RUB" for row in df.itertuples(index=False)]

    s3.close()

    await context.bot.send_message(chat_id=update.effective_chat.id, atext="\n".join(reply))


async def handle_get_daily_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the /getDailyReport command", user.username)

    keyboard = [
        [InlineKeyboardButton("By Service", callback_data="by_service")],
        [InlineKeyboardButton("By Product", callback_data="by_product")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Please, specify which report you want to see:", reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "by_service":
        await query.edit_message_text(text="You selected By Service")
        # Add functionality for Option 1 here
    elif query.data == "by_product":
        await query.edit_message_text(text="You selected By Product")
        # Add functionality for Option 2 here
