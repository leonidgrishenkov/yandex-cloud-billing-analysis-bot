import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format=r"[%(asctime)s] {%(module)s.%(funcName)s:%(lineno)d} %(levelname)s: %(message)s",
    datefmt=r"%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(name="yandex-cloud-billing-analysis")
# Desrease `httpx` log level because it's too verbose.
logging.getLogger("httpx").setLevel(logging.WARNING)
