from datetime import date, datetime, timedelta

import pandas as pd

from bot import config, s3
from bot.reports import groupby
from bot.utils import logger


def create_top_consumption_report(
    groupby: groupby.GroupBy,
) -> pd.DataFrame:
    current_date: date = datetime.now().date()
    report_dates: list[date] = [current_date - timedelta(days=_) for _ in range(30)]
    top = 20

    logger.info("Creating report for these dates: %s", report_dates)

    reports: list[pd.DataFrame] = []
    for report_date in report_dates:
        try:
            reports.append(
                s3.read_file(
                    key=f"{report_date.strftime(r'%Y%m%d')}.csv",
                    bucket=config.S3_BUCKET_NAME,
                )
            )
        except FileNotFoundError as err:
            logger.warning("%s, skipping", err)
            continue

    report: pd.DataFrame = pd.concat(reports)

    logger.info("Aggregating report by `%s` with top `%s`", groupby.value, top)

    return (
        report.groupby([groupby.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values("cost", ascending=False)
        .iloc[:top, :]
    )
