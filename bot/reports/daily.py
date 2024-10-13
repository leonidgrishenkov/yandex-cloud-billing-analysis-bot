from datetime import date, datetime

import pandas as pd

from bot import config, s3
from bot.reports import groupby
from bot.utils import logger


def create_top_consumption_report(
    groupby: groupby.GroupBy,
) -> pd.DataFrame:
    current_date: date = datetime.now().date()
    top = 10
    logger.info("Creating report for current date: `%s`", current_date)

    report: pd.DataFrame = s3.read_file(
        key=f"{current_date.strftime(r'%Y%m%d')}.csv",
        bucket=config.S3_BUCKET_NAME,
    )

    logger.info("Aggregating report by `%s` with top `%s`", groupby.value, top)

    return (
        report.groupby([groupby.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values("cost", ascending=False)
        .iloc[:top, :]
    )