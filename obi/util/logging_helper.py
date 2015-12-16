import logging

obi_api_logging_enabled=True

class APILoggedBase():
    """
    Inheriting from this class provides logging of member access.

    TODO: - log before up-call (exception case) in __getattribute__
          - provide functionality as decorator
    """
    _obi_logger = logging.getLogger()

    def __getattribute__(self,name):
        if not obi_api_logging_enabled:
            return super().__getattribute__(name)
        else:
            rv = super().__getattribute__(name)
            if (not (name.startswith("__") or name.startswith("_obi_"))):
                self._obi_logger.info(
                    "get: " + str(self.__class__.__name__) +
                    "." + name + " -> " + str(rv)
                )
            return rv

    def __setattr__(self,name,value):
        if (obi_api_logging_enabled and
            not (name.startswith("__") or name.startswith("_obi_"))):
            self.__class__._obi_logger.info(
                "set: " + str(self.__class__.__name__) +
                "." + name + " <- " + str(value)
            )
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
