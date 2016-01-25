import logging
import obi.util.function_details as fd

obi_api_logging_enabled = True
obi_api_logging_default_logger = logging.getLogger()

class APILoggedBase():
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

    The default logger can be changed by changing the default vaule
    of this module (obi_default_logge). Or by changing the _obi_logger
    member of an instance or class.
    """

    _obi_logger = obi_api_logging_default_logger

    def __getattribute__(self,name):
        if not obi_api_logging_enabled:
            return super().__getattribute__(name)

        do_log = False
        if not name.startswith("__") and not name.startswith("_obi_"):
            do_log = True
            log_string="get: {c}.{a}".format(
                c = str(self.__class__.__name__), a = name
            )
        try:
            rv = super().__getattribute__(name)
        except Exception as e:
            if do_log:
                self._obi_logger.exception(log_string + " ERROR")
            raise
        if do_log:
            self._obi_logger.info(log_string + " -> " + str(rv))
        return rv

    def __setattr__(self,name,value):
        if ( obi_api_logging_enabled and
             not name.startswith("__") and
             not name.startswith("_obi_")
        ):
            self.__class__._obi_logger.info("set: {c}.{a} <- {v}".format(
                c = str(self.__class__.__name__), a = name, v = value
            ))
        return super().__setattr__(name, value)
##  APILoggedBase

def loggedfunction(to_log):
    def logged(*args, **kwargs):
        logger = obi_api_logging_default_logger
        msg = "calling: {0} with arguments '{1}'".format(to_log.__name__ ,fd.args_to_str(*args,**kwargs))
        logger.info(msg)
        to_log( *args, **kwargs)
    return logged
