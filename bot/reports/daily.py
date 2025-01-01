from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from bot.logger import logger
from bot.reports.common import create_report

if TYPE_CHECKING:
    from pandas import DataFrame

    from bot.reports.groupby import GroupBy

def create_top_consumption_report(
    groupby: GroupBy,
) -> DataFrame:
    current_datetime: datetime = datetime.now().astimezone(ZoneInfo("Europe/Moscow"))
    report_date: date = current_datetime.date()

    logger.info("Creating daily report for this date: '%s'", report_date)

    report = create_report(
        report_date=report_date,
        dbtable = "daily_report",
        current_datetime=current_datetime,
    )

    logger.info("Aggregating report by '%s'", groupby.value)

    return (
        report.groupby([groupby.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values(by="cost", ascending=False)
    )
