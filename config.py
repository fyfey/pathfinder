#!/usr/env python

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Config:
    def load(self, filename):
        try:
            f = open(filename, 'r')
            self.config = yaml.load(f, Loader=Loader)
            print(self.config)
        except IOError:
            print("Can't find config.yaml!")

        for key in self.config:
            setattr(self, key, self.config[key])
