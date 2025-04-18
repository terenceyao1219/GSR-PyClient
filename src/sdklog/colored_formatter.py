import logging

class SdkColoredFormatter(logging.Formatter):
    _showName = False

    def show_name(self, flag: bool) -> 'SdkColoredFormatter':
        self._showName = flag
        return self

    def format(self, record):
        name = ' {' + f'{record.name}' + '} ' if self._showName else ' '
        if record.levelno == logging.NOTSET:
            record.msg = f"\033[37m[NOTE]{name}{record.msg}\033[0m"
        elif record.levelno == logging.DEBUG:
            record.msg = f"\033[94m[DEBG]{name}{record.msg}\033[0m"
        elif record.levelno == logging.INFO:
            record.msg = f"\033[32m[INFO]{name}{record.msg}\033[0m"
        elif record.levelno == logging.WARNING:
            record.msg = f"\033[33m[WARN]{name}{record.msg}\033[0m"
        elif record.levelno == logging.ERROR:
            record.msg = f"\033[31m[ERRO]{name}{record.msg}\033[0m"
        elif record.levelno == logging.CRITICAL:
            record.msg = f"\033[35m[CRIT]{name}{record.msg}\033[0m"
        return super().format(record)
