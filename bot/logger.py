import logging
from logging.handlers import TimedRotatingFileHandler

from bot import config


def _create_logger() -> logging.Logger:

    if not config.LOG_DIR.exists():
        config.LOG_DIR.mkdir()

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
        filename=config.LOG_DIR / "app.log",
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
        # Decrease `httpx` package log level bacause it's too verbose
        # and also writes encrypted bot token.
        if extlogger.name == "httpx":
            extlogger.setLevel(logging.WARNING)
        else:
            extlogger.setLevel(level)

        extlogger.addHandler(handler)

    return logger


logger = _create_logger()
