import logging


class ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR
