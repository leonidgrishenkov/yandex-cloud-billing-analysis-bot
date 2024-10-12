import os
import dotenv

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "not_set")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "not_set")

YC_S3_ENDPOINT_URL = "https://storage.yandexcloud.net"
YC_S3_ADMIN_SA_ACCESS_KEY = os.getenv("YC_S3_ADMIN_SA_ACCESS_KEY", "not_set")
YC_S3_ADMIN_SA_SECRET_KEY = os.getenv("YC_S3_ADMIN_SA_SECRET_KEY", "not_set")

APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "info")
