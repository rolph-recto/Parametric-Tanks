#!/usr/bin/env python

from guichan import *
from inputEvent import InputEvent

class MouseEvent(InputEvent):
    def __init__(self,source,shiftPressed,controlPressed,altPressed,metaPressed,type,button,x,y,clickCount):
        self.mSource=source
        self.mShiftPressed=shiftPressed
        self.mControlPressed=controlPressed
        self.mAltPressed=altPressed
        self.mMetaPressed=metaPressed
        self.mIsConsumed=False
        self.mType=type
        self.mButton=button
        self.mX=x
        self.mY=y
        self.mClickCount=clickCount
    
    def getButton(self):
        return self.mButton
 
    def getX(self):
        return self.mX
    
    def getY(self):
        return self.mY
    
    def getType(self):
        return self.mType
    
    def getClickCount(self):
        return self.mClickCount
    
    MOVED             = 0
    PRESSED           = 1
    RELEASED          = 2
    WHEEL_MOVED_DOWN  = 3
    WHEEL_MOVED_UP    = 4
    CLICKED           = 5
    ENTERED           = 6
    EXITED            = 7
    DRAGGED           = 8
    
    EMPTY             = 0
    LEFT              = 1
    RIGHT             = 2
    MIDDLE            = 3
