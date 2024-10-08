import os

import dotenv
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from report import daily, weekly
from utils import get_s3_instance, logger

dotenv.load_dotenv()


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when the command /start is issued."""
    user: User | None = update.effective_user

    logger.info("User `%s` triggered the /start command", user.username)

    await update.message.reply_html(
        text=rf"Hi {user.mention_html()}! Please, use one of available commands.",
        reply_markup=ForceReply(selective=True),
    )


async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when the command /help is issued."""
    user: User | None = update.effective_user

    logger.info("User `%s` triggered the /help command", user.username)

    await update.message.reply_text(text="This is a help page")


async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    """Send a message when unknown command is issued."""
    user: User | None = update.effective_user

    logger.info("User `%s` specified unknown command", user.username)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. 🤷 Please, use one of available commands.",
    )


async def handle_daily_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the `/daily_report` command", user.username)

    keyboard = [
        [InlineKeyboardButton("By Service", callback_data="daily_by_service")],
        [InlineKeyboardButton("By Product", callback_data="daily_by_product")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info("Waiting for `%s` user to click the button", user.username)
    await update.message.reply_text(
        "Please, specify which report you want to see:", reply_markup=reply_markup
    )


async def handle_weekly_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User | None = update.effective_user
    logger.info("User `%s` triggered the `/weekly_report` command", user.username)

    keyboard = [
        [InlineKeyboardButton(text="By Service", callback_data="weekly_by_service")],
        [InlineKeyboardButton("By Product", callback_data="weekly_by_product")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info("Waiting for `%s` user to click the button", user.username)
    await update.message.reply_text(
        "Please, specify which report you want to see:", reply_markup=reply_markup
    )


async def handle_callback_query_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User | None = update.effective_user

    query = update.callback_query
    await query.answer()

    if query.data == "daily_by_service":
        await query.edit_message_text(
            text="Creating daily report by service, it may take a while. 😉"
        )
        logger.info("User `%s` chose `by_service` button of `/daily_report` command", user.username)

        s3 = get_s3_instance()
        report = daily.create_top_consumption_by_service_report(s3, bucket=os.getenv("BUCKET"))
        reply = [
            f"<b>{row.service_name}:</b> {round(row.cost, 2)} RUB"
            for row in report.itertuples(index=False)
        ]
        s3.close()

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="\n".join(reply), parse_mode=ParseMode.HTML
        )

    elif query.data == "daily_by_product":
        await query.edit_message_text(
            text="Creating daily report by product, it may take a while. 😉"
        )
        logger.info("User `%s` chose `by_product` button of `/daily_report` command", user.username)

        s3 = get_s3_instance()
        report = daily.create_top_consumption_by_product_report(s3, bucket=os.getenv("BUCKET"))
        reply = [
            f"<b>{row.sku_name}:</b> {round(row.cost, 2)} RUB"
            for row in report.itertuples(index=False)
        ]
        s3.close()

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="\n".join(reply), parse_mode=ParseMode.HTML
        )

    elif query.data == "weekly_by_service":
        await query.edit_message_text(
            text="Creating weekly report by service, it may take a while. 😉"
        )
        logger.info(
            "User `%s` chose `by_service` button of `/weekly_report` command", user.username
        )

        s3 = get_s3_instance()
        report = weekly.create_top_consumption_by_service_report(s3, bucket=os.getenv("BUCKET"))
        reply = [
            f"<b>{row.service_name}:</b> {round(row.cost, 2)} RUB"
            for row in report.itertuples(index=False)
        ]
        s3.close()

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="\n".join(reply), parse_mode=ParseMode.HTML
        )

    elif query.data == "weekly_by_product":
        await query.edit_message_text(
            text="Creating weekly report by product, it may take a while. 😉"
        )
        logger.info(
            "User `%s` chose `by_product` button of `/weekly_report` command", user.username
        )

        s3 = get_s3_instance()
        report = weekly.create_top_consumption_by_product_report(s3, bucket=os.getenv("BUCKET"))
        reply = [
            f"<b>{row.sku_name}:</b> {round(row.cost, 2)} RUB"
            for row in report.itertuples(index=False)
        ]
        s3.close()

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="\n".join(reply), parse_mode=ParseMode.HTML
        )
