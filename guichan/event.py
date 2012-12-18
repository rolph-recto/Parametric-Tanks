#!/usr/bin/env python

from guichan import *

class Event:
    def __init__(self,source):
        self.mSource=source
        
    def getSource(self):
        return self.mSource