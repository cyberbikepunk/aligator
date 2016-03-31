""" Configure a logger for the application. """


from logging import INFO, DEBUG, getLogger, FileHandler, Formatter, StreamHandler
from logentries import LogentriesHandler
from sys import stdout

from app import app


# noinspection PyIncorrectDocstring
def get_custom_logger(name):
    """ Set up loggers according to environment and configuration. """

    file = app.config['LOGGER_FILEPATH']
    token = app.config['LOGENTRIES_TOKEN']
    level = DEBUG if app.config['DEBUG'] else INFO
    context = app.config['ENVIRONMENT']

    log = getLogger(name)
    log.setLevel(level)

    # shared by all handlers
    formatter = Formatter(
        '[%(asctime)s] '
        '[%(process)d] '
        '[%(name)s] '
        '[%(levelname)s] '
        '%(message)s'
    )

    if context != 'testing' and file:
        file = FileHandler(file, mode='a+')
        file.setLevel(level)
        file.setFormatter(formatter)
        log.addHandler(file)

    if context == 'development':
        console = StreamHandler(stream=stdout)
        console.setLevel(level)
        console.setFormatter(formatter)
        log.addHandler(console)

    if context != 'testing' and token:
        logentries = LogentriesHandler(token)
        logentries.setLevel(level)
        logentries.setFormatter(formatter)
        log.addHandler(logentries)

    return log
