#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from widget import Widget
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from keyListener import KeyListener
from keyEvent import KeyEvent
from key import Key
from focusListener import FocusListener

class Button(Widget,MouseListener,KeyListener,FocusListener):
    def __init__(self,caption=""):
        Widget.__init__(self)
        self.mHasMouse=False
        self.mKeyPressed=False
        self.mMousePressed=False
        self.mCaption=caption
        self.mAlignment=Graphics.CENTER
        self.mSpacing=4
        
        self.setFocusable(True)
        self.setTabInEnabled(True)
        self.setTabOutEnabled(True)
        self.setFrameSize(1)
        
        self.addMouseListener(self)
        self.addKeyListener(self)
        self.addFocusListener(self)
        self.adjustSize()
        
    def setCaption(self,caption,adjust=True):
        oCaption=self.mCaption
        self.mCaption=caption
        if adjust == True:
            self.adjustSize()
            
        elif oCaption != caption:
            self.addDirtyRect()
        
    def getCaption(self):
        return self.mCaption
    
    def setAlignment(self,align):
        oAlign=self.mAlignment
        self.mAlignment=align
        
        if oAlign != align:
            self.addDirtyRect()
        
    def getAlignment(self):
        return self.mAlignment
    
    def setSpacing(self,spacing):
        oSpacing=self.mSpacing
        self.mSpacing=spacing
        
        if oSpacing != spacing:
            self.addDirtyRect()
        
    def getSpacing(self):
        return self.mSpacing
    
    def draw(self,graphics):
        faceColor=Color(self.getBaseColor())
        highlightColor, shadowColor = Color(), Color()
        alpha = faceColor.a
        
        if self.isPressed() == True:
            faceColor = faceColor - 0x303030
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
        graphics.fillRectangle( Rectangle(1, 1, self.getDimension().width-1, self.getHeight() - 1) )
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0, 0, self.getWidth() - 1, 0)
        graphics.drawLine(0, 1, 0, self.getHeight() - 1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(self.getWidth() - 1, 1, self.getWidth() - 1, self.getHeight() - 1)
        graphics.drawLine(1, self.getHeight() - 1, self.getWidth() - 1, self.getHeight() - 1)
        
        graphics.setColor(self.getForegroundColor())
        textX=0
        textY=self.getHeight() /2 - self.getFont().getHeight() /2
        align=self.getAlignment()
        
        if align == Graphics.LEFT:
            textX=self.mSpacing
        
        elif align == Graphics.CENTER:
            textX=self.getWidth()/2
        
        elif align == Graphics.RIGHT:
            textX=self.getWidth() - self.mSpacing
            
        else:
            raise GCN_EXCEPTION("Unknown alignment.")
        graphics.setFont(self.getFont())
        
        if self.isPressed() == True:
            graphics.drawText(self.getCaption(), textX+1, textY+1, self.getAlignment(), self.getTextColor())
        else:
            graphics.drawText(self.getCaption(), textX, textY, self.getAlignment(), self.getTextColor() )
            if self.isFocused() == True:
                graphics.drawRectangle( Rectangle(2,2,self.getWidth()-4,self.getHeight()-4) )
            
    def adjustSize(self):
        r=Rectangle(self.getAbsoluteDimension())
        self.setWidth(self.getFont().getWidth(self.mCaption) + 2*self.mSpacing)
        self.setHeight(self.getFont().getHeight() + 2*self.mSpacing)
        r2=Rectangle(self.getAbsoluteDimension())
        if r != r2:
            self.addDirtyRect(r+r2)
        
    def isPressed(self):
        if self.mMousePressed == True:
            return self.mHasMouse
        else:
            return self.mKeyPressed
        
    def mousePressed(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT:
            self.mMousePressed=True
            mouseEvent.consume()
            self.addDirtyRect()
        
    def mouseEntered(self,mouseEvent):
        self.mHasMouse=True
        
    def mouseExited(self,mouseEvent):
        self.mHasMouse=False
        
    def mouseReleased(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT and self.mHasMouse == True and self.mMousePressed == True:
            self.mMousePressed=False
            self.distributeActionEvent()
            mouseEvent.consume()
            self.addDirtyRect()
            
        elif mouseEvent.getButton() == MouseEvent.LEFT:
            self.mMousePressed=False
            mouseEvent.consume()
            self.addDirtyRect()
            
    def mouseDragged(self,mouseEvent):
        mouseEvent.consume()
        
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        
        if key.getValue() == Key.ENTER or key.getValue() == Key.SPACE:
            self.mKeyPressed=True
            keyEvent.consume()
            self.addDirtyRect()
            
    def keyReleased(self,keyEvent):
        key=keyEvent.getKey()
        
        if (key.getValue() == Key.ENTER or key.getValue() == Key.SPACE) and self.mKeyPressed==True:
            self.mKeyPressed=False
            keyEvent.consume()
            self.distributeActionEvent()
            self.addDirtyRect()
    
    def focusGained(self,event):
        self.addDirtyRect()
    
    def focusLost(self,event):
        self.mMousePressed=False
        self.mKeyPressed=False
        self.addDirtyRect()
        
    def logic(self):
        pass
            
        
            
            
            




            
            
        
    