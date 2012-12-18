#!/usr/bin/env python

from guichan import *
from widget import Widget
from basicContainer import BasicContainer
from graphics import Graphics
from graphics import Graphics
from mouseEvent import MouseEvent
from mouseInput import MouseInput
from mouseListener import MouseListener
from event import Event
from keyEvent import KeyEvent
from key import Key
from keyInput import KeyInput
from keyListener import KeyListener
from focusHandler import FocusHandler

class Gui:
    def __init__(self):
        self.mTop=None
        self.mGraphics=None
        self.mTop=None
        self.mInput=None
        self.mTabbing=True
        self.mShiftPressed=False
        self.mMetaPressed=False
        self.mControlPressed=False
        self.mAltPressed=False
        self.mLastMousePressButton=0
        self.mLastMousePressTimeStamp=0
        self.mLastMouseX=0
        self.mLastMouseY=0
        self.mClickCount=1
        self.mLastMouseDragButton=0
        self.mFocusHandler=FocusHandler()
        self.mDirtyRect=DirtyRectangle()
        self.mKeyListeners=[]
        self.mWidgetWithMouseQueue=[]
        
        self.mDirtyRect.setEnabled(False)
    
    def __del__(self):
        #We assume that there is only one Gui object.
        if Widget.widgetExists(self.mTop):
            #self.mTop.shutDown()
            
            self.mTop.setFocusHandler(None)
            self.mTop=None   
            
    def setDirtyRectEnabled(self,enabled):
        self.mDirtyRect.setEnabled(enabled)
        
    def isDirtyRectEnabled(self):
        return self.mDirtyRect.isEnabled()
    
    def enableDirtyRect(self):
        self.mDirtyRect.setEnabled(True)
        
    def disableDirtyRect(self):
        self.mDirtyRect.setEnabled(False)
            
    def setDrawOptimized(self,draw):
        self.mDirtyRect.setDrawOptimized(draw)
        
    def isDrawOptimized(self):
        return self.mDirtyRect.isDrawOptimized()
    
    def optimizeDraw(self):
        self.mDirtyRect.setDrawOptimized(True)
        
    def deoptimizeDraw(self):
        self.mDirtyRect.setDrawOptimized(False)
    
    def setTop(self,widget):
        if self.mTop != None:
            self.mTop.setFocusHandler(None)
            self.mTop.setDirtyRectangle(None)
        
        if widget != None:
            widget.setFocusHandler(self.mFocusHandler)
            widget.setDirtyRectangle(self.mDirtyRect)
        
        self.mTop=widget
        
    def getTop(self):
        return self.mTop
    
    def setGraphics(self,graphics):
        self.mGraphics=graphics
    
    def getGraphics(self):
        return self.mGraphics
    
    def setInput(self,input):
        self.mInput=input
    
    def getInput(self):
        return self.mInput
    
    def logic(self):
        if self.mTop == None:
            raise GCN_EXCEPTION("No top widget set.")
        
        self.handleModalFocus()
        self.handleModalMouseInputFocus()
        
        if self.mInput != None:
            self.mInput.pollInput()
            
            self.handleKeyInput()
            self.handleMouseInput()
            
        self.mTop.logic()
        
    def draw(self):
        if self.mTop == None:
            raise GCN_EXCEPTION("No top widget set")
        
        if self.mGraphics == None:
            raise GCN_EXCEPTION("No graphics set")
        
        if self.mTop.isVisible() == False:
            return None
        
        self.mGraphics.beginDraw()
        #if top has a frame, draw it before drawing top
        if self.mTop.getFrameSize() > 0:
            rec=Rectangle(self.mTop.getDimension())
            rec.x-=self.mTop.getFrameSize()
            rec.y-=self.mTop.getFrameSize()
            rec.width+=2*self.mTop.getFrameSize()
            rec.height+=2*self.mTop.getFrameSize()
            
        self.mGraphics.pushClipArea( Rectangle(self.mTop.getDimension()) )
        self.mTop.draw(self.mGraphics)
        self.mGraphics.popClipArea()
        
        self.mGraphics.endDraw()
        
    def focusNone(self):
        self.mFocusHandler.focusNone()
        
    def setTabbingEnabled(self,tabbing):
        self.mTabbing=tabbing
        
    def isTabbingEnabled(self):
        return self.mTabbing
    
    def addGlobalKeyListener(self,keyListener):
        self.mKeyListeners.append(keyListener)
        
    def removeGlobalKeyListener(self,keyListener):
        self.mKeyListeners.remove(keyListener)
        
    def handleMouseInput(self):
        while self.mInput.isMouseQueueEmpty() == False:
            mouseInput=self.mInput.dequeueMouseInput()
            self.mLastMouseX=mouseInput.getX()
            self.mLastMouseY=mouseInput.getY()
            type=mouseInput.getType()
            if type == MouseInput.PRESSED:
                self.handleMousePressed(mouseInput)
                
            elif type == MouseInput.RELEASED:
                self.handleMouseReleased(mouseInput)
                
            elif type == MouseInput.MOVED:
                self.handleMouseMoved(mouseInput)
                
            elif type == MouseInput.WHEEL_MOVED_DOWN:
                self.handleMouseWheelMovedDown(mouseInput)
                
            elif type == MouseInput.WHEEL_MOVED_UP:
                self.handleMouseWheelMovedUp(mouseInput)
                
            else:
                raise GCN_EXCEPTION("Unknown mouse input type.")
            
    def handleKeyInput(self):
        while self.mInput.isKeyQueueEmpty() == False:
            keyInput=self.mInput.dequeueKeyInput()
            self.mShiftPressed=keyInput.isShiftPressed()
            self.mControlPressed=keyInput.isControlPressed()
            self.mAltPressed=keyInput.isAltPressed()
            self.mMetaPressed=keyInput.isMetaPressed()
            
            keyEventToGlobalListeners=KeyEvent(None,self.mShiftPressed,self.mControlPressed,self.mAltPressed,self.mMetaPressed,keyInput.getType(),keyInput.isNumericPad(),keyInput.getKey())
            
            self.distributeKeyEventToGlobalListeners(keyEventToGlobalListeners)
            #If a global key listener consumes the event it will not be
            #sent further to the source of the event.
            
            if keyEventToGlobalListeners.isConsumed() == True:
                continue
            
            keyEventConsumed=False
            
            #send keyInputs to focused widgets
            if self.mFocusHandler.getFocused() != None:
                keyEvent=KeyEvent(self.getKeyEventSource(),self.mShiftPressed,self.mControlPressed,self.mAltPressed,self.mMetaPressed,keyInput.getType(),keyInput.isNumericPad(),keyInput.getKey())
                
                if self.mFocusHandler.getFocused().isFocusable() == False:
                    self.mFocusHandler.focusNone()
                else:
                    self.distributeKeyEvent(keyEvent)
                    
                keyEventConsumed=keyEvent.isConsumed()
            
                #If the key event hasn't been consumed and
                #tabbing is enable check for tab press and
                #change focus.
                if keyEventConsumed == False and keyInput.getKey().getValue() == Key.TAB and keyInput.getType() == KeyInput.PRESSED and self.getKeyEventSource().isTabOutEnabled() == True:
                    if keyInput.isShiftPressed() == True:
                        self.mFocusHandler.focusPrevious()
                    else:
                        self.mFocusHandler.focusNext()
                        
    def handleMouseMoved(self,mouseInput):
        if len(self.mWidgetWithMouseQueue) > 0 and ( mouseInput.getX() < 0 or mouseInput.getY() < 0 or self.mTop.getDimension().isPointInRect(mouseInput.getX(),mouseInput.getY()) ) == False:
            #distribute an event to all widgets in the "widget with mouse" queue.
            while len(self.mWidgetWithMouseQueue) > 0:
                widget=self.mWidgetWithMouseQueue[0]
                if Widget.widgetExists(widget):
                    self.distributeMouseEvent(widget,MouseEvent.EXITED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY(),true,true)
                    
                self.mWidgetWithMouseQueue.pop(0)
            
            return None
        
        #Check if there is a need to send mouse exited events by
        #traversing the "widget with mouse" queue.
        widgetWithMouseQueueCheckDone=len(self.mWidgetWithMouseQueue) == 0
        while widgetWithMouseQueueCheckDone == False:
            iterations=0
            for i in self.mWidgetWithMouseQueue:
                widget=i
                
                #If a widget in the "widget with mouse queue" doesn't
                #exist anymore it should be removed from the queue
                if Widget.widgetExists(widget) == False:
                    self.mWidgetWithMouseQueue.remove(widget)
                    break

                else:
                    x, y=widget.getAbsolutePosition()
                    if x > mouseInput.getX() or y > mouseInput.getX() or x+widget.getWidth() <= mouseInput.getX() or y+widget.getHeight() <= mouseInput.getY() or widget.isVisible() == False:
                        self.distributeMouseEvent(widget,MouseEvent.EXITED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY(),true,true)
                        
                        self.mClickCount=1
                        self.mLastMousePressTimeStamp=0
                        self.mWidgetWithMouseQueue.remove(i)
                        break
                
                iterations+=1    
            
            widgetWithMouseQueueCheckDone = iterations == len(self.mWidgetWithMouseQueue)
            
        
        #Check all widgets below the mouse to see if they are
        #present in the "widget with mouse" queue. If a widget
        #is not then it should be added and an entered event should
        #be sent to it.
        parent=self.getMouseEventSource(mouseInput.getX(),mouseInput.getY())
        widget=parent

        #If a widget has modal mouse input focus then it will
        #always be returned from getMouseEventSource, but we only wan't to send
        #mouse entered events if the mouse has actually entered the widget with
        #modal mouse input focus, hence we need to check if that's the case. If
        #it's not we should simply ignore to send any mouse entered events.
        if self.mFocusHandler.getModalMouseInputFocused() == widget and Widget.widgetExists(widget) == True:
            x, y=widget.getAbsolutePosition()
            if x > mouseInput.getX() or y > mouseInput.getY() or x+widget.getWidth() <= mouseInput.getX() or y+widget.getHeight() <= mouseInput.getY():
                parent=None
                
        while parent != None:
            parent=widget.getParent()
            # Check if the widget is present in the "widget with mouse" queue.
            widgetIsPresentInQueue=False
            for i in self.mWidgetWithMouseQueue:
                if i==widget:
                    widgetIsPresentInQueue=True
                    break
                
            # Widget is not present, send an entered event and add
            #it to the "widget with mouse" queue.
            if widgetIsPresentInQueue == False and Widget.widgetExists(widget) == True:
                self.distributeMouseEvent(widget,MouseEvent.ENTERED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY(),True,True)
                self.mWidgetWithMouseQueue.insert(0,widget)
                
            swap = widget
            widget = parent
            parent = swap.getParent()
            
        if self.mFocusHandler.getDraggedWidget() != None:
            #self.distributeMouseEvent(widget,MouseEvent.DRAGGED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY(),True,True)
            self.distributeMouseEvent(self.mFocusHandler.getDraggedWidget(),MouseEvent.DRAGGED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY(),True,True)
        elif Widget.widgetExists(widget):
            self.distributeMouseEvent(widget,MouseEvent.MOVED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY(),True,True)
            
    def handleMousePressed(self,mouseInput):
        sourceWidget=self.getMouseEventSource(mouseInput.getX(),mouseInput.getY())
        if self.mFocusHandler.getDraggedWidget() != None:
            sourceWidget=self.mFocusHandler.getDraggedWidget()
            
        sourceWidgetX, sourceWidgetY=sourceWidget.getAbsolutePosition()
        if ( self.mFocusHandler.getModalFocused() != None and sourceWidget.isModalFocused() == True ) or self.mFocusHandler.getModalFocused() == None:
            sourceWidget.requestFocus()
            
        self.distributeMouseEvent(sourceWidget,MouseEvent.PRESSED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY())
        self.mFocusHandler.setLastWidgetPressed(sourceWidget)
        self.mFocusHandler.setDraggedWidget(sourceWidget)
        self.mLastMouseDragButton=mouseInput.getButton()
        if self.mLastMousePressTimeStamp < 300 and self.mLastMousePressButton == mouseInput.getButton():
            self.mClickCount+=1
        else:
            self.mClickCount=1
            
        self.mLastMousePressButton=mouseInput.getButton()
        currentTimeStamp=self.mLastMousePressTimeStamp
        self.mLastMousePressTimeStamp=mouseInput.getTimeStamp()-currentTimeStamp
        
    def handleMouseWheelMovedUp(self,mouseInput):
        sourceWidget=self.getMouseEventSource(mouseInput.getX(),mouseInput.getY())
        if self.mFocusHandler.getDraggedWidget() != None:
            sourceWidget=self.mFocusHandler.getDraggedWidget()
            
        sourceWidgetX, sourceWidgetY=sourceWidget.getAbsolutePosition()
        self.distributeMouseEvent(sourceWidget,MouseEvent.WHEEL_MOVED_UP,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY())

    def handleMouseWheelMovedDown(self,mouseInput):
        sourceWidget=self.getMouseEventSource(mouseInput.getX(),mouseInput.getY())
        if self.mFocusHandler.getDraggedWidget() != None:
            sourceWidget=self.mFocusHandler.getDraggedWidget()
            
        sourceWidgetX, sourceWidgetY=sourceWidget.getAbsolutePosition()
        self.distributeMouseEvent(sourceWidget,MouseEvent.WHEEL_MOVED_DOWN,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY())
        
    def handleMouseReleased(self,mouseInput):
        sourceWidget=self.getMouseEventSource(mouseInput.getX(),mouseInput.getY())
        if self.mFocusHandler.getDraggedWidget() != None:
            if sourceWidget != self.mFocusHandler.getLastWidgetPressed():
                self.mFocusHandler.setLastWidgetPressed(None)
            sourceWidget=self.mFocusHandler.getDraggedWidget()
            
        sourceWidgetX, sourceWidgetY=sourceWidget.getAbsolutePosition()
        self.distributeMouseEvent(sourceWidget,MouseEvent.RELEASED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY())    
        
        if mouseInput.getButton() == self.mLastMousePressButton and self.mFocusHandler.getLastWidgetPressed() == sourceWidget:
            self.distributeMouseEvent(sourceWidget,MouseEvent.CLICKED,mouseInput.getButton(),mouseInput.getX(),mouseInput.getY())   
        
        else:
            self.mLastMousePressButton=0
            self.mClickCount=0
        
        if self.mFocusHandler.getDraggedWidget() != None:
            self.mFocusHandler.setDraggedWidget(None)
            
    def getWidgetAt(self,x,y):
        #If the widget's parent has no child then we have found the widget..
        parent=self.mTop
        child=self.mTop
        
        while child != None:
            swap = child
            parentX, parentY = parent.getAbsolutePosition()
            child = parent.getWidgetAt(x-parentX,y-parentY)
            parent=swap
        
        return parent
    
    def getMouseEventSource(self,x,y):
        widget=self.getWidgetAt(x,y)
        if self.mFocusHandler.getModalMouseInputFocused() != None and widget.isModalMouseInputFocused():
            return self.mFocusHandler.getModalMouseInputFocused()
        else:
            return widget
        
    def getKeyEventSource(self):
        widget=self.mFocusHandler.getFocused()
        while widget.getInternalFocusHandler() != None and widget.getInternalFocusHandler().getFocused() != None:
            widget = widget.getInternalFocusHandler().getFocused()
            
        return widget
    
    def distributeMouseEvent(self,source,type,button,x,y,force=False,toSourceOnly=False):
        parent=source
        widget=source
        if self.mFocusHandler.getModalFocused() != None and widget.isModalFocused() == False and force == False:
            return None
        if self.mFocusHandler.getModalMouseInputFocused() != None and widget.isModalMouseInputFocused() == False and force == False:
            return None
        mouseEvent=MouseEvent(source,self.mShiftPressed,self.mControlPressed,self.mAltPressed,self.mMetaPressed,type,button,x,y,self.mClickCount)
        while parent != None:
            #If the widget has been removed due to input
            #cancel the distribution.
            if Widget.widgetExists(widget) == False:
                return None
            
            parent=widget.getParent()
            
            if widget.isEnabled() == True or force == True:
                widgetX, widgetY=widget.getAbsolutePosition()
                
                mouseEvent.mX=x-widgetX
                mouseEvent.mY=y-widgetY
                
                mouseListeners=widget.getMouseListeners()
                type=mouseEvent.getType()
                #Send the event to all mouse listeners of the widget.
                for i in mouseListeners:
                    if type == MouseEvent.ENTERED:
                        i().mouseEntered(mouseEvent)
                        
                    elif type == MouseEvent.DRAGGED:
                        i().mouseDragged(mouseEvent)

                    elif type == MouseEvent.EXITED:
                        i().mouseExited(mouseEvent)
                        
                    elif type == MouseEvent.MOVED:
                        i().mouseMoved(mouseEvent)
                        
                    elif type == MouseEvent.PRESSED:
                        i().mousePressed(mouseEvent)
                        
                    elif type == MouseEvent.RELEASED:
                        i().mouseReleased(mouseEvent)
                        
                    elif type == MouseEvent.WHEEL_MOVED_UP:
                        i().mouseWheelMovedUp(mouseEvent)
                        
                    elif type == MouseEvent.WHEEL_MOVED_DOWN:
                        i().mouseWheelMovedDown(mouseEvent)

                    elif type == MouseEvent.CLICKED:
                        i().mouseClicked(mouseEvent)
                        
                    else:
                        raise GCN_EXCEPTION("Unknown mouse event type.")
                    
                if toSourceOnly == True:
                    break
                
            swap=widget
            widget=parent
            parent=swap.getParent()
            
            #If a non modal focused widget has been reached
            #and we have modal focus cancel the distribution.
            if self.mFocusHandler.getModalFocused() != None and widget.isModalFocused() == False:
                break

            #If a non modal mouse input focused widget has been reached
            #and we have modal mouse input  focus cancel the distribution.
            if self.mFocusHandler.getModalMouseInputFocused() != None and widget.isModalMouseInputFocused() == False:
                break
            
    def distributeKeyEvent(self,keyEvent):
        parent=keyEvent.getSource()
        widget=keyEvent.getSource()
        
        if self.mFocusHandler.getModalFocused() != None and widget.isModalFocused() == False:
            return None
        
        if self.mFocusHandler.getModalMouseInputFocused() != None and widget.isModalMouseInputFocused() == False:
            return None
        
        while parent != None:
            #If the widget has been removed due to input
            #cancel the distribution.
            if Widget.widgetExists(widget) == False:
                break
            
            parent=widget.getParent()
            type=keyEvent.getType()
            if widget.isEnabled() == True:
                keyListeners=widget.getKeyListeners()
                for i in keyListeners:
                    if type == KeyEvent.PRESSED:
                        i().keyPressed(keyEvent)
                    elif type == KeyEvent.RELEASED:
                        i().keyReleased(keyEvent)
                    else:
                        raise GCN_EXCEPTION("Unknown key event type.")
                    
            
            swap=widget
            widget=parent
            parent=swap.getParent()
            
            #If a non modal focused widget has been reached
            #and we have modal focus cancel the distribution.
            if self.mFocusHandler.getModalFocused() != None and widget.isModalFocused() == False:
                break
            
    def distributeKeyEventToGlobalListeners(self,keyEvent):
        type=keyEvent.getType()
        for i in self.mKeyListeners:
            if type == KeyEvent.PRESSED:
                i().keyPressed(keyEvent)
            elif type == KeyEvent.RELEASED:
                i().keyReleased(keyEvent)
            else:
                raise GCN_EXCEPTION("Unknown key event type.")
            
            if keyEvent.isConsumed() == True:
                break
            
    def handleModalFocus(self):
        #Check if modal focus has been gained by a widget.
        if ( self.mFocusHandler.getLastWidgetWithModalFocus() != self.mFocusHandler.getModalFocused() ) and ( self.mFocusHandler.getLastWidgetWithModalFocus() == None ):
            self.handleModalFocusGained()
            self.mFocusHandler.setLastWidgetWithModalFocus(self.mFocusHandler.getModalFocused())
            
        #Check if modal focus has been released
        elif ( self.mFocusHandler.getLastWidgetWithModalFocus() != self.mFocusHandler.getModalFocused() ) and ( self.mFocusHandler.getLastWidgetWithModalFocus() != None ):
            self.handleModalFocusReleased()
            self.mFocusHandler.setLastWidgetWithModalFocus(None)
            
    def handleModalMouseInputFocus(self):
        #Check if modal focus has been gained by a widget.
        if ( self.mFocusHandler.getLastWidgetWithModalMouseInputFocus() != self.mFocusHandler.getModalMouseInputFocused() ) and ( self.mFocusHandler.getLastWidgetWithModalMouseInputFocus() == None ):
            self.handleModalFocusGained()
            self.mFocusHandler.setLastWidgetWithModalMouseInputFocus(self.mFocusHandler.getModalMouseInputFocused())
            
        #Check if modal focus has been released
        elif ( self.mFocusHandler.getLastWidgetWithModalMouseInputFocus() != self.mFocusHandler.getModalMouseInputFocused() ) and ( self.mFocusHandler.getLastWidgetWithModalMouseInputFocus() != None ):
            self.handleModalFocusReleased()
            self.mFocusHandler.setLastWidgetWithModalMouseInputFocus(None)
            
    def handleModalFocusGained(self):
        # Distribute an event to all widgets in the "widget with mouse" queue.
        while len(self.mWidgetWithMouseQueue) > 0:
            widget=self.mWidgetWithMouseQueue[0]
            if Widget.widgetExists(widget) == True:
                self.distributeMouseEvent(widget,MouseEvent.EXITED,self.mLastMousePressButton,self.mLastMouseX,self.mLastMouseY,true,true)
                
            self.mWidgetWithMouseQueue.pop(0)
        
        self.mFocusHandler.setLastWidgetWithModalMouseInputFocus(self.mFocusHandler.getModalMouseInputFocused())

    def handleModalFocusReleased(self):
        #Check all widgets below the mouse to see if they are
        #present in the "widget with mouse" queue. If a widget
        #is not then it should be added and an entered event should
        #be sent to it.
        widget=self.getMouseEventSource(self.mLastMouseX,self.mLastMouseX)
        parent=widget
        
        while parent != None:
            parent=widget.getParent()
            
            #Check if the widget is present in the "widget with mouse" queue.
            widgetIsPresentInQueue = false
            for i in self.mWidgetWithMouseQueue:
                if i == widget:
                    widgetIsPresentInQueue = true
                    break
                
            #Widget is not present, send an entered event and add
            #it to the "widget with mouse" queue.
            if widgetIsPresentInQueue == False and Widget.widgetExists(widget) == True:
                self.distributeMouseEvent(widget,MouseEvent.ENTERED,self.mLastMousePressButton,self.mLastMouseX,self.mLastMouseY,False,True)
                self.mWidgetWithMouseQueue.insert(0,widget)
                
            swap = widget
            widget = parent
            parent = swap.getParent()
                




        

                    






            

            


            
            
        
        
    
            
            
            
            