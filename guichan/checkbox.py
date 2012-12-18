#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from widget import Widget
from keyListener import KeyListener
from keyEvent import KeyEvent
from key import Key
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from mouseInput import MouseInput
from focusListener import FocusListener

class Checkbox(Widget,MouseListener,KeyListener,FocusListener):
    def __init__(self,caption="",selected=False):
        Widget.__init__(self)
        self.mCaption=caption
        self.mSelected=selected
        
        self.setFocusable(True)
        self.addMouseListener(self)
        self.addKeyListener(self)
        self.addFocusListener(self)
        
        self.adjustSize()
        
    def draw(self,graphics):
        self.drawBox(graphics)
        
        graphics.setFont(self.getFont())
        graphics.setColor(self.getForegroundColor())
        
        h=self.getHeight()+self.getHeight()/2
        
        graphics.drawText(self.getCaption(),h-2,0, self.getTextColor())
        
    def drawBox(self,graphics):
        h=self.getHeight()-2
        faceColor=self.getBaseColor()
        alpha=faceColor.a
        highlightColor=faceColor+0x303030
        highlightColor.a=alpha
        shadowColor=faceColor-0x303030
        shadowColor.a=alpha
        
        graphics.setColor(shadowColor)
        graphics.drawLine(1,1,h,1)
        graphics.drawLine(1,1,1,h)
        
        graphics.setColor(highlightColor)
        graphics.drawLine(h,1,h,h)
        graphics.drawLine(1,h,h-1,h)
        
        graphics.setColor(self.getBackgroundColor())
        
        if self.isFocused() == True:
            graphics.drawRectangle( Rectangle(0,0,h+2,h+2) )
            
        if self.mSelected == True:
            graphics.drawLine(3,5,3,h-2)
            graphics.drawLine(4,5,4,h-2)
            
            graphics.drawLine(5,h-3,h-2,4)
            graphics.drawLine(5,h-4,h-4,5)
            
    
    def setSelected(self,selected):
        if self.mSelected != selected:
            self.mSelected=selected
            self.addDirtyRect()

    def isSelected(self):
        return self.mSelected
        
    def setCaption(self,caption,adjust=True):
        self.mCaption=caption
        if adjust == True:
            self.adjustSize()
        else:
            self.addDirtyRect()
        
    def getCaption(self):
        return self.mCaption
    
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        if key.getValue() == Key.ENTER or key.getValue() == Key.SPACE:
            self.toggleSelected()
    
    def mousePressed(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT:
            self.toggleSelected()
            
    def mouseDragged(self,mouseEvent):
        mouseEvent.consume()
        
    def focusGained(self,event):
        self.addDirtyRect()
        
    def focusLost(self,event):
        self.addDirtyRect()
        
    def adjustSize(self):
        height = self.getFont().getHeight()
        
        self.setHeight(height)
        self.setWidth(self.getFont().getWidth(self.mCaption) + height + height / 2)
        
        self.addDirtyRect()
    
    def toggleSelected(self):
        if self.mSelected == True:
            self.mSelected=False
        else:
            self.mSelected=True
        self.distributeActionEvent()
        self.addDirtyRect()
        
        