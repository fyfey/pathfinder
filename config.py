#!/usr/env python

import yaml

class Config:
    def load(self, filename):
        try:
            f = open(filename, 'r')
            self.config = yaml.load(f)
            print self.config
        except IOError:
            print "Can't find config.yaml!"

        for key in self.config:
            setattr(self, key, self.config[key])
