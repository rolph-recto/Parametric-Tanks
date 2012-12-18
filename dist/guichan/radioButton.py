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

class RadioButton(Widget,MouseListener,KeyListener):
    mGroupMap={}
    def __init__(self,caption="",group="",selected=False):
        Widget.__init__(self)
        self.mSelected=selected
        self.mGroup=""
        self.setCaption(caption)
        self.setGroup(group)
        self.setSelected(selected)
        
        self.setFocusable(True)
        self.addMouseListener(self)
        self.addKeyListener(self)
        
        self.adjustSize()
    
    def setCaption(self,caption,adjust=True):
        self.mCaption=caption
        if adjust == True:
            self.adjustSize()
        else:
            self.addDirtyRect()
        
    def getCaption(self):
        return self.mCaption
        
    def setGroup(self,group):
        if self.mGroup != "":
            RadioButton.mGroupMap[self.mGroup].remove(self)
            
        if group != "":
            #Add group if it doesn't exist
            if group not in RadioButton.mGroupMap:
                RadioButton.mGroupMap[group]=[]
                
            RadioButton.mGroupMap[group].append(self)
            
        self.mGroup=group
        
    def getGroup(self):
        return self.mGroup
    
    def setSelected(self,selected):
        if selected == True and self.mGroup != "":
            for i in RadioButton.mGroupMap[self.mGroup]:
                if i.getSelected() == True:
                    i.setSelected(False)
                    
        self.mSelected=selected
        self.addDirtyRect()
        
    def getSelected(self):
        return self.mSelected
    
    def adjustSize(self):
        height=self.getFont().getHeight()
        
        self.setHeight(height)
        self.setWidth(self.getFont().getWidth(self.mCaption) + height + height/2)
        
    def draw(self,graphics):
        graphics.pushClipArea( Rectangle(1,1,self.getWidth()-1,self.getHeight()-1) )
        self.drawBox(graphics)
        graphics.popClipArea()
        
        graphics.setFont(self.getFont())
        graphics.setColor(self.getForegroundColor())
        
        if self.isFocused() == True:
            fh=0
            
            if self.getHeight()%2 == 0:
                fh=self.getHeight()-4
            else:
                fh=self.getHeight()-3
                
            hh=(fh+1)/2
            
            graphics.drawLine(0, hh+1, hh+1, 0)
            graphics.drawLine(hh+2, 1, fh+2, hh+1)
            graphics.drawLine(fh+1, hh+2, hh+1, fh+2)
            graphics.drawLine(hh+1, fh+2, 1, hh+2)
            
        h=self.getHeight()+self.getHeight()/2
        
        graphics.drawText(self.getCaption(), h-2, 0, self.getTextColor())
        
    def drawBox(self,graphics):
        h=0
        if self.getHeight()%2 == 0:
            h=self.getHeight()-4
        else:
            h=self.getHeight()-3
            
        alpha=self.getBaseColor().a
        faceColor=self.getBaseColor()
        highlightColor=faceColor+0x303030
        highlightColor.a=alpha
        shadowColor=faceColor-0x303030
        shadowColor.a=alpha
        
        graphics.setColor(self.getBackgroundColor())
        hh=(h+1)/2
        
        for i in range(1,hh+1):
            graphics.drawLine(hh-i+1, i, hh+i-1, i)
        
        for i in range(1,hh):
            graphics.drawLine(hh-i+1, h-i, hh+i-1, h-i)
            
        graphics.setColor(shadowColor)
        graphics.drawLine(hh, 0, 0, hh)
        graphics.drawLine(hh+1, 1, h-1, hh-1)
        
        graphics.setColor(highlightColor)
        graphics.drawLine(1, hh+1, hh, h)
        graphics.drawLine(hh+1, h-1, h, hh)
        
        graphics.setColor(self.getForegroundColor())
        
        hhh=hh-3
        if self.mSelected == True:
            for i in range(hhh):
                graphics.drawLine(hh-i, 4+1, hh+i, 4+i)
                graphics.drawLine(hh-i, h-4-i, hh+i, h-4-i)
                
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        if key.getValue() == Key.ENTER or key.getValue == Key.SPACE:
            self.setSelected(True)
            self.distributeActionEvent()
            keyEvent.consume()
            
    def mouseClicked(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT:
            self.setSelected(True)
            self.distributeActionEvent()
            
    def mouseDragged(self,mouseEvent):
        mouseEvent.consume()

    def adjustSize(self):
        height=self.getFont().getHeight()

        self.setHeight(height)
        self.setWidth(self.getFont().getWidth(self.getCaption()) + height + height/2)
