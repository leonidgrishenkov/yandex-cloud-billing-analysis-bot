from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

if TYPE_CHECKING:

    from pandas import DataFrame

    from bot.reports.groupby import GroupBy

from bot.logger import logger
from bot.reports.common import create_report


def create_top_consumption_report(
    groupby: GroupBy,
) -> DataFrame:
    current_datetime: datetime = datetime.now().astimezone(ZoneInfo("Europe/Moscow"))
    report_dates: list[date] = [(current_datetime - timedelta(days=day)).date() for day in range(30)]

    logger.info("Creating monthly report for these dates: %s", report_dates)

    report = create_report(
        report_date=report_dates,
        dbtable="monthly_report",
        current_datetime=current_datetime,
    )

    logger.info("Aggregating report by `%s`", groupby.value)

    return (
        report.groupby([groupby.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values("cost", ascending=False)
    )
