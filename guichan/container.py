#!/usr/bin/env python

from guichan import *
from basicContainer import BasicContainer

class Container(BasicContainer):
    def __init__(self):
        BasicContainer.__init__(self)
        self.mOpaque=True
        
    def __del__(self):
        BasicContainer.__del__(self)
        
    def draw(self,graphics):
        if self.isOpaque() == True:
            graphics.setColor(self.getBaseColor())
            graphics.fillRectangle( Rectangle(0,0,self.getWidth(),self.getHeight()) )
        
        self.drawChildren(graphics)
        
    def setOpaque(self,opaque):
        self.mOpaque=opaque
        
    def isOpaque(self):
        return self.mOpaque
    
    def add(self,widget,x=-1,y=-1):
        if x == -1 or y == -1:
            BasicContainer.add(self,widget)
        else:
            widget.setPosition(x,y)
            BasicContainer.add(self,widget)
        
        