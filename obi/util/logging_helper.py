import logging

obi_api_logging_enabled=True

class APILoggedBase():
    """
    Inheriting from this class provides logging of member access.

    TODO: - provide functionality as decorator
          - create better documenation
    """
    _obi_logger = logging.getLogger()

    def __getattribute__(self,name):
        if not obi_api_logging_enabled:
            return super().__getattribute__(name)
        else:
            do_log = False
            if (not (name.startswith("__") or name.startswith("_obi_"))):
                do_log = True
                log_string="get: {c}.{a}".format(
                    c = str(self.__class__.__name__), a = name
                )
            try:
                rv = super().__getattribute__(name)
            except Exception as e:
                if do_log:
                    self._obi_logger.error(log_string + " ERROR")
                raise
            if do_log:
                self._obi_logger.info(log_string + " -> " + str(rv))
            return rv

    def __setattr__(self,name,value):
        if (obi_api_logging_enabled and
            not (name.startswith("__") or name.startswith("_obi_"))):
            self.__class__._obi_logger.info("set: {c}.{a} <- {v}".format(
                c = str(self.__class__.__name__), a = name, v = value
            ))
        return super().__setattr__(name, value)

    @classmethod
    def setClassLogger(cls, logger):
        cls._obi_logger = logger

    @classmethod
    def getClassLogger(cls):
        return cls._obi_logger

    def setInstanceLogger(self, logger):
        self._obi_logger = logger

    # TODO - when an instance is asked for the logger and it can not
    #        provide the object it propagates the request to lower levels
    def getInstanceOrClassLogger(self):
        return self._obi_logger
