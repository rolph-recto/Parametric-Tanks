#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from widget import Widget
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from mouseInput import MouseInput
from keyListener import KeyListener
from keyEvent import KeyEvent
from key import Key

class TextField(Widget,MouseListener,KeyListener):
    def __init__(self,text=""):
        Widget.__init__(self)
        self.mCaretPosition=0
        self.mXScroll=0
        self.mText=text
        self.mInsert=True
        self.mMaxSize=-1
        
        self.setFocusable(True)
        
        self.addMouseListener(self)
        self.addKeyListener(self)
        
        self.adjustSize()
        
    def setText(self,text):
        if len(text) < self.mCaretPosition:
            self.mCaretPosition=len(text)
            
        self.mText=text
        self.addDirtyRect()
    
    def getText(self):
        return self.mText
    
    def setCaretPosition(self,position):
        if position > len(self.mText):
            self.mCaretPosition = len(self.mText)
        elif position < 0:
            self.mCaretPosition=0
        else:
            self.mCaretPosition=position
            
        self.fixScroll()
        
    def getCaretPosition(self):
        return self.mCaretPosition

    def setInsert(self,insert):
        self.mInsert=insert
        self.addDirtyRect()
    
    def isInsert(self):
        return self.mInsert
    
    def setMaxSize(self,size):
        self.mMaxSize=size
    
    def getMaxSize(self):
        return self.mMaxSize
    
    def toggleInsert(self):
        if self.mInsert == False:
            self.mInsert=True
        else:
            self.mInsert=False
    
    def fontChanged(self):
        self.adjustSize()
        self.fixScroll()
        Widget.fontChanged(self)
        
    def fixScroll(self):
        if self.isFocused() == True:
            caretX=self.getFont().getWidth(self.mText[:self.mCaretPosition])
            if caretX-self.mXScroll >= self.getWidth()-4:
                self.mXScroll = caretX-self.getWidth()+4
            elif caretX - self.mXScroll <= 0:
                self.mXScroll=caretX-self.getWidth()/2
                if self.mXScroll<0:
                    self.mXScroll=0
                    
            self.addDirtyRect()
                    
    def draw(self,graphics):
        faceColor=self.getBaseColor()
        highlightColor, shadowColor = Color(), Color()
        
        alpha=faceColor.a
        highlightColor=faceColor + 0x303030
        highlightColor.a=alpha
        shadowColor=faceColor - 0x303030
        shadowColor.a=alpha
        #Draw a border.
        graphics.setColor(shadowColor)
        graphics.drawLine(0,0,self.getWidth()-1,0)
        graphics.drawLine(0,1,0,self.getHeight()-2)
        graphics.setColor(highlightColor)
        graphics.drawLine(self.getWidth()-1,1,self.getWidth()-1,self.getHeight()-1)
        graphics.drawLine(0,self.getHeight()-1,self.getWidth()-1,self.getHeight()-1)
        
        #Push a clip area so the other drawings don't need to worry
        #about the border.
        graphics.pushClipArea( Rectangle(1,1,self.getWidth()-2,self.getHeight()-2) )
        
        graphics.setColor(self.getBackgroundColor())
        graphics.fillRectangle( Rectangle(0,0,self.getWidth(),self.getHeight()) )
        
        if self.isFocused() == True:
            self.drawCaret(graphics, self.getFont().getWidth(self.mText[:self.mCaretPosition]) - self.mXScroll )
            
        graphics.setColor(self.getBackgroundColor())
        graphics.setFont(self.getFont())
        graphics.drawText(self.mText,1-self.mXScroll,1, self.getTextColor())
        
        graphics.popClipArea()
        
        
    def drawCaret(self,graphics,x):
        #Check the current clip area as a clip area with a different
        #size than the widget might have been pushed (which is the
        #case in the draw method when we push a clip area after we have
        #drawn a border).
        clipArea=graphics.getCurrentClipArea()
        
        graphics.setColor(self.getForegroundColor())
        if self.mInsert==True:
            graphics.drawLine(x,clipArea.height-2,x,1)
        else:
            graphics.drawLine(x,clipArea.height/2-2,x,1)
            graphics.drawLine(x,clipArea.height/2+2,x,clipArea.height-2)
        
    def mousePressed(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT:
            self.mCaretPosition=self.getFont().getStringIndexAt(self.mText, mouseEvent.getX()+self.mXScroll)
            self.fixScroll()
            mouseEvent.consume()
            
    def mouseDragged(self,mouseEvent):
        mouseEvent.consume()
        
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        
        if key.getValue() == Key.LEFT and self.mCaretPosition > 0:
            self.mCaretPosition-=1
            
        elif key.getValue() == Key.RIGHT and self.mCaretPosition < len(self.mText):
            self.mCaretPosition+=1
            
        elif key.getValue() == Key.DELETE and self.mCaretPosition < len(self.mText):
            p=self.mText[:self.mCaretPosition]+self.mText[self.mCaretPosition+1:]
            self.mText=p
            
        elif key.getValue() == Key.BACKSPACE and self.mCaretPosition > 0:
            p=self.mText[:self.mCaretPosition-1]+self.mText[self.mCaretPosition:]
            self.mText=p
            self.mCaretPosition-=1
            
        elif key.getValue() == Key.ENTER:
            self.distributeActionEvent()
            
        elif key.getValue() == Key.HOME:
            self.mCaretPosition=0
            
        elif key.getValue() == Key.END:
            self.mCaretPosition=len(self.mText)
            
        elif key.getValue() == Key.INSERT:
            self.toggleInsert()
            
        elif key.isCharacter() == True and key.getValue() != Key.TAB:
            if self.mInsert == True:
                text=self.mText[:self.mCaretPosition]+chr(key.getValue())+self.mText[self.mCaretPosition:]
            else:
                text=self.mText[:self.mCaretPosition]+chr(key.getValue())+self.mText[self.mCaretPosition+1:]
            
            if len(text) <= self.mMaxSize or self.mMaxSize < 0:
                self.mText=text
                self.mCaretPosition+=1
        
        if key.getValue() != Key.TAB:
            keyEvent.consume()
            
        self.fixScroll()
    
    def adjustHeight(self):
        self.setHeight(self.getFont().getHeight()+4)
    
    def adjustSize(self):
        self.setWidth(self.getFont().getWidth(self.mText)+6)
        self.adjustHeight()
        self.fixScroll()
    