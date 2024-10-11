import logging
import os
from datetime import date, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import boto3
import dotenv

dotenv.load_dotenv()


def get_s3_instance() -> ...:
    return boto3.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.getenv("YC_S3_ADMIN_SA_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YC_S3_ADMIN_SA_SECRET_KEY"),
    )


AUTHORIZED_USERS = (196255068,)


def _create_logger() -> logging.Logger:
    today: date = date.today()
    current_week = today - timedelta(days=today.weekday())

    log_dir: Path = Path(__file__).parents[1] / "logs" / current_week.strftime(r"%Y-%m-%d")
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    current_date_log_file: Path = log_dir / (today.strftime(r"%Y-%m-%d") + ".log")

    levels: dict = dict(
        info=logging.INFO,
        debug=logging.DEBUG,
        warn=logging.WARN,
        warning=logging.WARN,
        fatal=logging.FATAL,
        error=logging.ERROR,
    )

    try:
        level: int = levels[os.getenv("APP_LOG_LEVEL", "info")]
    except KeyError:
        level: int = logging.INFO

    logger: logging.Logger = logging.getLogger(name="__this_bot__")
    logger.setLevel(level)

    handler = TimedRotatingFileHandler(
        filename=log_dir / current_date_log_file,
        # when="W0",  # Rotate logs every week on Monday
        when="midnight",
        interval=1,  # Interval is set to 1 week
        backupCount=30,  # Keep 4 backup copies of the log file
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        fmt=r"[%(asctime)s] {%(name)s:%(module)s.%(funcName)s:%(lineno)d} %(levelname)s: %(message)s",
        datefmt=r"%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # To get all logger instances for project:
    # loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for extlogger in (
        logging.getLogger(_name) for _name in ("boto3", "botocore", "httpx", "telegram", "dotenv")
    ):
        # Decrease `httpx` package log level bacause it's to verbose
        # and also writes encrypted bot token.
        if extlogger.name == "httpx":
            extlogger.setLevel(logging.WARNING)
        else:
            extlogger.setLevel(level)

        extlogger.addHandler(handler)

    return logger


logger = _create_logger()
