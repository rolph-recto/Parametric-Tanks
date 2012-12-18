#!/usr/bin/env python

from guichan import *

class MouseInput:
    def __init__(self,button=0,type=0,x=0,y=0,timeStamp=0):
        self.mType=type
        self.mButton=button
        self.mTimeStamp=timeStamp
        self.mX=x
        self.mY=y
        
    def __str__(self):
        return "MouseInput [button="+str(self.mButton)+", type="+str(self.mType)+", timeStamp="+str(self.mTimeStamp)+", x="+str(self.mX)+", y="+str(self.mY)+"]"
        
    def setType(self,type):
        self.mType=type
        
    def setButton(self,button):
        self.mButton=button
    
    def setTimeStamp(self,timeStamp):
        self.mTimeStamp=timeStamp

    def setX(self,x):
        self.mX=x
        
    def setY(self,y):
        self.mY=y
        
    def getType(self):
        return self.mType
    
    def getButton(self):
        return self.mButton
    
    def getTimeStamp(self):
        return self.mTimeStamp
    
    def getX(self):
        return self.mX
    
    def getY(self):
        return self.mY  
    
    MOVED             = 0
    PRESSED           = 1
    RELEASED          = 2
    WHEEL_MOVED_DOWN  = 3
    WHEEL_MOVED_UP    = 4

    EMPTY             = 0
    LEFT              = 1
    RIGHT             = 2
    MIDDLE            = 3
