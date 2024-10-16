import logging
from datetime import date, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from bot import config


def _create_logger() -> logging.Logger:
    today: date = date.today()
    current_week = today - timedelta(days=today.weekday())

    log_dir: Path = config.LOG_DIR / current_week.strftime(r"%Y-%m-%d")
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
        level: int = levels[config.APP_LOG_LEVEL]
    except KeyError:
        level: int = logging.INFO

    logger: logging.Logger = logging.getLogger(name="__bot__")
    logger.setLevel(level)

    handler = TimedRotatingFileHandler(
        filename=log_dir / current_date_log_file,
        when="midnight",
        interval=1,
        backupCount=30,
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
