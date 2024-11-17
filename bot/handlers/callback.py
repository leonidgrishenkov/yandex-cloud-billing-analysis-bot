from typing import cast

from telegram import Update, User
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.reports import daily, groupby, monthly, weekly
from bot.templater import render_template
from bot.logger import logger


async def handle_callback_query_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ...:
    user: User = cast(User, update.effective_user)

    query = update.callback_query
    await query.answer()

    if query.data == "daily_by_service":
        await query.edit_message_text(text=render_template(name="creating.tpl"))
        logger.info(
            "User `%s` chose `daily_by_service` button of `/daily_report` command", user.username
        )

        report = daily.create_top_consumption_report(
            groupby.GroupBy.SERVICE,
        )
        reply = render_template(
            name="service.tpl",
            values=dict(
                report_type="daily",
                rows=(row for row in report.iloc[:10, :].itertuples(index=False)),
                total=sum(row.cost for row in report.itertuples(index=False)),
            ),
        )

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply,
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "daily_by_product":
        await query.edit_message_text(text=render_template(name="creating.tpl"))
        logger.info(
            "User `%s` chose `daily_by_product` button of `/daily_report` command", user.username
        )

        report = daily.create_top_consumption_report(
            groupby.GroupBy.PRODUCT,
        )
        reply = render_template(
            name="product.tpl",
            values=dict(
                report_type="daily",
                rows=(row for row in report.iloc[:10, :].itertuples(index=False)),
                total=sum(row.cost for row in report.itertuples(index=False)),
            ),
        )

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML
        )

    elif query.data == "weekly_by_service":
        await query.edit_message_text(text=render_template(name="creating.tpl"))
        logger.info(
            "User `%s` chose `weekly_by_service` button of `/weekly_report` command", user.username
        )

        report = weekly.create_top_consumption_report(
            groupby.GroupBy.SERVICE,
        )
        reply = render_template(
            name="service.tpl",
            values=dict(
                report_type="weekly",
                rows=(row for row in report.iloc[:15, :].itertuples(index=False)),
                total=sum(row.cost for row in report.itertuples(index=False)),
            ),
        )

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML
        )

    elif query.data == "weekly_by_product":
        await query.edit_message_text(text=render_template(name="creating.tpl"))
        logger.info(
            "User `%s` chose `weekly_by_product` button of `/weekly_report` command", user.username
        )

        report = weekly.create_top_consumption_report(
            groupby.GroupBy.PRODUCT,
        )

        reply = render_template(
            name="product.tpl",
            values=dict(
                report_type="weekly",
                rows=(row for row in report.iloc[:15, :].itertuples(index=False)),
                total=sum(row.cost for row in report.itertuples(index=False)),
            ),
        )

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML
        )

    elif query.data == "monthly_by_service":
        await query.edit_message_text(text=render_template(name="creating.tpl"))
        logger.info(
            "User `%s` chose `monthly_by_service` button of `/monthly_report` command",
            user.username,
        )

        report = monthly.create_top_consumption_report(
            groupby.GroupBy.SERVICE,
        )
        reply = render_template(
            name="service.tpl",
            values=dict(
                report_type="monthly",
                rows=(row for row in report.iloc[:15, :].itertuples(index=False)),
                total=sum(row.cost for row in report.itertuples(index=False)),
            ),
        )

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML
        )

    elif query.data == "monthly_by_product":
        await query.edit_message_text(text=render_template(name="creating.tpl"))
        logger.info(
            "User `%s` chose `monthly_by_product` button of `/monthly_report` command",
            user.username,
        )

        report = monthly.create_top_consumption_report(
            groupby.GroupBy.PRODUCT,
        )

        reply = render_template(
            name="product.tpl",
            values=dict(
                report_type="monthly",
                rows=(row for row in report.iloc[:15, :].itertuples(index=False)),
                total=sum(row.cost for row in report.itertuples(index=False)),
            ),
        )

        logger.info("Report created, sending back to user")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.HTML
        )
