#!/usr/bin/env python

from guichan import *
from inputEvent import InputEvent

class KeyEvent(InputEvent):
    def __init__(self,source,shiftPressed,controlPressed,altPressed,metaPressed,type,isNumPad,key):
        self.mSource=source
        self.mShiftPressed=shiftPressed
        self.mControlPressed=controlPressed
        self.mAltPressed=altPressed
        self.mMetaPressed=metaPressed
        self.mIsConsumed=False
        self.mType=type
        self.mIsNumericPad=isNumPad
        self.mKey=key
        
    def getType(self):
        return self.mType
    
    def isNumericPad(self):
        return self.mIsNumericPad
    
    def getKey(self):
        return self.mKey
    
    PRESSED  = 0
    RELEASED = 1