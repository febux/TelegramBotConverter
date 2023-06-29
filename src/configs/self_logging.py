import logging


logging.basicConfig(
    format="%(asctime)s::[%(levelname)s]::%(name)s::(%(filename)s).%(funcName)s(%(lineno)d)::%(message)s",
    datefmt='%d.%m.%Y %I:%M:%S %p', level=logging.INFO,
)

logging.getLogger("aiogram").setLevel(logging.INFO)
logging.getLogger("root").setLevel(logging.INFO)

self_logging = logging
