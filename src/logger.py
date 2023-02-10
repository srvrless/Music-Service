import os

from loguru import logger
from structlog import getLogger

from src.core.settings import BASEDIR, LOGDIR, LOGFILE

LOGDIR = BASEDIR + "/" + LOGDIR
if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)
logger.add(
    LOGDIR + "/" + LOGFILE,
    rotation="25MB",
    colorize=True,
    format="<green>{time:YYYYMMDD_HH:mm:ss}</green> | {level} | <level>{message}</level>",
    level="ERROR",
)


def get_logger(context: dict = None):
    """get logger"""

    logger = getLogger()

    if context:
        logger = logger.bind(**context)

    return logger
