#!/usr/bin/env python

from guichan import *
from font import Font
from image import Image

class Graphics:

    def __init__(self):
        self.mFont=None
        self.mClipStack=[]
        
    def pushClipArea(self,area):
        if len(self.mClipStack) == 0:
            carea=ClipRectangle()
            carea.x=area.x
            carea.y=area.y
            carea.width=area.width
            carea.height=area.height
            if carea.x < 0:
                carea.width+=carea.x
                carea.x=0
            if carea.y < 0:
                carea.height+=carea.y
                carea.y=0
            carea.xOffset=area.x
            carea.yOffset=area.y
            self.mClipStack.append(carea)
            return True
        else:
            top=self.mClipStack[-1]
            carea=ClipRectangle(area)
            carea.xOffset=top.xOffset+carea.x
            carea.yOffset=top.yOffset+carea.y
            carea.x+=top.xOffset
            carea.y+=top.yOffset
            
            #clamp the pushed clip rectangle
            if carea.x < top.x:
                carea.width+=carea.x-top.x
                carea.x=top.x
            
            if carea.y < top.y:
                carea.height+=carea.y-top.y
                carea.y=top.y
                
            if carea.x+carea.width > top.x+top.width:
                carea.width=top.x+top.width-carea.x
                if carea.width < 0:
                    carea.width=0
                    
            if carea.y+carea.height > top.y+top.height:
                carea.height=top.y+top.height-carea.y
                if carea.height < 0:
                    carea.height=0
                    
            result=carea.isIntersecting(top)
            self.mClipStack.append(carea)
            return result
        
    def popClipArea(self):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Tried to pop clip area from empty stack.")
        else:
            self.mClipStack.pop()
            
    def getCurrentClipArea(self):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("The clip area stack is empty.")
        else:
            return self.mClipStack[-1]
            
    def drawImage(self,image,dstX,dstY,width=-1,height=-1):
        pass
    
    def drawPoint(self,x,y):
        pass
    
    def drawLine(self,x1,y1,x2,y2):
        pass
    
    def drawRectangle(self,rect):
        pass

    def fillRectangle(self,rect):
        pass
    
    def setColor(self,color):
        pass

    def getColor(self):
        pass
    
    def setFont(self,font):
        self.mFont=font
        
    def drawText(self,text,x,y,alignment=0,color=None):
        if self.mFont==None:
            raise GCN_EXCEPTION("No font set.")
        
        self.mFont.setAlpha(self.mColor.a)
        if alignment == 0:
            self.mFont.drawText(self,text,x,y,color)
            
        elif alignment == 1:
            self.mFont.drawText(self,text,x - (self.mFont.getWidth(text)/2),y,color)
            
        elif alignment == 2:
            self.mFont.drawText(text,x - self.mFont.getWidth(text),y,color)
            
    def beginDraw(self):
        pass
    
    def endDraw(self):
        pass
            
    LEFT   = 0
    CENTER = 1
    RIGHT  = 2
        
        