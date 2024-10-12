from datetime import date, datetime

import config
import pandas as pd
import s3
from utils import logger

from reports import common


def create_top_consumption_report(
    groupby: common.GroupBy,
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
