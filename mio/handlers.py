import logging
import sys

from ordered_set import OrderedSet


class LogHistoryHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.history = {}
        self.enabled = True

    def history_entry(self, record):
        return (record.msg, record.args)

    def emit(self, record):
        if not self.enabled:
            return

        level = record.levelno
        history_entry = self.history_entry(record)

        if level not in self.history:
            self.history[level] = OrderedSet()

        if history_entry not in self.history[level]:
            self.history[level].add(history_entry)

    def get_warnings(self):
        if logging.WARNING not in self.history:
            return []

        return self.history[logging.WARNING]

    def stop(self):
        self.enabled = False

    def resume(self):
        self.enabled = True


class ExitOnCriticalHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.setLevel(logging.CRITICAL)

    def emit(self, record):
        if record.levelno == logging.CRITICAL:
            sys.exit(1)


"""
class AdminEmailHandler(logging.Handler):
    An exception log handler that emails log entries to site admins.

    If the request is passed as the first argument to the log record,
    request data will be provided in the email report.

    def __init__(self, include_html=False, email_backend=None, reporter_class=None):
        super().__init__()
        self.include_html = include_html
        self.email_backend = email_backend
        self.reporter_class = import_string(
            reporter_class or settings.DEFAULT_EXCEPTION_REPORTER
        )

    def emit(self, record):
        try:
            request = record.request
            subject = "%s (%s IP): %s" % (
                record.levelname,
                (
                    "internal"
                    if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
                    else "EXTERNAL"
                ),
                record.getMessage(),
            )
        except Exception:
            subject = "%s: %s" % (record.levelname, record.getMessage())
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = self.reporter_class(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (
            self.format(no_exc_record),
            reporter.get_traceback_text(),
        )
        html_message = reporter.get_traceback_html() if self.include_html else None
        self.send_mail(subject, message, fail_silently=True, html_message=html_message)

    def send_mail(self, subject, message, *args, **kwargs):
        mail.mail_admins(
            subject, message, *args, connection=self.connection(), **kwargs
        )

    def connection(self):
        return get_connection(backend=self.email_backend, fail_silently=True)

    def format_subject(self, subject):
        #Escape CR and LF characters.
        return subject.replace("\n", "\\n").replace("\r", "\\r")
"""
