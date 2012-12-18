#!/usr/bin/env python

from guichan import *
from event import Event

class InputEvent(Event):
    def __init__(self,source,shiftPressed=False,controlPressed=False,altPressed=False,metaPressed=False):
        self.mSource=source
        self.mShiftPressed=shiftPressed
        self.mControlPressed=controlPressed
        self.mAltPressed=altPressed
        self.mMetaPressed=metaPressed
        self.mIsConsumed=False
        
    def isShiftPressed(self):
        return self.mShiftPressed
    
    def isControlPressed(self):
        return self.mControlPressed

    def isAltPressed(self):
        return self.mAltPressed
    
    def isMetaPressed(self):
        return self.mMetaPressed
    
    def consume(self):
        self.mIsConsumed=True
        
    def isConsumed(self):
        return self.mIsConsumed