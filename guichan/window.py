#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from container import Container
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from mouseInput import MouseInput

class Window(Container,MouseListener):
    def __init__(self,caption=""):
        Container.__init__(self)
        self.mMoved=False
        self.mDragOffsetX=-1
        self.mDragOffsetY=-1
        self.setCaption(caption)
        self.setFrameSize(1)
        self.setPadding(2)
        self.setTitleBarHeight(16)
        self.setAlignment(Graphics.CENTER)
        self.addMouseListener(self)
        self.setMovable(True)
        self.setOpaque(True)
        
    def setPadding(self,padding):
        self.mPadding=padding
        self.addDirtyRect()
    
    def getPadding(self):
        return self.mPadding
    
    def setCaption(self,caption):
        self.mCaption=caption
        self.addDirtyRect()
        
    def getCaption(self):
        return self.mCaption
    
    def setMovable(self,movable):
        self.mMovable=movable
        
    def isMovable(self):
        return self.mMovable
    
    def setAlignment(self,align):
        self.mAlignment=align
        self.addDirtyRect()
        
    def getAlignment(self):
        return self.mAlignment
    
    def setTitleBarHeight(self,titleBarHeight):
        self.mTitleBarHeight=titleBarHeight
        self.addDirtyRect()
        
    def getTitleBarHeight(self):
        return self.mTitleBarHeight
    
    def setOpaque(self,opaque):
        self.mOpaque=opaque
        
    def isOpaque(self):
        return self.mOpaque
    
    def draw(self,graphics):
        faceColor=self.getBaseColor()
        highlightColor, shadowColor = Color(), Color()
        
        alpha=faceColor.a
        width=self.getWidth()+self.getFrameSize()*2-1
        height=self.getHeight()+self.getFrameSize()*2-1
        highlightColor=faceColor + 0x303030
        highlightColor.a=alpha
        shadowColor=faceColor - 0x303030
        shadowColor.a=alpha
        
        d=self.getChildrenArea()
        
        #Fill the background around the content
        graphics.setColor(faceColor)
        #Fill top
        graphics.fillRectangle( Rectangle(0, 0, self.getWidth(), d.y-1) )
        #Fill left
        graphics.fillRectangle( Rectangle(0, d.y-1, d.x-1, self.getHeight()-d.y+1) )
        #Fill right
        graphics.fillRectangle( Rectangle(d.x+d.width+1, d.y-1, self.getWidth()-d.x-d.width-1, self.getHeight()-d.y+1) )
        #Fill bottom
        graphics.fillRectangle( Rectangle(d.x-1, d.y+d.height+1, d.width+2, self.getHeight()-d.height-d.y-1) )
        
        if self.isOpaque() == True:
            graphics.fillRectangle(d)
            
        #Construct a rectangle one pixel bigger than the content
        d.x-=1
        d.y-=1
        d.width+=2
        d.height+=2
        
        #Draw a border around the content
        graphics.setColor(shadowColor)
        #Top line
        graphics.drawLine(d.x, d.y, d.x+d.width-2, d.y)
        #Left line
        graphics.drawLine(d.x, d.y+1, d.x, d.y+d.height-1)
        
        graphics.setColor(highlightColor)
        #Right line
        graphics.drawLine(d.x+d.width-1, d.y, d.x+d.width-1, d.y+d.height-2)
        #Bottom line
        graphics.drawLine(d.x+1, d.y+d.height-1, d.x+d.width-1, d.y+d.height-1)
        
        self.drawChildren(graphics)
        
        textX, textY = 0, 0
        
        textY = (self.getTitleBarHeight()-self.getFont().getHeight()) /2
        align = self.getAlignment()
        
        if align == Graphics.LEFT:
            textX=4
        elif align == Graphics.CENTER:
            textX=self.getWidth()/2
        elif align == Graphics.RIGHT:
            textX=self.getWidth()-4
        else:
            raise GCN_EXCEPTION("Unknown alignment.")
        
        graphics.setColor(self.getForegroundColor())
        graphics.setFont(self.getFont())
        graphics.pushClipArea( Rectangle(0,0,self.getWidth(),self.getTitleBarHeight()-1) )
        graphics.drawText(self.getCaption(), textX, textY, align, self.getTextColor())
        graphics.popClipArea()
        
    def mousePressed(self,mouseEvent):
        if mouseEvent.getSource() != self:
            return None
        
        if self.getParent() != None:
            self.getParent().moveToTop(self)
            
        self.mDragOffsetX=mouseEvent.getX()
        self.mDragOffsetY=mouseEvent.getY()
        
        self.mMoved=mouseEvent.getY() <= self.mTitleBarHeight
        
    def mouseReleased(self,mouseEvent):
        self.mMoved=False
        
    def mouseDragged(self,mouseEvent):
        if mouseEvent.isConsumed() == True or mouseEvent.getSource() != self:
            return None
        
        if self.isMovable() == True and self.mMoved == True:
            self.setPosition(mouseEvent.getX()-self.mDragOffsetX+self.getX(), mouseEvent.getY()-self.mDragOffsetY+self.getY())
            
        mouseEvent.consume()
        
    def getChildrenArea(self):
        return Rectangle(self.getPadding(), self.getTitleBarHeight(), self.getWidth()-self.getPadding()*2, self.getHeight()-self.getPadding()-self.getTitleBarHeight())
    
    def resizeToContent(self):
        w, h=0, 0
        for i in self.mWidgets:
            if i.getX()+i.getWidth() > w:
                w=i.getX()+i.getWidth()
            if i.getY()+i.getHeight() > h:
                h=i.getY()+i.getHeight()
        
        self.setSize(w+2*self.getPadding(), h+self.getPadding()+self.getTitleBarHeight())
        self.addDirtyRect()
        
            

        
    
    