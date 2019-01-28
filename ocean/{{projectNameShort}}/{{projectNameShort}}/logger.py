import logging.config
import os
import yaml

class Logger:
    """
    **File/console logger**

    - Usage::

        # Creation
        logger = Logger(path='../logs', name='EdaLogger', filename='eda.txt')
        
        # Different levels of importance
        logger.debug('something happened')
        logger.info('something happened')
        logger.warning('something happened')
        logger.error('something happened')
        logger.exception('something happened')
        logger.critical('something happened')
    """
    
    _src_path = os.path.dirname(os.path.realpath(__file__))
    _logs_path = os.path.abspath(os.path.join(_src_path, '../logs'))
    _config_path = os.path.abspath(os.path.join(_src_path, '../config'))

    def __init__(self, path: str, name: str, filename: str):
        super().__init__()
        with open(os.path.join(self._config_path, 'logging_config.yml'), 'r') as f:
            config = yaml.safe_load(f.read())
            config['handlers']['file']['filename'] = os.path.join(self._logs_path, filename)
            logging.config.dictConfig(config)
            if not name:
                name = __name__
            self._logger = logging.getLogger(name)

    def debug(self, msg, args=[], kwargs={}):
        self._logger.disabled = False
        self._logger.debug(msg.format(args, kwargs))

    def info(self, msg, args=[], kwargs={}):
        self._logger.disabled = False
        self._logger.info(msg.format(args, kwargs))

    def warning(self, msg, args=[], kwargs={}):
        self._logger.disabled = False
        self._logger.warning(msg.format(args, kwargs))

    def error(self, msg, args=[], kwargs={}):
        self._logger.disabled = False
        self._logger.error(msg.format(args, kwargs))

    def exception(self, msg, exc_info, args=[], kwargs={}):
        self._logger.disabled = False
        self._logger.exception(msg.format(args, kwargs), exc_info)

    def critical(self, msg, args=[], kwargs={}):
        self._logger.disabled = False
        self._logger.critical(msg.format(args, kwargs))
