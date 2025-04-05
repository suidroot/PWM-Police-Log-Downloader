#!/usr/bin/env python3

import logging
import config

if config.ENABLE_DISCORD:
    # https://pypi.org/project/python-logging-discord-handler/
    from discord_logging.handler import DiscordHandler


def setup_logger():
    '''
    Set up logging subsystem
    Logging Schema
    FATAL: Program should quit sending error
    ERROR: Non-fatal error can continue operating
    WARNING: Normal Status updates positive activities occurred
    INFO: Verbose normal Status updates all activities occurred
    DEBUG: Full operation debugging including supported libraries
    '''

    logger = logging.getLogger()

    if config.ENABLE_DISCORD:
        discord_handler = DiscordHandler(
            config.DISCORD_NAME,
            config.DISCORD_WEBHOOK_URL )
        discord_format = logging.Formatter(config.LOGGER_DISCORD_FORMAT)
        discord_handler.setFormatter(discord_format)
        logger.addHandler(discord_handler)

    stream_handler = logging.StreamHandler()
    stream_format = logging.Formatter(config.LOGGER_STREAM_FORMAT)
    stream_handler.setFormatter(stream_format)

    # Add the handlers to the Logger
    logger.addHandler(stream_handler)
    logger.setLevel(config.LOGGING_LEVEL)

    return logger