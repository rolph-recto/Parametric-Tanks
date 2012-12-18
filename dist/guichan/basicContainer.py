#!/usr/bin/env python

from guichan import *
from widget import Widget
from deathListener import DeathListener

class BasicContainer(Widget, DeathListener):
    def __init__(self):
        Widget.__init__(self)
        self.mWidgets=[]
        
    def __del__(self):
        Widget.__del__(self)
        self.clear()
        
    def moveToTop(self,widget):
        found=self.hasWidget(widget)
        if found > -1:
            self.mWidgets.pop(found)
        else:
            raise GCN_EXCEPTION("There is no such widget in this container.")
            
        self.mWidgets.append(widget)
            
    def moveToBottom(self,widget):
        found=self.hasWidget(widget)
        if found > -1:
            self.mWidgets.pop(found)
        else:
            raise GCN_EXCEPTION("There is no such widget in this container.")
            
        self.mWidget.insert(0,widget)
        
    def death(self,event):
        if self.mWidgets.count(event.getSource()) > 0:
            self.mWidgets.remove(event.getSource())
        else:
            raise GCN_EXCEPTION("There is no such widget in this container.")
        
    def getChildrenArea(self):
        return Rectangle(0,0,self.getWidth(),self.getHeight())

    def iterateFocus(self,direction):
        for i in range(len(self.mWidgets)):
            if self.mWidgets[i]().isFocused() == True:
                break
            
        end=i
        if i == len(self.mWidgets):
            i=0
        if i == 0:
            i=len(self.mWidgets)
            
        i+=direction
        while i != end:
            if i == len(self.mWidgets):
                i=0
            if i == 0:
                i=len(self.mWidgets)
                
            if self.mWidgets[i]().isFocusable() == True:
                self.mWidgets[i]().requestFocus()
                break
            
            i+=direction
            
    def focusNext(self):
        self.iterateFocus(1)
        
    def focusPrevious(self):
        self.iterateFocus(-1)
        
    def getWidgetAt(self,x,y):
        r=self.getChildrenArea()
        if r.isPointInRect(x,y) == False:
            return None
        
        x-=r.x
        y-=r.y
        for i in range(len(self.mWidgets)-1,-1,-1):
            if self.mWidgets[i].isVisible() == True and self.mWidgets[i].getDimension().isPointInRect(x,y) == True:
                widget=self.mWidgets[i]
                return widget
            
        return None
    
    def logic(self):
        self.logicChildren()
        
    def setFocusHandler(self,focusHandler):
        Widget.setFocusHandler(self,focusHandler)
        if self.mInternalFocusHandler != None:
            return None
        
        for i in self.mWidgets:
            i.setFocusHandler(focusHandler)
            
    def setDirtyRectangle(self,dirtyRect):
        Widget.setDirtyRectangle(self,dirtyRect)
        for i in self.mWidgets:
            i.setDirtyRectangle(dirtyRect)
            
    def add(self,widget):
        self.mWidgets.append(widget)
        
        if self.mInternalFocusHandler == None:
            widget.setFocusHandler(self.getFocusHandler())
        else:
            widget.setFocusHandler(self.mInternalFocusHandler)
            
        widget.setDirtyRectangle(self.getDirtyRectangle())
            
        widget.setParent(self)
        widget.addDeathListener(self)
        
        if widget.isVisible() == True:
            widget.addDirtyRect()
        
        """
        #adjust alpha to container's alpha
        widget.setBaseColor(widget.getBaseColor())
        widget.setForegroundColor(widget.getForegroundColor())
        widget.setBackgroundColor(widget.getBackgroundColor())
        widget.setSelectionColor(widget.getSelectionColor())
        """
        
    def remove(self,widget):
        found=self.hasWidget(widget)
        if found > -1:
            self.mWidgets.pop(found)
            widget.setFocusHandler(None)
            widget.setParent(None)
            widget.removeDeathListener(self)
            found=True
                
        else:
            raise GCN_EXCEPTION("There is no such widget in this container.")
        
    def clear(self):
        for i in self.mWidgets:
            widget=i
            self.mWidgets.remove(i)
            widget.setFocusHandler(None)
            widget.setParent(None)
            widget.removeDeathListener(self)
            
        del self.mWidgets[:]
    
    def hasWidget(self,widget):
        if self.mWidgets.count(widget) > 0:
            return self.mWidgets.index(widget)
        
        else:
            return -1
    
    def drawChildren(self,graphics):
        graphics.pushClipArea( self.getChildrenArea() )
        
        for i in self.mWidgets:
            """
            Optimized draw means that only widgets who
            are updated in a dirty rect are drawn. When enabled,
            Guichan runs A LOT faster (tests indicate acceleration
            from 125 to 500 FPS!), but may screw up some widgets
            as their draw() function isn't being called.
            
            It has some drawbacks, though. For example, widgets that
            move a lot (especially windows) have to be drawn every time
            they move, so optimized draw doesn't have much effect on them.
            The only solution I have right now is to limit the movement
            of widgets (ie, disable movement for windows).
            Also, widgets have to specify themselves when they are 'dirty',
            which can confuse people who want to make custom widgets.
            """
            if self.getDirtyRectangle().isDrawOptimized() == True:
                drawOptimized=self.getDirtyRectangle().isRectInDirtyRect(i.getAbsoluteDimension()) == True
            else:
                drawOptimized=True
            
            if i.isVisible() == True and drawOptimized == True:
                #If the widget has a frame,
                # draw it before drawing the widget
                if i.getFrameSize() > 0:
                    rec = Rectangle(i.getDimension())
                    rec.x-=i.getFrameSize()
                    rec.y-=i.getFrameSize()
                    rec.width+=2*i.getFrameSize()
                    rec.height+=2*i.getFrameSize()
                    graphics.pushClipArea(rec)
                    i.drawFrame(graphics)
                    graphics.popClipArea()
                
                graphics.pushClipArea(i.getDimension())
                i.draw(graphics)
                graphics.popClipArea()
                
        
        graphics.popClipArea()
        
    def logicChildren(self):
        for i in self.mWidgets:
            i.logic()
            
    def showWidgetPart(self,widget,area):
        widgetArea=self.getChildrenArea()
        area.x=area.x+widget.getX()
        area.y=area.y+widget.getY()
        
        if area.x+area.width > widgetArea.width:
            widget.setX(widget.getX()-area.x-area.width+widgetArea.width)
            
        if area.y+area.height > widgetArea.height:
            widget.setY(widget.getY()-area.y-area.height+widgetArea.height)
            
        if area.x < 0:
            widget.setX(widget.getX() - area.x)
            
        if area.y < 0:
            widget.setY(widget.getY() - area.y)
            
    def setInternalFocusHandler(self,focusHandler):
        Widget.setInternalFocusHandler(self,focusHandler)
        for i in self.mWidgets:
            if self.mInternalFocusHandler == None:
                i.setFocusHandler(self.getFocusHandler())
            else:
                i.setFocusHandler(self.mInternalFocusHandler)
                
                
    def findWidgetById(self,id):
        for i in self.mWidgets:
            if i.getId() == id:
                return i
            
            if isinstance(i,BasicContainer) == True:
                widget = None
                widget = i.findWidgetById(id)
                if widget != None:
                    return widget
                
        return None
    
    def setBaseColor(self,color):
        Widget.setBaseColor(self,color)
    
    def setForegroundColor(self,color):
        Widget.setForegroundColor(self,color)
    
    def setBackgroundColor(self,color):
        Widget.setBackgroundColor(self,color)
    
    def setSelectionColor(self,color):
        Widget.setSelectionColor(self,color)
        """
        for i in self.mWidgets:
            if i.getSelectionColor().a > self.mSelectionColor.a:
                c=Color(i.getSelectionColor())
                c.a=self.mSelectionColor.a
                i.setSelectionColor(c)
        """
                
    def shutDown(self):
        for i in self.mWidgets:
            i.shutDown()
                
        self.clear()
    
                


            
