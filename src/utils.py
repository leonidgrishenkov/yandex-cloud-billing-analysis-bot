import logging
import os
import sys

import boto3
import dotenv

dotenv.load_dotenv()

_levels = dict(
    info=logging.INFO,
    debug=logging.DEBUG,
    warn=logging.WARN,
    warning=logging.WARN,
    fatal=logging.FATAL,
    error=logging.ERROR,
)

try:
    _level = _levels[os.getenv("APP_LOG_LEVEL", "info")]
except KeyError:
    _level = logging.INFO

logging.basicConfig(
    level=_level,
    format=r"[%(asctime)s] {%(module)s.%(funcName)s:%(lineno)d} %(levelname)s: %(message)s",
    datefmt=r"%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(name="yandex-cloud-billing-analysis-bot")
# Desrease `httpx` log level because it's too verbose.
logging.getLogger("httpx").setLevel(logging.WARNING)


def get_s3_instance() -> ...:
    return boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_S3_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_S3_ADMIN_SA_SECRET_KEY"),
    )


AUTHORIZED_USERS = (196255068,)
