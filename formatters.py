import time
import logging
import re

from mio.consts import (
    COLOR_CODES,
    DEFAULT_DATE_FORMAT,
    CUSTOM_ASCTIME,
    SUCCESS,
    SUCCESS_KEYWORDS,
    FAILURE,
    FAILURE_KEYWORDS,
    BULLET_CHARACTERS,
    INDENTATION,
    BRACES_PATTERN,
)
from utils.strings import unaccentuate

level = -1


def increment_level():
    global level
    level += 1


def decrement_level():
    global level
    level -= 1


# Inspired by
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class CustomFormatter(logging.Formatter):
    ARGS_COLORS = [COLOR_CODES["MAGENTA"], COLOR_CODES["CYAN"]]
    LOGGERS_COLORS = {
        logging.DEBUG: COLOR_CODES["WHITE"],
        logging.INFO: COLOR_CODES["WHITE"],
        logging.WARNING: COLOR_CODES["YELLOW"],
        logging.ERROR: COLOR_CODES["RED"],
        logging.CRITICAL: COLOR_CODES["BOLD"] + COLOR_CODES["RED"],
        SUCCESS: COLOR_CODES["BOLD"] + COLOR_CODES["GREEN"],
        FAILURE: COLOR_CODES["BOLD"] + COLOR_CODES["RED"],
    }

    def __init__(
        self,
        format: str,
        datefmt: str = DEFAULT_DATE_FORMAT,
        handle_date: bool = False,
        use_colors: bool = False,
        indent_levels: bool = True,
    ):
        self.datefmt = datefmt
        self.last_date = None

        self.handle_date = handle_date
        self.use_colors = use_colors
        self.indent_levels = indent_levels

        self.args_index = 0

        date_size = self.compute_date_size()
        if handle_date:
            format = format.replace("%(asctime)s", f"%({CUSTOM_ASCTIME})-{date_size}s")

        super().__init__(format, datefmt)

    def rewrite_record(self, record: logging.LogRecord):
        self.replace_braces(record)
        if self.indent_levels:
            self.indent(record)
        if self.handle_date:
            self.add_date(record)

    def compute_date_size(self):
        current_time = time.localtime()
        current_time_str = time.strftime(self.datefmt, current_time)

        return len(current_time_str)

    def indent(self, record):
        global level
        use_bullet = getattr(record, "use_bullet", True)
        n = len(BULLET_CHARACTERS)

        if level >= n:
            level = n - 1

        if level >= 0:
            bullet_character = BULLET_CHARACTERS[level] if use_bullet else " "
            record.msg = INDENTATION * level + f"{bullet_character} {record.msg}"

    def add_date(self, record: logging.LogRecord):
        date = time.localtime(record.created)
        date_str = time.strftime(self.datefmt, date)

        # Only showing the date when it's not the same as the last one
        if self.last_date == date_str:
            date_str = ""
        else:
            self.last_date = date_str

        setattr(record, CUSTOM_ASCTIME, date_str)

    def replace_braces(self, record: logging.LogRecord):
        msg = ""
        braces_count = 0

        arg_color = ""
        # Processing the arg braces
        for m in re.finditer(BRACES_PATTERN, record.msg):
            if self.use_colors:
                arg_color = CustomFormatter.ARGS_COLORS[self.args_index]
            msg += f"{m.group(1)}{arg_color}{m.group(2)}{self.msg_color}{m.group(3)}"
            braces_count += 1
            self.args_index = (self.args_index + 1) % len(CustomFormatter.ARGS_COLORS)

        if braces_count > 0:
            record.msg = msg.format(*record.args)
            record.args = ()

    def find_msg_color(self, record):
        # Setting up the message color
        if self.use_colors:
            self.msg_color = CustomFormatter.LOGGERS_COLORS[record.levelno]
            self.check_keywords(record)
        else:
            self.msg_color = ""

    def check_keywords(self, record):
        unaccentuated = unaccentuate(
            record.msg.lower() + "".join((str(arg).lower() for arg in record.args))
        )
        if any(keyword in unaccentuated for keyword in SUCCESS_KEYWORDS):
            self.msg_color = CustomFormatter.LOGGERS_COLORS[SUCCESS]
        if any(keyword in unaccentuated for keyword in FAILURE_KEYWORDS):
            self.msg_color = CustomFormatter.LOGGERS_COLORS[FAILURE]

    def colorize(self, output):
        if not self.use_colors:
            return output

        return self.msg_color + output + COLOR_CODES["RESET"]

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args

        self.find_msg_color(record)
        self.rewrite_record(record)
        output = super().format(record)
        # Adding color if needed
        output = self.colorize(output)

        record.msg = orig_msg
        record.args = orig_args

        return output
