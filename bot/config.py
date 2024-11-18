import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")

YC_S3_ENDPOINT_URL: str = "https://storage.yandexcloud.net"
YC_S3_ADMIN_SA_ACCESS_KEY: str = os.getenv("YC_S3_ADMIN_SA_ACCESS_KEY")
YC_S3_ADMIN_SA_SECRET_KEY: str = os.getenv("YC_S3_ADMIN_SA_SECRET_KEY")

YC_OAUTH_TOKEN = os.getenv("YC_OAUTH_TOKEN")
YC_BILLING_ACC_ID = os.getenv("YC_BILLING_ACC_ID")

APP_LOG_LEVEL: str = os.getenv("APP_LOG_LEVEL", "info")
LOG_DIR: Path = Path(__file__).parents[1] / "logs"

DB_PATH: Path = Path(__file__).parents[0] / "sql/db.sqlite3"

if not YC_S3_ADMIN_SA_SECRET_KEY or not YC_S3_ADMIN_SA_ACCESS_KEY:
    raise ValueError(
        "Both `YC_S3_ADMIN_SA_SECRET_KEY` and `YC_S3_ADMIN_SA_ACCESS_KEY` env variables "
        "are required to interact with S3 bucket"
    )

if not YC_OAUTH_TOKEN or not YC_BILLING_ACC_ID:
    raise ValueError(
        "Both `YC_OAUTH_TOKEN` and `YC_BILLING_ACC_ID` env variables "
        "are required to interact with Yandex Cloud API"
    )

if not S3_BUCKET_NAME:
    raise ValueError("`S3_BUCKET_NAME` env variable is required")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("`TELEGRAM_BOT_TOKEN` env variable is required")
