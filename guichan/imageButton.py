#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from button import Button
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from keyListener import KeyListener
from keyEvent import KeyEvent
from key import Key
from focusListener import FocusListener
from image import Image

class ImageButton(Button):
    def __init__(self,image=None):
        self.mImage=None
        Button.__init__(self)
        self.setSize(0,0)
        if type(image) == type("abc"):
            self.mImage=Image.load(image)
        else:
            self.mImage=image
            
        self.adjustSize()
            
    def adjustSize(self):
        if self.mImage != None:
            self.setSize( self.mImage.getWidth() + self.mImage.getWidth()/2, self.mImage.getHeight() + self.mImage.getHeight()/2)
            self.addDirtyRect()
    
    def setImage(self,image):
        self.mImage=image
        self.adjustSize()
        
    def getImage(self):
        return self.mImage
    
    def draw(self,graphics):
        faceColor=Color( self.getBaseColor() )
        highlightColor, shadowColor=Color(), Color()
        alpha=faceColor.a
        
        if self.isPressed() == True:
            faceColor=faceColor - 0x303030
            faceColor.a=alpha
            highlightColor=faceColor - 0x303030
            highlightColor.a=alpha
            shadowColor=faceColor + 0x303030
            shadowColor.a=alpha
        else:
            highlightColor=faceColor + 0x303030
            highlightColor.a=alpha
            shadowColor=faceColor - 0x303030
            shadowColor.a=alpha
            
        graphics.setColor(faceColor)
        graphics.fillRectangle( Rectangle(1, 1, self.getWidth()-1, self.getHeight()-1) )
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0, 0, self.getWidth()-1, 0)
        graphics.drawLine(0, 1, 0, self.getHeight()-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(self.getWidth()-1, 1, self.getWidth()-1, self.getHeight()-1)
        graphics.drawLine(1, self.getHeight()-1, self.getWidth()-1, self.getHeight()-1)
        
        graphics.setColor(self.getForegroundColor())
        textX=(self.getWidth() - (self.mImage.getWidth() if self.mImage != None else 0) ) /2
        textY=(self.getHeight() - (self.mImage.getHeight() if self.mImage != None else 0) ) /2
        
        oldAlpha=self.mImage.getAlpha()
        self.mImage.setAlpha(self.getBaseColor().a)
        if self.isPressed() == True:
            if self.mImage != None:
                graphics.drawImage(self.mImage, textX+1, textY+1)
        
        else:
            if self.mImage != None:
                graphics.drawImage(self.mImage, textX, textY)
                
            if self.isFocused() == True:
                graphics.drawRectangle( Rectangle(2, 2, self.getWidth()-4, self.getHeight()-4) )
                
        self.mImage.setAlpha(oldAlpha)
            
            
        
            