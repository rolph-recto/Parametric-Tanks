#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font

class DefaultFont(Font):
    def getHeight(self):
        return 8
    
    def getWidth(self,text):
        return 8*len(text)
    
    def drawGlyph(self,graphics,glyph,x,y):
        oldColor=graphics.getColor()
        graphics.setColor( Color( 0xFFFFFF ) )
        graphics.drawRectangle( Rectangle(x,y,8,8) )
        graphics.setColor(oldColor)
        return 8
    
    def drawText(self,graphics,text,x,y,color=None):
        for i in range(len(text)):
            self.drawGlyph(graphics,text[i],x,y)
            x+=self.getWidth(text[i])
            
    def getStringIndexAt(self,text,x):
        if x > len(text)*8:
            return len(text)*8
        else:
            return x/8
    