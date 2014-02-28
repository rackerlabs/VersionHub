#!/usr/bin/env python
""" This file handles loading and parsing the config """

import logging
import yaml

log = logging.getLogger(__name__)


class Config(dict):
    """ Configuration dictionary """

    def __init__(self, *args, **kwargs):
        log.error(args)
        log.error(kwargs)
        dict.__init__(self, *args, **kwargs)

    def load_file(self, file_name):
        """ Given a config file, parse it and store it """
        data = yaml.load(open(file_name, 'r'))
        log.error(file_name)
        log.error(data)

        if not isinstance(data, dict):
            raise Exception("config file not parsed correctly")

        deep_merge(self, data)


def deep_merge(orig, other):
    """ Modify orig, overlaying information from other """

    for key, value in list(other.items()):
        if(
            key in orig
            and isinstance(orig[key], dict)
            and isinstance(value, dict)
        ):
            deep_merge(orig[key], value)
        else:
            orig[key] = value

#
# Singleton Instance
#

config = Config()
