import boto3
import config
import pandas as pd
from utils import logger


def get_instance() -> ...:
    if not getattr(get_instance, "_s3", None):
        logger.debug("Initializing new s3 connection")

        _s3 = boto3.client(
            service_name="s3",
            endpoint_url=config.YC_S3_ENDPOINT_URL,
            aws_access_key_id=config.YC_S3_ADMIN_SA_ACCESS_KEY,
            aws_secret_access_key=config.YC_S3_ADMIN_SA_SECRET_KEY,
        )
        get_instance._s3 = _s3
    else:
        logger.debug("Using existing one s3 connection")
    return get_instance._s3


def read_file(key: str, bucket: str) -> pd.DataFrame:
    logger.info("Getting `%s` key from `%s` bucket", key, bucket)

    _s3 = get_instance()

    try:
        response: dict = _s3.get_object(
            Bucket=bucket,
            Key=key,
        )
        logger.info("Response recieved")

        return pd.read_csv(response["Body"])

    except _s3.exceptions.NoSuchKey:
        raise FileNotFoundError("There is no file with such key: `%s`", key) from None
