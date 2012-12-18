#!/usr/bin/env python

from guichan import *
from defaultFont import DefaultFont
from keyInput import KeyInput
from keyListener import KeyListener
from mouseInput import MouseInput
from mouseListener import MouseListener
from widgetListener import WidgetListener
from deathListener import DeathListener
from actionListener import ActionListener
from focusHandler import FocusHandler
from actionEvent import ActionEvent
from graphics import Graphics

class Widget:
    mWidgets=[]
    mGlobalFont=None
    mDefaultFont=DefaultFont()
    def __init__(self):
        self.mDimension=Rectangle()
        self.mForegroundColor=Color(0x000000)
        self.mBackgroundColor=Color(0xFFFFFF)
        self.mBaseColor=Color(0x808090)
        self.mSelectionColor=Color(0xC3D9FF)
        self.mTextColor=Color(0x000000)
        self.mFocusHandler=None
        self.mInternalFocusHandler=None
        self.mDirtyRect=None
        self.mParent=None
        self.mFrameSize=0
        self.mFocusable=False
        self.mVisible=True
        self.mTabIn=True
        self.mTabOut=True
        self.mEnabled=True
        self.mCurrentFont=None
        self.mId=""
        self.mActionEventId=""
        self.mMouseListeners=[]
        self.mKeyListeners=[]
        self.mActionListeners=[]
        self.mDeathListeners=[]
        self.mFocusListeners=[]
        self.mWidgetListeners=[]
        Widget.mWidgets.append(weakref.ref(self))
        
    def __del__(self):
        for i in self.mDeathListeners:
            i().death( Event(self) )
        
        for i in Widget.mWidgets:
            widget2=i()
            if widget2 == self:
                Widget.mWidgets.remove(i)
                
        self.setFocusHandler(None)
        
    def drawFrame(self,graphics):
        faceColor=self.getBaseColor()
        highlightColor, shadowColor=Color(), Color()
        alpha=self.getBaseColor().a
        width=self.getWidth() + self.getFrameSize()*2 - 1
        height=self.getHeight() + self.getFrameSize()*2 - 1
        highlightColor=faceColor+0x303030
        highlightColor.a=alpha
        shadowColor=faceColor-0x303030
        shadowColor.a=alpha
        
        for i in range(self.getFrameSize()):
            graphics.setColor(shadowColor)
            graphics.drawLine(i, i, width-i, i)
            graphics.drawLine(i, i+1, i, height-i-1)
            
            graphics.setColor(highlightColor)
            graphics.drawLine(width-i, i+1, width-i, height-i)
            graphics.drawLine(i, height-i, width-i-1, height-i)
            
    def setParent(self,widget):
        if widget != None:
            self.mParent=widget
        else:
            self.mParent=None
        
    def getParent(self):
        if self.mParent != None:
            parent=self.mParent
            return parent
        
        return None
        
    def setWidth(self,width):
        newDimension=Rectangle(self.mDimension)
        newDimension.width=width
        self.setDimension(newDimension)
        
    def getWidth(self):
        return self.mDimension.width
    
    def setHeight(self,height):
        newDimension=Rectangle(self.mDimension)
        newDimension.height=height
        self.setDimension(newDimension)
        
    def getHeight(self):
        return self.mDimension.height
    
    def setX(self,x):
        newDimension=Rectangle(self.mDimension)
        newDimension.x=x
        self.setDimension(newDimension)
        
    def getX(self):
        return self.mDimension.x
    
    def setY(self,y):
        newDimension=Rectangle(self.mDimension)
        newDimension.y=y
        self.setDimension(newDimension)
        
    def getY(self):
        return self.mDimension.y
    
    def setPosition(self,x,y):
        newDimension=Rectangle(self.mDimension)
        newDimension.y=y
        newDimension.x=x
        self.setDimension(newDimension)
        
    def setSize(self,width,height):
        newDimension=Rectangle(self.mDimension)
        newDimension.width=width
        newDimension.height=height
        self.setDimension(newDimension)        
    
    def setDimension(self,dimension):
        aOldDimension=self.getAbsoluteDimension()
        oldDimension=self.mDimension
        self.mDimension=dimension
        
        if dimension.width != oldDimension.width or dimension.height != oldDimension.height:
            self.distributeResizedEvent()
            self.addDirtyRect( aOldDimension+self.getAbsoluteDimension() )
            
        if dimension.x != oldDimension.x or dimension.y != oldDimension.y:
            self.distributeMovedEvent()
            self.addDirtyRect( aOldDimension+self.getAbsoluteDimension() )
            
    def setFrameSize(self,size):
        if self.mFrameSize != size:
            self.mFrameSize=size
            self.addDirtyRect()
        
    def getFrameSize(self):
        return self.mFrameSize
    
    def getDimension(self):
        return self.mDimension
    
    def setActionEventId(self,id):
        self.mActionEventId=id
        
    def getActionEventId(self):
        return self.mActionEventId
    
    def isFocused(self):
        if self.mFocusHandler == None:
            return false
        else:
            return self.mFocusHandler.isFocused(self)
        
    def setFocusable(self,focusable):
        if focusable == False and self.isFocused() == True:
            self.mFocusHandler.focusNone()
        
        self.mFocusable=focusable
        
    def isFocusable(self):
        return self.mFocusable and self.isVisible() and self.isEnabled()
    
    def requestFocus(self):
        if self.mFocusHandler == None:
            raise GCN_EXCEPTION("Requested focus but no focushandler set.")
        
        if self.isFocusable() == True:
            self.mFocusHandler.requestFocus(self)
            
    def requestMoveToTop(self):
        if self.mParent != None:
            self.mParent.moveToTop(self)
            
    def requestMoveToBottom(self):
        if self.mParent != None:
            self.mParent.moveToBottom(self)
        
    def setVisible(self,visible):
        if visible == False and self.isFocused() == True:
            self.mFocusHandler.focusNone()
            
        if visible == True:
            self.distributeShownEvent()
        elif visible == False:
            self.distributeHiddenEvent()
            
        self.mVisible=visible
        
    def isVisible(self):
        if self.mParent == None:
            return self.mVisible
        else:
            return self.mVisible and self.getParent().isVisible()
        
    def setBaseColor(self,color):
        self.mBaseColor=color
        self.addDirtyRect()
        
    def getBaseColor(self):
        return self.mBaseColor
    
    def setForegroundColor(self,color):
        self.mForegroundColor=color
        self.addDirtyRect()
        
    def getForegroundColor(self):
        return self.mForegroundColor
    
    def setBackgroundColor(self,color):
        self.mBackgroundColor=color
        self.addDirtyRect()
        """
        if self.mParent != None:
            if self.mParent.getBackgroundColor().a < self.mBackgroundColor.a:
                self.mBackgroundColor.a=self.mParent.getBackgroundColor().a
                
        if self.mBaseColor.a > self.mBackgroundColor.a:
            self.mBaseColor.a=self.mBackgroundColor.a
            
        if self.mForegroundColor.a > self.mBackgroundColor.a:
            self.mForegroundColor.a=self.mBackgroundColor.a
            
        if self.mSelectionColor.a > self.mBackgroundColor.a:
            self.mSelectionColor.a=self.mBackgroundColor.a
        """
        
    def getBackgroundColor(self):
        return self.mBackgroundColor
    
    def setSelectionColor(self,color):
        self.mSelectionColor=color
        self.addDirtyRect()
        
    def getSelectionColor(self):
        return self.mSelectionColor
    
    def setTextColor(self,color):
        self.mTextColor=color
        self.addDirtyRect()
        
    def getTextColor(self):
        return self.mTextColor
    
    def setFocusHandler(self,focusHandler):
        if self.mFocusHandler != None:
            self.releaseModalFocus()
            self.mFocusHandler.remove(self)
            
        if focusHandler != None:
            focusHandler.add(self)
        
        self.mFocusHandler=focusHandler

    def getFocusHandler(self):
        return self.mFocusHandler
    
    def setDirtyRectangle(self,dirtyRect):
        self.mDirtyRect=dirtyRect
        
    def getDirtyRectangle(self):
        return self.mDirtyRect
    
    def addDirtyRect(self, rect=None):
        if type(rect) == type(None):
            rect=self.getAbsoluteDimension()
            
        if self.mDirtyRect != None and self.mVisible == True:
            self.mDirtyRect.addRect(rect)
    
    def addActionListener(self,listener):
        self.mActionListeners.append(weakref.ref(listener))
    
    def removeActionListener(self,listener):
        for i in self.mActionListeners:
            if i() == listener:
                self.mActionListeners.remove(i)
        
    def addDeathListener(self,listener):
        self.mDeathListeners.append(weakref.ref(listener))
    
    def removeDeathListener(self,listener):
        for i in self.mDeathListeners:
            if i() == listener:
                self.mDeathListeners.remove(i)
        
    def addKeyListener(self,listener):
        self.mKeyListeners.append(weakref.ref(listener))
    
    def removeKeyListener(self,listener):
        for i in self.mKeyListeners:
            listen=i()
            if listen == listener:
                self.mKeyListeners.remove(i)
        
    def addFocusListener(self,listener):
        self.mFocusListeners.append(weakref.ref(listener))
    
    def removeFocusListener(self,listener):
        for i in self.mFocusListeners:
            listen=i()
            if listen == listener:
                self.mFocusListeners.remove(i)
        
    def addMouseListener(self,listener):
        self.mMouseListeners.append(weakref.ref(listener))
    
    def removeMouseListener(self,listener):
        for i in self.mMouseListeners:
            listen=i()
            if listen == listener:
                self.mMouseListeners.remove(i)
        
    def addWidgetListener(self,listener):
        self.mWidgetListeners.append(weakref.ref(listener))
    
    def removeWidgetListener(self,listener):
        for i in self.mWidgetListeners:
            listen=i()
            if listen == listener:
                self.mWidgetListeners.remove(i)

    def getAbsolutePosition(self):
        if self.mParent == None:
            return self.mDimension.x, self.mDimension.y
        else:
            parentX, parentY = self.getParent().getAbsolutePosition()
            x=parentX + self.mDimension.x + self.getParent().getChildrenArea().x
            y=parentY + self.mDimension.y + self.getParent().getChildrenArea().y
            return x, y
        
    def getAbsoluteX(self):
        if self.mParent == None:
            return self.mDimension.x
        else:
            parentX, parentY = self.getParent().getAbsolutePosition()
            x=parentX + self.mDimension.x + self.getParent().getChildrenArea().x
            return x
    
    def getAbsoluteY(self):
        if self.mParent == None:
            return self.mDimension.y
        else:
            parentX, parentY = self.getParent().getAbsolutePosition()
            y=parentY + self.mDimension.y + self.getParent().getChildrenArea().y
            return y
        
    def getAbsoluteDimension(self):
        if self.mParent == None:
            return Rectangle(self.getDimension())
        else:
            parentX, parentY = self.getParent().getAbsolutePosition()
            x=parentX + self.mDimension.x + self.getParent().getChildrenArea().x
            y=parentY + self.mDimension.y + self.getParent().getChildrenArea().y
            return Rectangle(x-self.mFrameSize, y-self.mFrameSize, self.getWidth()+self.mFrameSize*2, self.getHeight()+self.mFrameSize*2)
    
    def getFont(self):
        if self.mCurrentFont == None:
            if Widget.mGlobalFont == None:
                return Widget.mDefaultFont
            else:
                return Widget.mGlobalFont
        else:
            return self.mCurrentFont
    
    @staticmethod    
    def setGlobalFont(font):
        Widget.mGlobalFont=font
        for i in Widget.mWidgets:
            if i().mCurrentFont == None:
                i().fontChanged()
                
    def setFont(self,font):
        self.mCurrentFont=font
        self.fontChanged()
        
    @staticmethod
    def widgetExists(widget):
        exist=False
        eWidget=None
        for i in Widget.mWidgets:
            eWidget=i()
            if eWidget is widget:
                exist=True
            
        return exist
    
    def isTabInEnabled(self):
        return self.mTabIn
    
    def setTabInEnabled(self,tabIn):
        self.mTabIn=tabIn
        
    def isTabOutEnabled(self):
        return self.mTabOut
    
    def setTabOutEnabled(self,tabOut):
        self.mTabOut=tabOut
    
    def setEnabled(self,enabled):
        self.mEnabled=enabled
        
    def isEnabled(self):
        return self.mEnabled and self.isVisible()
    
    def requestModalFocus(self):
        if self.mFocusHandler == None:
            raise GCN_EXCEPTION("Requested modal focus but no focushandler set.")
        
        self.mFocusHandler.requestModalFocus(self)
        
    def requestModalMouseInputFocus(self):
        if self.mFocusHandler == None:
            raise GCN_EXCEPTION("Requested modal mouse input focus but no focushandler set.")
        
        self.mFocusHandler.requestModalMouseInputFocus(self)
        
    def releaseModalFocus(self):
        if self.mFocusHandler == None:
            return None
        
        self.mFocusHandler.releaseModalFocus(self)
        
    def releaseModalMouseInputFocus(self):
        if self.mFocusHandler == None:
            return None
        
        self.mFocusHandler.releaseModalMouseInputFocus(self)
        
    def isModalFocused(self):
        if self.mFocusHandler == None:
            raise GCN_EXCEPTION("No focushandler set (did you add the widget to the gui?).")
        
        if self.mParent != None:
            return (self.mFocusHandler.getModalFocused() == self) or self.mParent.isModalFocused()
        
        return self.mFocusHandler.getModalFocused() == self
    
    def isModalMouseInputFocused(self):
        if self.mFocusHandler == None:
            raise GCN_EXCEPTION("No focushandler set (did you add the widget to the gui?).")
        
        if self.mParent != None:
            return self.mFocusHandler.isModalMouseInputFocused(self) or self.mParent.isModalMouseInputFocused()
        
        return self.mFocusHandler.getModalMouseInputFocused() == self
    
    def getWidgetAt(self,x,y):
        return None
    
    def getMouseListeners(self):
        return self.mMouseListeners
    
    def getKeyListeners(self):
        return self.mKeyListeners
    
    def getFocusListeners(self):
        return self.mFocusListeners
    
    def getChildrenArea(self):
        return Rectangle(0,0,0,0)
    
    def getInternalFocusHandler(self):
        return self.mInternalFocusHandler
    
    def setInternalFocusHandler(self,focusHandler):
        self.mInternalFocusHandler=focusHandler
        
    def setId(self,id):
        self.mId=id
        
    def getId(self):
        return self.mId
    
    def distributeResizedEvent(self):
        for i in self.mWidgetListeners:
            i().widgetResized( Event(weakref.proxy(self)) )
            
    def distributeMovedEvent(self):
        for i in self.mWidgetListeners:
            i().widgetMoved( Event(weakref.proxy(self)) )
            
    def distributeHiddenEvent(self):
        for i in self.mWidgetListeners:
            i().widgetHidden( Event(weakref.proxy(self)) )

    def distributeShownEvent(self):
        for i in self.mWidgetListeners:
            i().widgetShown( Event(weakref.proxy(self)) )      
            
    def distributeActionEvent(self):
        for i in self.mActionListeners:
            i().action( ActionEvent(weakref.proxy(self),self.mActionEventId) )
            
    def showPart(self,rect):
        if self.mParent != None:
            self.getParent().showWidgetPart(self,rect)
    
    def shutDown(self):
        pass
    
    #overridden functions
    def draw(self):
        pass
    
    def logic(self):
        pass
    
    def fontChanged(self):
        self.addDirtyRect()
    
    def moveToTop(self):
        pass
    
    def moveToBottom(self):
        pass
    
    def focusNext(self):
        pass
    
    def focusPrevious(self):
        pass
    
    def showWidgetPart(self,rect):
        pass
        
        