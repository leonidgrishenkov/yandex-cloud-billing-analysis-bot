from datetime import date
from enum import Enum

import pandas as pd
from botocore.exceptions import ClientError

from utils import logger


class GroupBy(Enum):
    SERVICE = "service_name"
    PRODUCT = "sku_name"


def groupby_top_consumption_items(
    report: pd.DataFrame,
    groupby: GroupBy,
    top: int = 10,
) -> pd.DataFrame:
    logger.info("Aggregating report by `%s` with top `%s`", groupby.value, top)
    return (
        report.groupby([groupby.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values("cost", ascending=False)
        .iloc[:top, :]
    )


class NoReportError(Exception): ...


def get_report_from_s3(s3, report_date: date, bucket: str) -> pd.DataFrame:
    key: str = f"{report_date.strftime(r'%Y%m%d')}.csv"

    logger.info("Getting `%s` key from `%s` bucket", key, bucket)
    try:
        response: dict = s3.get_object(
            Bucket=bucket,
            Key=key,
        )
        logger.info("Response recieved")
        return pd.read_csv(response["Body"])
    except ClientError:
        raise NoReportError(f"There is no report for this date: `{report_date}`") from None
