import atexit
import os
import sys
from datetime import date, datetime
from enum import Enum
from pprint import pprint

import boto3
import dotenv
import pandas as pd
from botocore.exceptions import ClientError

from utils import logger


def convert_bytes_to_mb(n: int) -> float:
    if isinstance(n, str):
        n = int(n)
    return round(n / 1_000_000, 4)


def list_buckets(client) -> ...:
    pprint(client.list_buckets())


def list_bucket_objects(client, bucket: str) -> ...:
    response = client.list_objects(
        Bucket=bucket,
        MaxKeys=100,
    )

    for item in response["Contents"]:
        print(
            f"key={item['Key']} modified_at={item['LastModified'].strftime(r'%Y-%m-%d %H:%M:%S')} UTC size={convert_bytes_to_mb(item['Size'])} MB"
        )


class By(Enum):
    SERVICE = "service_name"
    PRODUCT = "sku_name"


def get_top_consumption(table: pd.DataFrame, by: By, top: int = 10) -> pd.DataFrame:
    return (
        table.groupby([by.value], as_index=False)
        .agg({"cost": "sum"})
        .sort_values("cost", ascending=False)
        .iloc[:top, :]
    )


class NoReportError(Exception): ...


def get_report(client, report_date: date, bucket: str) -> pd.DataFrame:
    key: str = f"{report_date.strftime(r'%Y%m%d')}.csv"
    try:
        response: dict = client.get_object(
            Bucket=bucket,
            Key=key,
        )
        return pd.read_csv(response["Body"])
    except ClientError:
        raise NoReportError(f"There is no report for this date: `{report_date}`") from None


def main() -> ...:
    dotenv.load_dotenv()

    s3 = boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_ADMIN_SA_SECRET_KEY"),
    )
    atexit.register(s3.close)
    BUCKET = "yandex-cloud-billing"

    # report_date: date = datetime.now().date()
    report_date: date = date(2023, 4, 4)

    try:
        table = get_report(client=s3, report_date=report_date, bucket=BUCKET)

        print(
            get_top_consumption(
                table=table,
                by=By.PRODUCT,
            ).head(10)
        )

        print(
            get_top_consumption(
                table=table,
                by=By.SERVICE,
            ).head(10)
        )
    except NoReportError as err:
        logger.exception(err)
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logger.exception(err)
        sys.exit(1)
