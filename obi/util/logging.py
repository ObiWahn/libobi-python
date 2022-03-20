#!/usr/bin/env python3
# Copyright - 2016 - Jan Christoph Uhde <Jan@UhdeJC.com>
import logging
import sys

import obi.util.stringify as sf

# debugging helper
# from pprint import pprint as PP
# from pprint import pformat as PF

obi_logging_enabled = True
obi_logging_logger = None
obi_logging_detailed = True
obi_logging_api = True


def create_logger(
    logger_name: str = "obi_default", level: int = logging.INFO, handler=None, handlers=[]
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.handlers = []
    logger.setLevel(level)

    if handler:
        handlers.append(handler)

    if handlers:
        for handler in handlers:
            logger.addHandler(handler)
    else:
        logger.addHandler(logging.StreamHandler())

    return logger


def init_logging(
    logger_name: str = "obi_default", level: int = logging.INFO, handler=None, handlers=[]
) -> logging.Logger:
    global obi_logging_logger
    obi_logging_logger = create_logger(logger_name, level, handler, handlers)
    return obi_logging_logger


# We could make the init mandatory
init_logging()


def apply_formatter(logger: logging.Logger, formatter):
    for handler in logger.handlers:
        handler.setFormatter(formatter)


def create_obi_formatter_short():
    return logging.Formatter("%(levelname)7s - %(filename)s:%(lineno)s - %(message)s")


def create_obi_formatter():
    return logging.Formatter("%(asctime)s - %(name)s - %(levelname)7s - %(filename)s:%(lineno)s - %(message)s")


def log_with_caller_info(logger, level, msg, depth=2):
    frame = sys._getframe(depth)

    filename = frame.f_code.co_filename
    name = frame.f_code.co_name
    line = frame.f_lineno

    record = logger.makeRecord(logger.name, logging.INFO, filename, line, msg, None, None, name, None)
    logger.handle(record)


class LoggedBase:
    """
    Inheriting from this class provides logging of member access.

    Given a class 'Some' has this class as base the following code
    would produce the shown log information.

    Code:
        some = Some()
        some.foo = "bar"
        print(some.foo)

    Log:
        INFO:root:set: Some.foo <- bar
        INFO:root:get: Some.foo -> bar

    """

    def __getattribute__(self, name):
        if not obi_logging_api:
            return super().__getattribute__(name)

        do_log = False
        if not name.startswith("__") and not name.startswith("_obi_"):
            do_log = True
            log_string = "get: {c}.{a}".format(c=str(self.__class__.__name__), a=name)
        try:
            rv = super().__getattribute__(name)
        except Exception as e:
            if do_log:
                obi_logging_logger.exception(log_string + " ERROR: " + str(e))
            raise
        if do_log:
            msg = "{0} -> {1}".format(log_string, str(rv))
            if obi_logging_detailed:
                log_with_caller_info(obi_logging_logger, logging.INFO, msg)
            else:
                obi_logging_logger.info(msg)
        return rv

    def __setattr__(self, name, value):
        if obi_logging_api and not name.startswith("__") and not name.startswith("_obi_"):
            msg = "set: {c}.{a} <- {v}".format(c=str(self.__class__.__name__), a=name, v=value)
            if obi_logging_detailed:
                log_with_caller_info(obi_logging_logger, logging.INFO, msg)
            else:
                obi_logging_logger.info(msg)
        return super().__setattr__(name, value)


#  APILoggedBase
def loggedfunction(to_log):
    def logged(*args, **kwargs):
        logger = obi_logging_logger
        msg = "calling: {0}({1})".format(to_log.__name__, sf.args_to_str(*args, **kwargs))
        if obi_logging_detailed:
            log_with_caller_info(logger, logging.INFO, msg)
        else:
            logger.info(msg)
        return to_log(*args, **kwargs)

    return logged
