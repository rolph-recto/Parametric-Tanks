#!/usr/bin/env python

from guichan import *

from key import Key

class KeyInput:
    def __init__(self,key,type):
        self.mKey=key
        self.mType=type
        self.mShiftPressed=False
        self.mControlPressed=False
        self.mAltPressed=False
        self.mMetaPressed=False
        self.mNumericPad=False
        
    def __str__(self):
        s="KeyInput [type="+str(self.mType)+", key="+str(self.mKey)+" mods pressed="
        if self.mShiftPressed == True:
            s+="SHIFT "
        if self.mControlPressed == True:
            s+="CONTROL "
        if self.mAltPressed == True:
            s+="ALT "
        if self.mMetaPressed == True:
            s+="META "            
        if self.mNumericPad == True:
            s+="NUMPAD"
        s+="]"
        return s
        
    def setType(self,type):
        self.mType=type

    def setKey(self,key):
        self.mKey=key
        
    def setShiftPressed(self,pressed):
        self.mShiftPressed=pressed
        
    def setControlPressed(self,pressed):
        self.mControlPressed=pressed
        
    def setAltPressed(self,pressed):
        self.mAltPressed=pressed
        
    def setMetaPressed(self,pressed):
        self.mMetaPressed=pressed
        
    def setNumericPad(self,pressed):
        self.mNumericPad=pressed
        
    def getType(self):
        return self.mType

    def getKey(self):
        return self.mKey
        
    def isShiftPressed(self):
        return self.mShiftPressed
    
    def isControlPressed(self):
        return self.mControlPressed
    
    def isAltPressed(self):
        return self.mAltPressed
    
    def isMetaPressed(self):
        return self.mMetaPressed
    
    def isNumericPad(self):
        return self.mNumericPad
    
        
    PRESSED  = 0
    RELEASED = 1