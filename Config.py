#!/usr/bin/env python

import logging
import os
from ConfigParser import ConfigParser


class Config():

    DEFAULT_CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, configfile):
        self.config = None

        conf_dir = os.environ.get('CONF_DIR', self.DEFAULT_CONFIG_DIR)
        conf_file = os.path.normpath(os.path.join(conf_dir, configfile))
        if not os.path.exists(conf_file):
            msg = 'Config file %s not found ' % [conf_file]
            raise RuntimeError(msg)
            return
        else:
            self.config = ConfigParser()
            self.config.read(conf_file)

    @property
    def config(self):
        return self.config


if __name__ == "__main__":

    config = Config('dbinfo.conf')
    #print vmmgrconfig.config.get('global', 'version')
