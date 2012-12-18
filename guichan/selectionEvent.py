#!/usr/bin/env python

from guichan import *
from event import Event

class SelectionEvent(Event):
    def __init__(self,source):
        self.mSource=source