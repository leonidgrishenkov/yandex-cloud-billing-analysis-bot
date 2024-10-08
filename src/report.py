import os
import sys
from datetime import date, datetime
from enum import Enum

import boto3
import dotenv
import pandas as pd
from botocore.exceptions import ClientError

from utils import logger


class GroupBy(Enum):
    SERVICE = "service_name"
    PRODUCT = "sku_name"


def _get_top_consumption(report: pd.DataFrame, by: GroupBy, top: int = 10) -> pd.DataFrame:
    logger.info("Aggregating report by %s with top %s", by.value, top)
    return (
        report.groupby([by.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values("cost", ascending=False)
        .iloc[:top, :]
    )


class NoReportError(Exception): ...


def _get_report(s3, report_date: date, bucket: str) -> pd.DataFrame:
    key: str = f"{report_date.strftime(r'%Y%m%d')}.csv"

    logger.info("Getting %s key from %s bucket", key, bucket)
    try:
        response: dict = s3.get_object(
            Bucket=bucket,
            Key=key,
        )
        logger.info("Response recieved")
        return pd.read_csv(response["Body"])
    except ClientError:
        raise NoReportError(f"There is no report for this date: `{report_date}`") from None


def get_top_consumption_by_product(s3, bucket: str) -> pd.DataFrame:
    report_date: date = datetime.now().date()

    report: pd.DataFrame = _get_report(s3, report_date=report_date, bucket=bucket)

    return _get_top_consumption(
        report=report,
        by=GroupBy.PRODUCT,
        top=10,
    )


def get_top_consumption_by_service(s3, bucket: str) -> pd.DataFrame:
    report_date: date = datetime.now().date()

    report: pd.DataFrame = _get_report(s3, report_date=report_date, bucket=bucket)

    return _get_top_consumption(
        report=report,
        by=GroupBy.SERVICE,
        top=10,
    )


def main() -> ...:
    dotenv.load_dotenv()

    s3 = boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_ADMIN_SA_SECRET_KEY"),
    )
    BUCKET = "yandex-cloud-billing"

    # print(get_top_consumption_by_product(s3, bucket=BUCKET).head(10))

    df = get_top_consumption_by_product(s3, bucket=BUCKET)
    l = []
    for row in df.itertuples(index=False):
        _ = f"{row.sku_name} - {round(row.cost, 2)} RUB"
        l.append(_)

    print("\n".join(l))

    s3.close()

    # report_date: date = datetime.now().date()
    # report_date: date = date(2023, 4, 4)

    # try:
    #     table = get_report(client=s3, report_date=report_date, bucket=BUCKET)

    #     print(
    #         get_top_consumption(
    #             table=table,
    #             type=GroupBy.PRODUCT,
    #         ).head(10)
    #     )

    #     print(
    #         get_top_consumption(
    #             table=table,
    #             type=GroupBy.SERVICE,
    #         ).head(10)
    #     )
    # except NoReportError as err:
    #     logger.exception(err)
    #     sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logger.exception(err)
        sys.exit(1)
