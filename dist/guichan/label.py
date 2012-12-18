#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from widget import Widget

class Label(Widget):
    def __init__(self,caption=""):
        Widget.__init__(self)
        self.mCaption=caption
        self.mAlignment=Graphics.LEFT
        self.adjustSize()
        
    def __del__(self):
        Widget.__del__(self)
        
    def setCaption(self,caption,adjust=True):
        self.mCaption=caption
        if adjust == True:
            self.adjustSize()
        else:
            self.addDirtyRect()
        
    def getCaption(self):
        return self.mCaption
    
    def setAlignment(self,align):
        if self.mAlignment != align:
            self.mAlignment=align
            self.addDirtyRect()
        
    def getAlignment(self):
        return self.mAlignment
    
    def adjustSize(self):
        self.setHeight( self.getFont().getHeight() )
        self.setWidth( self.getFont().getWidth(self.mCaption) )
        self.addDirtyRect()
    
    def draw(self,graphics):
        textX=0
        textY=self.getHeight()/2 - self.getFont().getHeight()/2
        align=self.mAlignment
        
        if align == Graphics.LEFT:
            textX=0
            
        elif align == Graphics.CENTER:
            textX=self.getWidth()/2
            
        elif align == Graphics.RIGHT:
            textX=self.getWidth()
        
        else:
            raise GCN_EXCEPTION("Unknown alignment.")
        
        graphics.setFont(self.getFont())
        graphics.setColor(self.getForegroundColor())
        graphics.drawText(self.mCaption, textX, textY, self.getAlignment(), self.getTextColor() )
            