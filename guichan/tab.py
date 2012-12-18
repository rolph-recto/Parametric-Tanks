#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from mouseInput import MouseInput
from basicContainer import BasicContainer
from label import Label

class Tab(BasicContainer,MouseListener):
    def __init__(self,caption=""):
        BasicContainer.__init__(self)
        self.mHasMouse=False
        self.mTabbedArea=None
        self.mLabel=Label()
        self.mLabel.setPosition(4,4)
        self.setCaption(caption)
        self.add(self.mLabel)
        
        self.addMouseListener(self)
        self.addFocusListener(self)
        
    def adjustSize(self):
        self.setSize(self.mLabel.getWidth()+8, self.mLabel.getHeight()+8)
        
        if self.mTabbedArea != None:
            self.mTabbedArea.adjustTabPositions()
            
        self.addDirtyRect()
            
    def setTabbedArea(self,tabbedArea):
        self.mTabbedArea=tabbedArea
        
    def getTabbedArea(self):
        return self.mTabbedArea
    
    def setCaption(self,caption):
        self.mLabel.setCaption(caption)
        self.mLabel.adjustSize()
        self.adjustSize()
        
    def getCaption(self):
        return self.mLabel.getCaption()
    
    def draw(self,graphics):
        faceColor = self.getBaseColor()
        alpha=faceColor.a
        highlightColor=faceColor+0x303030
        highlightColor.a=alpha
        shadowColor=faceColor-0x303030
        shadowColor.a=alpha
        
        borderColor, baseColor = None, None
        
        if (self.mTabbedArea != None and self.mTabbedArea.isTabSelected(self) == True) or self.mHasMouse:
            #Draw a border.
            graphics.setColor(highlightColor)
            graphics.drawLine(0, 0, self.getWidth()-1, 0)
            graphics.drawLine(0, 1, 0, self.getHeight()-1)
            
            graphics.setColor(shadowColor)
            graphics.drawLine(self.getWidth()-1, 1, self.getWidth()-1, self.getHeight()-1)
            
            borderColor=Color(highlightColor)
            baseColor=Color(self.getBaseColor())
        else:
            #draw a border
            graphics.setColor(shadowColor)
            graphics.drawLine(0, 0, self.getWidth()-1, 0)
            graphics.drawLine(0, 1, 0, self.getHeight()-1)
            graphics.drawLine(self.getWidth()-1, 1, self.getWidth()-1, self.getHeight()-1)
            
            baseColor=self.getBaseColor() - 0x151515
            baseColor.a=alpha
            
        #Push a clip area so the other drawings don't need to worry
        #about the border.
        graphics.pushClipArea( Rectangle(1, 1, self.getWidth() - 2, self.getHeight() - 1) )
        currentClipArea=Rectangle( graphics.getCurrentClipArea() )
        
        graphics.setColor(baseColor)
        graphics.fillRectangle( Rectangle(0,0,self.getWidth(), self.getHeight()) )
        
        self.drawChildren(graphics)
        
        if self.mTabbedArea != None and self.mTabbedArea.isFocused() == True and self.mTabbedArea.isTabSelected(self) == True:
            graphics.setColor( self.getForegroundColor() )
            graphics.drawRectangle( Rectangle(2,2,currentClipArea.width-4,currentClipArea.height-4) )
            
        graphics.popClipArea()
        
    def mouseEntered(self,mouseEvent):
        self.mHasMouse=True
        self.addDirtyRect()
        
    def mouseExited(self,mouseEvent):
        self.mHasMouse=False
        self.addDirtyRect()