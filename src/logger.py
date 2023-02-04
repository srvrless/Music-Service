from structlog import getLogger


def get_logger(context: dict = None):  # type:ignore
    """get logger"""

    logger = getLogger()

    if context:
        logger = logger.bind(**context)

    return logger
