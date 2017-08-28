import logging
import logging.config

import yaml

default_path = 'config.yaml'

default_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(name)s %(version)s %(message)s"
        },
        "json": {
            "class": "logging_mv_integrations.logging_json_formatter.LoggingJsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(version)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",

            "level": "INFO",
            "formatter": "json",
        }
    },
    "loggers": {
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}


class CustomAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        extra = kwargs.pop('extra', self.extra['extra'])
        version = self.extra['version']
        return '%s, extra: %s, version: %s' % (msg, extra, version), kwargs


def get_logger(logger_name, logger_version=None, logger_format=None, logger_level=None, config_path=None):
    config_dict = default_config

    if config_path:
        with open(config_path) as config:
            config_dict = yaml.load(config)

    logging.config.dictConfig(config_dict)

    logger = logging.getLogger(logger_name)

    adapter = CustomAdapter(logger, {'version': logger_version, 'extra': 'none'})

    return adapter




