"""
FILE: log_utils.py

DESCRIPTION:
    This module provides utility functions for logging within the application.
"""

import logging


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.

    Attributes:
        name (str): The name of the logger.
        level (int): The logging level (default is logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger


def log_loop_status(
    logger: logging.Logger,
    loop_idx: int,
    total_elements: int,
    log_msg: str,
    log_pace: int = 50
) -> None:
    """
    Logs the progress of a loop processing stock tickers at specified intervals.

    At every `log_pace` iterations, this method logs the number of tickers processed,
    the number remaining, and the percentage of completion.

    Args:
        logger (logging.Logger): The logger instance to use for logging.
        loop_idx (int): The current index of the loop iteration.
        total_elements (int): The total number of elements to process.
        log_pace (int): The interval at which to log progress. Default is 50.
    """

    if loop_idx > 0 and loop_idx % log_pace == 0:
        num_elements_left = total_elements - loop_idx
        pct_elements_left = round(100 * (1 - (num_elements_left / total_elements)), 2)
        logger.info(f"{log_msg}. There are {num_elements_left} remaining "
                    f"({pct_elements_left}% completed)")
