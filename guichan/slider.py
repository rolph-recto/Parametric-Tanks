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

class Slider(Widget,MouseListener,KeyListener,FocusListener):
    class Orientation:
        HORIZONTAL=0
        VERTICAL=1
        
    def __init__(self,scaleStart,scaleEnd=None):
        Widget.__init__(self)
        self.mDragged=False
        
        if scaleEnd == None:
            self.mScaleStart=float(0.0)
            self.mScaleEnd=float(scaleStart)
        else:
            self.mScaleStart=float(scaleStart)
            self.mScaleEnd=float(scaleEnd)
            
        self.setFocusable(True)
        self.setFrameSize(1)
        self.setOrientation(Slider.Orientation.HORIZONTAL)
        self.mValue=self.mScaleStart
        self.setStepLength( (self.mScaleEnd-self.mScaleStart)/10 )
        self.setMarkerLength(10)
        
        self.addMouseListener(self)
        self.addKeyListener(self)
        self.addFocusListener(self)
        
    def setScale(self,scaleStart,scaleEnd):
        self.mScaleStart=scaleStart
        self.mScaleEnd=scaleEnd
        self.addDirtyRect()
    
    def setScaleStart(self,scaleStart):
        self.mScaleStart=scaleStart
        self.addDirtyRect()
        
    def setScaleEnd(self,scaleEnd):
        self.mScaleEnd=scaleEnd
        self.addDirtyRect()
        
    def getScaleStart(self):
        return self.mScaleStart
    
    def getScaleEnd(self):
        return self.mScaleEnd
    
    def setValue(self,value):
        oValue=self.mValue
        if value > self.mScaleEnd:
            self.mValue=float(self.mScaleEnd)
            
        elif value < self.mScaleStart:
            self.mValue=float(self.mScaleStart)
            
        else:
            self.mValue=float(value)
        
        oPos=self.valueToMarkerPosition(oValue)
        nPos=self.valueToMarkerPosition(self.mValue)
        aRect=self.getAbsoluteDimension()
        r, r2=Rectangle(aRect), Rectangle(aRect)
        if self.mOrientation == Slider.Orientation.HORIZONTAL:
            r.x+=oPos
            r2.x+=nPos
        else:
            r.y+=oPos
            r2.y+=nPos
        
        self.addDirtyRect(r+r2)
            
    def getValue(self):
        return self.mValue
    
    def setMarkerLength(self,length):
        self.mMarkerLength=length
        self.addDirtyRect()
        
    def getMarkerLength(self):
        return self.mMarkerLength
        self.addDirtyRect()
    
    def setOrientation(self,orientation):
        self.mOrientation=orientation
        self.addDirtyRect()
        
    def getOrientation(self):
        return self.mOrientation
    
    def setStepLength(self,length):
        self.mStepLength=float(length)
        
    def getStepLength(self):
        return self.mStepLength
    
    def getMarkerPosition(self):
        return self.valueToMarkerPosition(self.getValue())
    
    def markerPositionToValue(self,v):
        w=self.getHeight()
        if self.mOrientation == Slider.Orientation.HORIZONTAL:
            w=self.getWidth()
            
        pos = float(v) / float(w-self.getMarkerLength())
        
        return float(1.0 * pos) * float(self.mScaleStart) + float(pos) * float(self.mScaleEnd)
    
    def valueToMarkerPosition(self,value):
        v=self.getHeight()
        if self.mOrientation == Slider.Orientation.HORIZONTAL:
            v=self.getWidth()
            
        w=int( (v-self.getMarkerLength()) * (value-self.mScaleStart) / (self.mScaleEnd-self.mScaleStart) )
        
        if w < 0:
            return 0
        
        elif w > v - self.getMarkerLength():
            return v - self.getMarkerLength()
        
        else:
            return w
        
    def draw(self,graphics):
        shadowColor=self.getBaseColor()-0x101010
        alpha=self.getBaseColor().a
        shadowColor.a=alpha
        
        graphics.setColor(shadowColor)
        graphics.fillRectangle( Rectangle(0,0,self.getWidth(),self.getHeight()) )
        
        self.drawMarker(graphics)
        
    def drawMarker(self,graphics):
        faceColor=Color( self.getBaseColor() )
        alpha=faceColor.a
        highlightColor=faceColor+0x303030
        highlightColor.a=alpha
        shadowColor=faceColor-0x303030
        shadowColor.a=alpha
        
        graphics.setColor(faceColor)
        
        if self.mOrientation == Slider.Orientation.HORIZONTAL:
            v=self.getMarkerPosition()
            graphics.fillRectangle( Rectangle(v+1, 1, self.getMarkerLength()-2, self.getHeight()-2) )
            graphics.setColor(highlightColor)
            graphics.drawLine(v, 0, v+self.getMarkerLength()-1, 0)
            graphics.drawLine(v, 0, v, self.getHeight()-1)
            graphics.setColor(shadowColor)
            graphics.drawLine(v+self.getMarkerLength()-1, 1, v+self.getMarkerLength()-1, self.getHeight()-1)
            graphics.drawLine(v+1, self.getHeight()-1, v+self.getMarkerLength()-1, self.getHeight()-1)
            
            if self.isFocused() == True:
                graphics.setColor( self.getForegroundColor() )
                graphics.drawRectangle( Rectangle(v+2, 2, self.getMarkerLength()-4, self.getHeight()-4) )
                
        else:
            v=( self.getMarkerPosition())
            graphics.fillRectangle( Rectangle(1, v+1, self.getWidth()-2, self.getMarkerLength()-2) )
            graphics.setColor(highlightColor)
            graphics.drawLine(0, v, 0, v+self.getMarkerLength()-1)
            graphics.drawLine(0, v, self.getWidth()-1, v)
            graphics.setColor(shadowColor)
            graphics.drawLine(1, v+self.getMarkerLength()-1, self.getWidth()-1, v+self.getMarkerLength()-1)
            graphics.drawLine(self.getWidth()-1, v+1, self.getWidth()-1, v+self.getMarkerLength()-1)
            
            if self.isFocused() == True:
                graphics.setColor(self.getForegroundColor())
                graphics.drawRectangle( Rectangle(2, v+2, self.getWidth()-4, self.getMarkerLength()-4) )
                
    def mousePressed(self,mouseEvent):
        button, x, y = mouseEvent.getButton(), mouseEvent.getX(), mouseEvent.getY()
        if button == MouseEvent.LEFT and x >= 0 and x <= self.getWidth() and y >=0 and y <= self.getHeight():
            if self.mOrientation == Slider.Orientation.HORIZONTAL:
                self.setValue( self.markerPositionToValue(mouseEvent.getX()-self.getMarkerLength()/2) )
            else:
                self.setValue( self.markerPositionToValue(mouseEvent.getY()-self.getMarkerLength()/2) )
                
            self.distributeActionEvent()
            
    def mouseDragged(self,mouseEvent):
        if self.mOrientation == Slider.Orientation.HORIZONTAL:
            self.setValue( self.markerPositionToValue(mouseEvent.getX()-self.getMarkerLength()/2) )
        else:
            self.setValue( self.markerPositionToValue(mouseEvent.getY()-self.getMarkerLength()/2) )
                
        self.distributeActionEvent()
        mouseEvent.consume()
        
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        
        if self.mOrientation == Slider.Orientation.HORIZONTAL:
            if key.getValue() == Key.RIGHT:
                self.setValue( self.getValue()+self.getStepLength() )
                self.distributeActionEvent()
                keyEvent.consume()
            elif key.getValue() == Key.LEFT:
                self.setValue( self.getValue()-self.getStepLength() )
                self.distributeActionEvent()
                keyEvent.consume()
                
        else:
            if key.getValue() == Key.DOWN:
                self.setValue( self.getValue()+self.getStepLength() )
                self.distributeActionEvent()
                keyEvent.consume()
            elif key.getValue() == Key.UP:
                self.setValue( self.getValue()-self.getStepLength() )
                self.distributeActionEvent()
                keyEvent.consume()
                
    def focusGained(self,event):
        self.addDirtyRect()
        
    def focusLost(self,event):
        self.addDirtyRect()    
            
            
            
            
                
        
        
        