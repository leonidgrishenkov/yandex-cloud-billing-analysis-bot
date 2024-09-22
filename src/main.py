import os
from pprint import pprint

import boto3
import dotenv

import pandas as pd


def convert_bytes_to_mb(n: int) -> float:
    if isinstance(n, str):
        n = int(n)
    return round(n / 1_000_000, 4)


def list_buckets(client) -> ...:
    pprint(client.list_buckets())


def list_bucket_objects(client, bucket: str) -> ...:
    response = client.list_objects(
        Bucket=bucket,
        MaxKeys=5,
    )

    for item in response["Contents"]:
        print(
            f"key={item['Key']} modified_at={item['LastModified'].strftime(r'%Y-%m-%d %H:%M:%S')} UTC size={convert_bytes_to_mb(item['Size'])} MB"
        )


def main() -> ...:
    dotenv.load_dotenv()

    session = boto3.session.Session()
    client = session.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_ADMIN_SA_SECRET_KEY"),
    )
    BUCKET = "yandex-cloud-billing"

    # list_bucket_objects(client=client, bucket=BUCKET)

    r = client.get_object(
        Bucket=BUCKET,
        Key="20240922.csv",
    )
    frame = pd.read_csv(r["Body"])

    print(frame.columns)


if __name__ == "__main__":
    main()
