import logging
import os
import sys

import boto3

logging.basicConfig(
    level=logging.INFO,
    format=r"[%(asctime)s] {%(module)s.%(funcName)s:%(lineno)d} %(levelname)s: %(message)s",
    datefmt=r"%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(name="yandex-cloud-billing-analysis")
# Desrease `httpx` log level because it's too verbose.
logging.getLogger("httpx").setLevel(logging.WARNING)


def get_s3_instance() -> ...:
    return boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_ADMIN_SA_SECRET_KEY"),
    )
