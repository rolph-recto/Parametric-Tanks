#!/usr/bin/env python

from guichan import *

class Font:
    def getWidth(self,text):
        pass
    
    def getHeight(self):
        pass
    
    def getStringIndexAt(self,text,x):
        size=0
        for i in range(len(text)):
            size=self.getWidth(text[:i])
            if size > x:
                return i
        
        return len(text)
        
    def drawText(self,graphics,text,x,y,color=None):
        pass
    
    def setAlpha(self,alpha):
        pass
    
    def getAlpha(self):
        pass