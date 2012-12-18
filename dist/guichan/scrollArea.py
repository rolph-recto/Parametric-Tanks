#!/usr/bin/env python

from guichan import *
from basicContainer import BasicContainer
from widget import Widget
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from graphics import Graphics

class ScrollArea(BasicContainer,MouseListener):
    SHOW_ALWAYS = 0
    SHOW_NEVER  = 1
    SHOW_AUTO   = 2
    
    def __init__(self,content=None,hPolicy=SHOW_AUTO,vPolicy=SHOW_AUTO):
        BasicContainer.__init__(self)
        
        self.mVScroll=0
        self.mHScroll=0
        self.mHPolicy=hPolicy
        self.mVPolicy=vPolicy
        self.mScrollbarWidth=12
        self.mUpButtonPressed=False
        self.mDownButtonPressed=False
        self.mLeftButtonPressed=False
        self.mRightButtonPressed=False
        self.mIsVerticalMarkerDragged=False
        self.mIsHorizontalMarkerDragged=False
        self.mUpButtonScrollAmount=10
        self.mDownButtonScrollAmount=10
        self.mLeftButtonScrollAmount=10
        self.mRightButtonScrollAmount=10
        self.mHorizontalMarkerDragOffset=0
        self.mVerticalMarkerDragOffset=0
        self.mVBarVisible=False
        self.mHBarVisible=False
        self.mOpaque=True
        self.mContent=None
        
        self.setContent(content)
        self.addMouseListener(self)
        
    def __del__(self):
        Widget.__del__(self)
        self.setContent(None)
        
    def setContent(self,widget):
        if widget != None:
            self.clear()
            self.add(widget)
            widget.setPosition(0,0)
            self.mContent=widget
        
        else:
            self.clear()
            
        self.checkPolicies()
        
    def getContent(self):
        if len(self.mWidgets) > 0:
            return self.mWidgets[0]
        
        return None
    
    def setHorizontalScrollPolicy(self,policy):
        self.mHPolicy=policy
        self.checkPolicies()
        
    def getHorizontalScrollPolicy(self):
        return self.mHPolicy
        
    def setVerticalScrollPolicy(self,policy):
        self.mVPolicy=policy
        self.checkPolicies()
        
    def getVerticalScrollPolicy(self):
        return self.mVPolicy
    
    def setScrollPolicy(self,hPolicy,vPolicy):
        self.mHPolicy=hPolicy
        self.mVPolicy=vPolicy
        
        self.checkPolicies()
        
    def setVerticalScrollAmount(self,vScroll):
        max=self.getVerticalMaxScroll()
        
        if vScroll > max:
            self.mVScroll=max
            
        elif vScroll < 0:
            self.mVScroll=0
            
        else:
            self.mVScroll=vScroll
            
    def getVerticalScrollAmount(self):
        return self.mVScroll
    
    def setHorizontalScrollAmount(self,hScroll):
        max=self.getHorizontalMaxScroll()
        
        if hScroll > max:
            self.mHScroll=max
            
        elif hScroll < 0:
            self.mHScroll=0
            
        else:
            self.mHScroll=hScroll
            
    def getHorizontalScrollAmount(self):
        return self.mHScroll
    
    def setScrollAmount(self,hScroll,vScroll):
        self.setHorizontalScrollAmount(hScroll)
        self.setVerticalScrollAmount(vScroll)
        
    def getHorizontalMaxScroll(self):
        self.checkPolicies()
        
        if self.mContent == None:
            return 0
        
        value=self.getContent().getWidth()-self.getChildrenArea().width+2*self.getContent().getFrameSize()
        
        if value < 0:
            value = 0
            
        return value
    
    def getVerticalMaxScroll(self):
        self.checkPolicies()
        
        if self.mContent == None:
            return 0
        
        value=self.getContent().getHeight()-self.getChildrenArea().height+2*self.getContent().getFrameSize()
        
        if value < 0:
            value = 0
            
        return value
    
    def setScrollbarWidth(self,width):
        if width > 0:
            self.mScrollbarWidth=width
            
        else:
            raise GCN_EXCEPTION("Width should be greater than 0.")
            
            
    def getScrollbarWidth(self):
        return self.mScrollbarWidth
    
    def mousePressed(self,mouseEvent):
        x=mouseEvent.getX()
        y=mouseEvent.getY()
        
        if self.getUpButtonDimension().isPointInRect(x,y) == True:
            self.setVerticalScrollAmount(self.getVerticalScrollAmount()-self.mUpButtonScrollAmount)
            self.mUpButtonPressed=True
            
        elif self.getDownButtonDimension().isPointInRect(x,y) == True:
            self.setVerticalScrollAmount(self.getVerticalScrollAmount()+self.mDownButtonScrollAmount)
            self.mDownButtonPressed=True
            
        elif self.getLeftButtonDimension().isPointInRect(x,y) == True:
            self.setHorizontalScrollAmount(self.getHorizontalScrollAmount() - self.mLeftButtonScrollAmount)
            self.mLeftButtonPressed=True
            
        elif self.getRightButtonDimension().isPointInRect(x,y) == True:
            self.setHorizontalScrollAmount(self.getHorizontalScrollAmount() + self.mRightButtonScrollAmount)
            self.mRightButtonPressed=True
            
        elif self.getVerticalMarkerDimension().isPointInRect(x,y) == True:
            self.mIsHorizontalMarkerDragged = False
            self.mIsVerticalMarkerDragged = True
            
            self.mVerticalMarkerDragOffset=y-self.getVerticalMarkerDimension().y
            
        elif self.getVerticalBarDimension().isPointInRect(x,y) == True:
            if y < self.getVerticalMarkerDimension().y:
                self.setVerticalScrollAmount(self.getVerticalScrollAmount() - int(self.getChildrenArea().height * 0.95))
                
            else:
                self.setVerticalScrollAmount(self.getVerticalScrollAmount() + int(self.getChildrenArea().height * 0.95))
                
        elif self.getHorizontalMarkerDimension().isPointInRect(x,y) == True:
            self.mIsHorizontalMarkerDragged = True
            self.mIsVerticalMarkerDragged = False
            
            self.mHorizontalMarkerDragOffset=x-self.getHorizontalMarkerDimension().x
            
        elif self.getHorizontalBarDimension().isPointInRect(x,y) == True:
            if x < self.getHorizontalMarkerDimension().x:
                self.setHorizontalScrollAmount(self.getHorizontalScrollAmount() - int(self.getChildrenArea().width * 0.95))
                
            else:
                self.setHorizontalScrollAmount(self.getHorizontalScrollAmount() + int(self.getChildrenArea().width * 0.95))
                
    def mouseReleased(self,mouseEvent):
        self.mUpButtonPressed=False
        self.mDownButtonPressed=False
        self.mLeftButtonPressed=False
        self.mRightButtonPressed=False
        self.mIsHorizontalMarkerDragged = False
        self.mIsVerticalMarkerDragged = False
        
        mouseEvent.consume()
        
    def mouseDragged(self,mouseEvent):
        x, y=mouseEvent.getX(), mouseEvent.getY()
        
        if self.mIsVerticalMarkerDragged == True:
            pos=y - self.getVerticalBarDimension().y - self.mVerticalMarkerDragOffset
            length=self.getVerticalMarkerDimension().height
            
            barDim = Rectangle(self.getVerticalBarDimension())
            
            if barDim.height-length > 0:
                self.setVerticalScrollAmount((self.getVerticalMaxScroll() * pos) / (barDim.height - length))
                
            else:
                self.setVerticalScrollAmount(0)
                
        if self.mIsHorizontalMarkerDragged == True:
            pos=x - self.getHorizontalBarDimension().x - self.mHorizontalMarkerDragOffset
            length=self.getHorizontalMarkerDimension().width
            
            barDim = Rectangle(self.getHorizontalBarDimension())
            
            if barDim.width-length > 0:
                self.setHorizontalScrollAmount((self.getHorizontalMaxScroll() * pos) / (barDim.width - length))
                
            else:
                self.setHorizontalScrollAmount(0)
                
        mouseEvent.consume()
        
    def draw(self,graphics):
        self.drawBackground(graphics)
        
        if self.mVBarVisible == True:
            self.drawUpButton(graphics)
            self.drawDownButton(graphics)
            self.drawVBar(graphics)
            self.drawVMarker(graphics)
            
        if self.mHBarVisible == True:
            self.drawLeftButton(graphics)
            self.drawRightButton(graphics)
            self.drawHBar(graphics)
            self.drawHMarker(graphics)
            
        if self.mHBarVisible == True and self.mVBarVisible == True:
            graphics.setColor(self.getBaseColor())
            graphics.fillRectangle( Rectangle(self.getWidth()-self.mScrollbarWidth, self.getHeight()-self.mScrollbarWidth, self.mScrollbarWidth, self.mScrollbarWidth) )
            
        self.drawChildren(graphics)
        
    def drawHBar(self,graphics):
        dim=self.getHorizontalBarDimension()
        
        graphics.pushClipArea(dim)
        
        alpha=self.getBaseColor().a
        trackColor=self.getBaseColor() - 0x101010
        trackColor.a=alpha
        shadowColor=self.getBaseColor() - 0x303030
        shadowColor.a=alpha
        
        graphics.setColor(trackColor)
        graphics.fillRectangle(Rectangle(0, 0, dim.width, dim.height))
        
        graphics.setColor(shadowColor)
        graphics.drawLine(0, 0, dim.width, 0)
        
        graphics.popClipArea()
        
    def drawVBar(self,graphics):
        dim=self.getVerticalBarDimension()
        
        graphics.pushClipArea(dim)
        
        alpha=self.getBaseColor().a
        trackColor=self.getBaseColor() - 0x101010
        trackColor.a=alpha
        shadowColor=self.getBaseColor() - 0x303030
        shadowColor.a=alpha
        
        graphics.setColor(trackColor)
        graphics.fillRectangle(Rectangle(0, 0, dim.width, dim.height))
        
        graphics.setColor(shadowColor)
        graphics.drawLine(0, 0, 0, dim.height)
        
        graphics.popClipArea()
        
    def drawBackground(self,graphics):
        if self.isOpaque() == True:
            graphics.setColor(self.getBackgroundColor())
            graphics.fillRectangle(self.getChildrenArea())
            
    def drawUpButton(self,graphics):
        dim=self.getUpButtonDimension()
        graphics.pushClipArea(dim)
        
        highlightColor, shadowColor, faceColor = None, None, None
        offset=0
        alpha=self.getBaseColor().a
        
        if self.mUpButtonPressed == True:
            faceColor=self.getBaseColor() - 0x303030
            faceColor.a=alpha
            highlightColor=self.getBaseColor() - 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor()
            shadowColor.a=alpha
            
            offset=1
            
        else:
            faceColor=self.getBaseColor()
            faceColor.a=alpha
            highlightColor=self.getBaseColor() + 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor() - 0x303030
            shadowColor.a=alpha
            
            offset=0
            
        graphics.setColor(faceColor)
        graphics.fillRectangle(Rectangle(0,0,dim.width,dim.height))
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0,0,dim.width-1,0)
        graphics.drawLine(0,1,0,dim.height-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(dim.width-1, 0, dim.width-1, dim.height-1)
        graphics.drawLine(1, dim.height-1, dim.width-1, dim.height-1)
        
        graphics.setColor(self.getForegroundColor())
        
        w=dim.height/2
        h=w/2+2
        for i in range(int(w/2)):
            graphics.drawLine(w-i+offset, i+h+offset, w+i+offset, i+h+offset)
            
        graphics.popClipArea()

    def drawDownButton(self,graphics):
        dim=self.getDownButtonDimension()
        graphics.pushClipArea(dim)
        
        highlightColor, shadowColor, faceColor = None, None, None
        offset=0
        alpha=self.getBaseColor().a
        
        if self.mDownButtonPressed == True:
            faceColor=self.getBaseColor() - 0x303030
            faceColor.a=alpha
            highlightColor=self.getBaseColor() - 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor()
            shadowColor.a=alpha
            
            offset=1
            
        else:
            faceColor=self.getBaseColor()
            faceColor.a=alpha
            highlightColor=self.getBaseColor() + 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor() - 0x303030
            shadowColor.a=alpha
            
            offset=0
            
        graphics.setColor(faceColor)
        graphics.fillRectangle(Rectangle(0,0,dim.width,dim.height))
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0,0,dim.width-1,0)
        graphics.drawLine(0,1,0,dim.height-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(dim.width-1, 0, dim.width-1, dim.height-1)
        graphics.drawLine(1, dim.height-1, dim.width-1, dim.height-1)
        
        graphics.setColor(self.getForegroundColor())
        
        w=dim.height/2
        h=w/2+2
        for i in range(int(w/2)):
            graphics.drawLine(w-i+offset, -i+h+offset, w+i+offset, -i+h+offset)
            
        graphics.popClipArea()
        
    def drawLeftButton(self,graphics):
        dim=self.getLeftButtonDimension()
        graphics.pushClipArea(dim)
        
        highlightColor, shadowColor, faceColor = None, None, None
        offset=0
        alpha=self.getBaseColor().a
        
        if self.mLeftButtonPressed == True:
            faceColor=self.getBaseColor() - 0x303030
            faceColor.a=alpha
            highlightColor=self.getBaseColor() - 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor()
            shadowColor.a=alpha
            
            offset=1
            
        else:
            faceColor=self.getBaseColor()
            faceColor.a=alpha
            highlightColor=self.getBaseColor() + 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor() - 0x303030
            shadowColor.a=alpha
            
            offset=0
            
        graphics.setColor(faceColor)
        graphics.fillRectangle(Rectangle(0, 0, dim.width, dim.height))
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0, 0, dim.width-1, 0)
        graphics.drawLine(0, 1, 0, dim.height-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(dim.width-1, 0, dim.width-1, dim.height-1)
        graphics.drawLine(1, dim.height-1, dim.width-1, dim.height-1)
        
        graphics.setColor(self.getForegroundColor())
        
        w=dim.width/2
        h=w-2
        for i in range(int(w/2)):
            graphics.drawLine(i+h+offset, w-i+offset, i+h+offset, w+i+offset)
            
        graphics.popClipArea()
        
    def drawRightButton(self,graphics):
        dim=self.getRightButtonDimension()
        graphics.pushClipArea(dim)
        
        highlightColor, shadowColor, faceColor = None, None, None
        offset=0
        alpha=self.getBaseColor().a
        
        if self.mRightButtonPressed == True:
            faceColor=self.getBaseColor() - 0x303030
            faceColor.a=alpha
            highlightColor=self.getBaseColor() - 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor()
            shadowColor.a=alpha
            
            offset=1
            
        else:
            faceColor=self.getBaseColor()
            faceColor.a=alpha
            highlightColor=self.getBaseColor() + 0x303030
            highlightColor.a=alpha
            shadowColor=self.getBaseColor() - 0x303030
            shadowColor.a=alpha
            
            offset=0
            
        graphics.setColor(faceColor)
        graphics.fillRectangle(Rectangle(0, 0, dim.width, dim.height))
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0, 0, dim.width-1, 0)
        graphics.drawLine(0, 1, 0, dim.height-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(dim.width-1, 0, dim.width-1, dim.height-1)
        graphics.drawLine(1, dim.height-1, dim.width-1, dim.height-1)
        
        graphics.setColor(self.getForegroundColor())
        
        w=dim.width/2
        h=w+1
        for i in range(int(w/2)):
            graphics.drawLine(-i+h+offset, w-i+offset, -i+h+offset, w+i+offset)
            
        graphics.popClipArea()
        
    def drawVMarker(self,graphics):
        dim=self.getVerticalMarkerDimension()
        graphics.pushClipArea(dim)
        
        alpha=self.getBaseColor().a
        faceColor=self.getBaseColor()
        faceColor.a=alpha
        highlightColor=self.getBaseColor() + 0x303030
        highlightColor.a=alpha
        shadowColor=self.getBaseColor() - 0x303030
        shadowColor.a=alpha
        
        graphics.setColor(faceColor)
        graphics.fillRectangle(Rectangle(1, 1, dim.width-1, dim.height-1))
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0, 0, dim.width-1, 0)
        graphics.drawLine(0, 1, 0, dim.height-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(1, dim.height-1, dim.width-1, dim.height-1)
        graphics.drawLine(dim.width-1, 0, dim.width-1, dim.height-1)
        
        graphics.popClipArea()
        
    def drawHMarker(self,graphics):
        dim=self.getHorizontalMarkerDimension()
        graphics.pushClipArea(dim)
        
        alpha=self.getBaseColor().a
        faceColor=self.getBaseColor()
        faceColor.a=alpha
        highlightColor=self.getBaseColor() + 0x303030
        highlightColor.a=alpha
        shadowColor=self.getBaseColor() - 0x303030
        shadowColor.a=alpha
        
        graphics.setColor(faceColor)
        graphics.fillRectangle(Rectangle(1, 1, dim.width-1, dim.height-1))
        
        graphics.setColor(highlightColor)
        graphics.drawLine(0, 0, dim.width-1, 0)
        graphics.drawLine(0, 1, 0, dim.height-1)
        
        graphics.setColor(shadowColor)
        graphics.drawLine(1, dim.height-1, dim.width-1, dim.height-1)
        graphics.drawLine(dim.width-1, 0, dim.width-1, dim.height-1)
        
        graphics.popClipArea()
            
    def logic(self):
        self.checkPolicies()
        
        self.setVerticalScrollAmount(self.getVerticalScrollAmount())
        self.setHorizontalScrollAmount(self.getHorizontalScrollAmount())
        
        if self.getContent() != None:
            frameSize=self.getContent().getFrameSize()
            self.mContent.setPosition(-self.mHScroll+frameSize, -self.mVScroll+frameSize)
            self.getContent().logic()
            
    def checkPolicies(self):
        w=self.getWidth()
        h=self.getHeight()
        
        self.mHBarVisible=False
        self.mVBarVisible=True
        
        if self.getContent() == None:
            self.mHBarVisible= (self.mHPolicy==ScrollArea.SHOW_ALWAYS)
            self.mVBarVisible= (self.mVPolicy==ScrollArea.SHOW_ALWAYS)
            return None
        
        if self.mHPolicy == ScrollArea.SHOW_AUTO and self.mVPolicy == ScrollArea.SHOW_AUTO:
            if self.getContent().getWidth() <= w and self.getContent().getHeight() <= h:
                self.mHBarVisible=False
                self.mVBarVisible=False
                
            if self.getContent().getWidth() > w:
                self.mHBarVisible=True
                
            if (self.getContent().getHeight() > h) or (self.mHBarVisible == True and self.getContent().getHeight() > h - self.mScrollbarWidth):
                self.mVBarVisible=True
                
            if self.mVBarVisible == True and self.getContent().getWidth() > w - self.mScrollbarWidth:
                self.mHBarVisible=True
                
            return None
        
        #horizontal bar
        if self.mHPolicy == SHOW_NEVER:
            self.mHBarVisible=False
            
        elif self.mHPolicy == SHOW_ALWAYS:
        
            self.mHBarVisible=True
    
        elif self.mHPolicy == SHOW_AUTO:
            if self.mVPolicy == SHOW_NEVER:
                self.mHBarVisible=self.getContent().getWidth() > w
            
            else:
                self.mHBarVisible=self.getContent.getWidth() > w-self.mScrollbarWidth
                
        else:
            raise GCN_EXCEPTION("Horizontal scroll policy invalid.")
        
        #vertical bar
        if self.mVPolicy == SHOW_NEVER:
            self.mVBarVisible=False

        elif self.mVPolicy == SHOW_NEVER:
            self.mVBarVisible=True

        elif self.mVPolicy == SHOW_AUTO:
            if self.mHPolicy == SHOW_NEVER:
                self.mVBarVisible = self.getContent().getHeight() > h
                
            else:
                self.mVBarVisible = self.getContent().getHeight() > h - self.mScrollbarWidth
                
        else:
            raise GCN_EXCEPTION("Vertical scroll policy invalid.")
            
    def getUpButtonDimension(self):
        if self.mVBarVisible == False:
            return Rectangle(0,0,0,0)
            
        return Rectangle(self.getWidth() - self.mScrollbarWidth, 0, self.mScrollbarWidth, self.mScrollbarWidth)
        
    def getDownButtonDimension(self):
        if self.mVBarVisible == False:
            return Rectangle(0,0,0,0)
            
        if self.mVBarVisible and self.mHBarVisible:
            return Rectangle(self.getWidth() - self.mScrollbarWidth, self.getHeight() - self.mScrollbarWidth*2, self.mScrollbarWidth, self.mScrollbarWidth)

        return Rectangle(self.getWidth() - self.mScrollbarWidth, self.getHeight() - self.mScrollbarWidth, self.mScrollbarWidth, self.mScrollbarWidth)
                
    def getLeftButtonDimension(self):
        if self.mHBarVisible == False:
            return Rectangle(0,0,0,0)
            
        return Rectangle(0,self.getHeight()-self.mScrollbarWidth,self.mScrollbarWidth,self.mScrollbarWidth)
        
    def getRightButtonDimension(self):
        if self.mHBarVisible == False:
            return Rectangle(0,0,0,0)
            
        if self.mVBarVisible and self.mHBarVisible:
            return Rectangle(self.getWidth()-self.mScrollbarWidth*2, self.getHeight()-self.mScrollbarWidth, self.mScrollbarWidth, self.mScrollbarWidth)
        
        return Rectangle(self.getWidth()-self.mScrollbarWidth, self.getHeight()-self.mScrollbarWidth, self.mScrollbarWidth, self.mScrollbarWidth)
        
    def getChildrenArea(self):
        if self.mVBarVisible and self.mHBarVisible:
            return Rectangle(0, 0, self.getWidth()-self.mScrollbarWidth, self.getHeight()-self.mScrollbarWidth)
        
        if self.mVBarVisible:
            return Rectangle(0, 0, self.getWidth()-self.mScrollbarWidth, self.getHeight())
        
        if self.mHBarVisible:
            return Rectangle(0, 0, self.getWidth(), self.getHeight()-self.mScrollbarWidth)
            
        return Rectangle(0, 0, self.getWidth(), self.getHeight())
        
    def getVerticalBarDimension(self):
        if self.mVBarVisible == False:
            return Rectangle(0,0,0,0)
            
        if self.mHBarVisible:
            return Rectangle(self.getWidth()-self.mScrollbarWidth, self.getUpButtonDimension().height, self.mScrollbarWidth, self.getHeight()-self.getUpButtonDimension().height-self.getDownButtonDimension().height-self.mScrollbarWidth)
            
        return Rectangle(self.getWidth()-self.mScrollbarWidth, self.getUpButtonDimension().height, self.mScrollbarWidth, self.getHeight()-self.getUpButtonDimension().height-self.getDownButtonDimension().height)
        
    def getHorizontalBarDimension(self):
        if self.mHBarVisible == False:
            return Rectangle(0,0,0,0)
            
        if self.mVBarVisible:
            return Rectangle(self.getLeftButtonDimension().width,self.getHeight()-self.mScrollbarWidth,self.getWidth()-self.getLeftButtonDimension().width-self.getRightButtonDimension().width-self.mScrollbarWidth,self.mScrollbarWidth)
            
        return Rectangle(self.getLeftButtonDimension().width,self.getHeight()-self.mScrollbarWidth,self.getWidth()-self.getLeftButtonDimension().width-self.getRightButtonDimension().width,self.mScrollbarWidth)
        
    def getVerticalMarkerDimension(self):
        if self.mVBarVisible == False:
            return Rectangle(0,0,0,0)
            
        length, pos=0, 0
        barDim=Rectangle(self.getVerticalBarDimension())
        
        if self.getContent() != None and self.getContent().getHeight() != 0:
            length=(barDim.height*self.getChildrenArea().height)/self.getContent().getHeight()
        else:
            length=barDim.height
            
        if length < self.mScrollbarWidth:
            length=self.mScrollbarWidth
            
        if length > barDim.height:
            length=barDim.height
            
        if self.getVerticalMaxScroll() != 0:
            pos=((barDim.height-length) * self.getVerticalScrollAmount()) / self.getVerticalMaxScroll()
        else:
            pos=0
            
        return Rectangle(barDim.x, barDim.y+pos, self.mScrollbarWidth, length)
            
    def getHorizontalMarkerDimension(self):
        if self.mHBarVisible == False:
            return Rectangle(0,0,0,0)
            
        length, pos=0, 0
        barDim=Rectangle(self.getHorizontalBarDimension())
        
        if self.getContent() != None and self.getContent().getWidth() != 0:
            length=(barDim.width*self.getChildrenArea().width)/self.getContent().getWidth()
        else:
            length=barDim.width
            
        if length < self.mScrollbarWidth:
            length=self.mScrollbarWidth
            
        if length > barDim.width:
            length=self.barDim.width
            
        if self.getHorizontalMaxScroll() != 0:
            pos=((barDim.width-length) * self.getHorizontalScrollAmount()) / self.getHorizontalMaxScroll()
        else:
            pos=0
            
        return Rectangle(barDim.x+pos, barDim.y, length, self.mScrollbarWidth)        
    
    def showWidgetPart(self, widget, area):
        if widget != self.getContent():
            raise GCN_EXCEPTION("Widget not content widget")
            
        BasicContainer.showWidgetPart(self, widget, area)
        
        self.setHorizontalScrollAmount(self.getContent().getFrameSize()-self.getContent().getX())
        self.setVerticalScrollAmount(self.getContent().getFrameSize()-self.getContent().getY())
        
    def getWidgetAt(self, x, y):
        if self.getChildrenArea().isPointInRect(x, y):
            return self.getContent()
            
        return None
    
    def mouseWheelMovedUp(self, mouseEvent):
        if mouseEvent.isConsumed():
            return
        
        self.setVerticalScrollAmount(self.getVerticalScrollAmount()-self.getChildrenArea().height/8)
        mouseEvent.consume()
        
    def mouseWheelMovedDown(self, mouseEvent):
        if mouseEvent.isConsumed():
            return
        
        self.setVerticalScrollAmount(self.getVerticalScrollAmount()+self.getChildrenArea().height/8)
        mouseEvent.consume() 
        
    def setWidth(self, width):
        Widget.setWidth(self, width)
        self.checkPolicies()
        
    def setHeight(self, height):
        Widget.setHeight(self, height)
        self.checkPolicies()
        
    def setDimension(self, dimension):
        Widget.setDimension(self, dimension)
        self.checkPolicies()
        
    def setLeftButtonScrollAmount(self, amount):
        self.mLeftButtonScrollAmount=amount
        
    def setRightButtonScrollAmount(self, amount):
        self.mRightButtonScrollAmount=amount
        
    def setUpButtonScrollAmount(self, amount):
        self.mUpButtonScrollAmount=amount
        
    def setDownButtonScrollAmount(self, amount):
        self.mDownButtonScrollAmount=amount
        
    def getLeftButtonScrollAmount(self):
        return self.mLeftButtonScrollAmount
    
    def getRightButtonScrollAmount(self):
        return self.mRightButtonScrollAmount
    
    def getUpButtonScrollAmount(self):
        return self.mUpButtonScrollAmount
    
    def getDownButtonScrollAmount(self):
        return self.mDownButtonScrollAmount
    
    def setOpaque(self, opaque):
        self.mOpaque=opaque
        
    def isOpaque(self):
        return self.mOpaque
    
    #DONE WITH THE LONGEST SOURCE FILE EVER!