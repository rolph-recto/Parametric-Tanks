#!/usr/bin/env python

from guichan import *
from event import Event

class ActionEvent(Event):
    def __init__(self,source,id):
        self.mSource=source
        self.mId=id
        
    def getId(self):
        return self.mId