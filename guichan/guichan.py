#!/usr/bin/env python

from array import *
from exception import *
from rectangle import *
from color import *
from event import Event
import weakref

true=True
TRUE=True
false=False
FALSE=False

class DirtyRectangle:
    def __init__(self):
        self.mRectList=[]
        self.mEnabled=True
        self.mDrawOptimized=True
        
    def addRect(self,rect,clipArea=Rectangle(0,0)):
        if self.mEnabled == True:
            rect.x+=clipArea.x
            rect.y+=clipArea.y
            add=True
            for i in self.mRectList:
                #if rect is already added
                if i == rect:
                    add=False
                #if rect collides with another rect, add the two rect's union
                if i.isIntersecting(rect) == True and rect.isBoundTo(i) == False:
                    self.mRectList.append(i+rect)
                    add=False
                #if rect is inside a rect in the list, don't add it
                elif rect.isBoundTo(i) == True:
                    add=False
            
            if add == True:
                self.mRectList.append(rect)
        
    def removeRect(self,rect):
        if self.mEnabled == True:
            for i in self.mRectList:
                if i == rect:
                    self.mRectList.remove(i)
        
    def clearList(self):
        if self.mEnabled == True:
            del self.mRectList[:]
        
    def getList(self):
        return self.mRectList
    
    def isRectInDirtyRect(self,rect):
        """Convenience functions to check if
        the graphics object even has to draw a
        widget; if the widget doesn't collide
        a dirty rect, then the graphics doesn't
        need to draw the widget."""
        if self.mEnabled == False:
            return True
        
        for i in self.mRectList:
            if i.isIntersecting(rect) == True:
                return True
            
        return False
    
    def enable(self):
        self.mEnabled=True
        
    def disable(self):
        self.mEnabled=False
        
    def setEnabled(self,enable):
        self.mEnabled=enable
        
    def isEnabled(self):
        return self.mEnabled
    
    def setDrawOptimized(self,draw):
        self.mDrawOptimized=draw
        
    def isDrawOptimized(self):
        return self.mDrawOptimized
        
