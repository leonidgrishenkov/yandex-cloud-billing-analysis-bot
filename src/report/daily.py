from datetime import date, datetime

from report import common
import pandas as pd

from utils import logger


def create_top_consumption_by_product_report(s3, bucket: str) -> pd.DataFrame:
    current_date: date = datetime.now().date()

    logger.info("Creating report for current date: %s", current_date)

    report: pd.DataFrame = common.get_report_from_s3(s3, report_date=current_date, bucket=bucket)

    return common.groupby_top_consumption_items(
        report=report,
        groupby=common.GroupBy.PRODUCT,
        top=10,
    )


def create_top_consumption_by_service_report(s3, bucket: str) -> pd.DataFrame:
    current_date: date = datetime.now().date()

    logger.info("Creating report for current date: %s", current_date)

    report: pd.DataFrame = common.get_report_from_s3(s3, report_date=current_date, bucket=bucket)

    return common.groupby_top_consumption_items(
        report=report,
        groupby=common.GroupBy.SERVICE,
        top=10,
    )
