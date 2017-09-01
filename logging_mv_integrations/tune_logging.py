import logging
import logging.config
import yaml
import os


class CustomAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        if 'extra' in kwargs:
            kwargs['extra'].update({'version': self.extra['version']})
        else:
            kwargs['extra'] = {'version': self.extra['version']}
        return msg, kwargs


def get_logger(logger_name, logger_version=None, logger_format=None, logger_level=None, config_path=None):

    config_dict = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yaml')))

    if config_path:
        with open(config_path) as config:
            config_dict = yaml.load(config)

    logging.config.dictConfig(config_dict)

    logger = logging.getLogger(logger_name)

    adapter = CustomAdapter(logger, {'version': logger_version})

    return adapter





