"""
Version: v1
Copyright: Jonathan Cabezas, 8a rue Victor Huen 68000 Colmar

Magical IO (MIO), a module to produce my scripts outputs/logging at once.

Changelog:

- v1 (2023-07-28)
    *
"""

import os
import sys
import logging

from pathlib import Path
from mio.handlers import LogHistoryHandler, ExitOnCriticalHandler
from mio.formatters import CustomFormatter, level, increment_level, decrement_level
from mio.filters import ExcludeErrorsFilter
from mio.decorators import run_only_once
from mio.exceptions import install_excepthook
from mio.utils.enclose import enclose

#
#     At Exit Handlers
#

installed = False


def add_confirmation_text_at_exit(text):
    import atexit

    @atexit.register
    def exit_input():
        input("\n" + text)


#
#     Sections
#


class Section:
    def __init__(self, title, *args):
        self.title = title
        self.args = args

    def __enter__(self):
        __beginsection__(self.title, *self.args)
        return self

    def __exit__(self, type, value, traceback):
        __endsection__()
        return type is None


def __beginsection__(title, *args):
    if not installed:
        return

    if level == -1:
        for logging_args in enclose(title, *args):
            logging.info(*logging_args, extra={"use_bullet": False})
    else:
        logging.info(title, *args)
    increment_level()


def __endsection__():
    if not installed:
        return

    decrement_level()


#
#     Warnings
#


def summarize_warnings(title):
    history.stop()

    warnings = history.get_warnings()
    if warnings:
        with Section(title):
            for warning in warnings:
                logging.warning(warning[0], *warning[1])

    history.resume()

    return


#
#     Logger installation
#

history = LogHistoryHandler()


@run_only_once
def install_logger(path: Path, debug: bool):
    global installed
    installed = True

    os.system("")  # enables ansi escape characters in terminal
    install_excepthook()

    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    console_formatter = CustomFormatter(format="%(message)s", use_colors=True)
    file_formatter = CustomFormatter(
        format="%(asctime)s %(levelname)-8s %(message)s", handle_date=True
    )

    # Setting up stderr
    console_stderr_handler = logging.StreamHandler(sys.stderr)
    console_stderr_handler.setLevel(logging.ERROR)
    console_stderr_handler.setFormatter(console_formatter)

    # Setting up stdout
    console_stdout_handler = logging.StreamHandler(sys.stdout)
    console_stdout_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_stdout_handler.setFormatter(console_formatter)

    # Exclusing errors from stdout
    exclude_errors_filter = ExcludeErrorsFilter()
    console_stdout_handler.addFilter(exclude_errors_filter)

    # Setting up the log files
    file_handler = logging.FileHandler(path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Adding the handlers to the root Logger
    logger.addHandler(history)
    logger.addHandler(console_stderr_handler)
    logger.addHandler(console_stdout_handler)
    logger.addHandler(file_handler)
    logger.addHandler(ExitOnCriticalHandler())
