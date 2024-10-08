from datetime import date, datetime, timedelta

import common
import pandas as pd

from utils import logger


def create_top_consumption_by_service_report(s3, bucket: str) -> pd.DataFrame:
    current_date: date = datetime.now().date()
    report_dates: list[date] = [current_date - timedelta(days=x) for x in range(7)]

    logger.info("Creating report for these dates: %s", report_dates)

    reports: list[pd.DataFrame] = []
    for report_date in report_dates:
        try:
            reports.append(common.get_report_from_s3(s3, report_date=report_date, bucket=bucket))
        except common.NoReportError as err:
            logger.warning("%s, skipping", err)
            continue

    return common.groupby_top_consumption_items(
        report=pd.concat(reports),
        groupby=common.GroupBy.SERVICE,
        top=15,
    )


def create_top_consumption_by_product_report(s3, bucket: str) -> pd.DataFrame:
    current_date: date = datetime.now().date()
    report_dates: list[date] = [current_date - timedelta(days=x) for x in range(7)]

    logger.info("Creating report for these dates: %s", report_dates)

    reports: list[pd.DataFrame] = []
    for report_date in report_dates:
        try:
            reports.append(common.get_report_from_s3(s3, report_date=report_date, bucket=bucket))
        except common.NoReportError as err:
            logger.warning("%s, skipping", err)
            continue

    return common.groupby_top_consumption_items(
        report=pd.concat(reports),
        groupby=common.GroupBy.PRODUCT,
        top=15,
    )
