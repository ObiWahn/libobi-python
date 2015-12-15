import logging

obi_api_logging_enabled=True

class APILoggedBase():
    """
    Inheriting from this class provides logging of member access
    """
    _obi_no_log_logger = logging.getLogger()
    _obi_no_log_exclude = [ "setClassLogger", "getClassLogger"
                          , "setInstanceLogger", "getInstnaceOrClassLogger"
                          ]

    def __getattribute__(self,name):
        rv = super().__getattribute__(name)
        if ( obi_api_logging_enabled
             and not (name.startswith("__") or name.startswith("_obi_no_log"))
             and not self._obi_no_log_check_exclude(name)):
             # using the above line only would be shorter and lead to more recursion :P
            self._obi_no_log_logger.info(
                "get: " + str(self.__class__.__name__) + "." + name + " -> " + str(rv))
        return rv

    def __setattr__(self,name,value):
        rv = super().__setattr__(name, value)
        if ( obi_api_logging_enabled
             and not (name.startswith("__") or name.startswith("_obi_no_log"))
             and not self._obi_no_log_check_exclude(name)):
            self.__class__._obi_no_log_logger.info(
                "set: " + str(self.__class__.__name__) + "." + name + " <- " + str(value))
        return rv

    @classmethod
    def _obi_no_log_check_exclude(cls, name):
        if name in cls._obi_no_log_exclude:
            return True
        return False

    @classmethod
    def setClassLogger(cls, logger):
        cls._obi_no_log_logger = logger

    @classmethod
    def getClassLogger(cls):
        return cls._obi_no_log_logger

    def setInstanceLogger(self, logger):
        self._obi_no_log_logger = logger

    # TODO - when an instanace is asked for the logger and it can not
    #        provide the object it propagets the request to lower levels
    def getInstanceOrClassLogger(self):
        return self._obi_no_log_logger
