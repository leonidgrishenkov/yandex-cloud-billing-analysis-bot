import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format=r"[%(asctime)s] {%(module)s.%(funcName)s:%(lineno)d} %(levelname)s: %(message)s",
    datefmt=r"%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger()

