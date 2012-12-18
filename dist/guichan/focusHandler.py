#!/usr/bin/env python

from guichan import *
from event import Event

class FocusHandler:
    def __init__(self):
        self.mWidgets=[]
        self.mModalFocusedWidget=None
        self.mModalMouseInputFocusedWidget=None
        self.mDraggedWidget=None
        self.mLastWidgetWithMouse=None
        self.mLastWidgetWithModalFocus=None
        self.mLastWidgetWithModalMouseInputFocus=None
        self.mLastWidgetPressed=None
        self.mFocusedWidget=None
    
    def requestFocus(self,widget):
        if widget == None or widget == self.mFocusedWidget:
            return None
        toBeFocusedIndex=-1
        for i in range(len(self.mWidgets)):
            if self.mWidgets[i] == widget:
                toBeFocusedIndex=i
                
        if toBeFocusedIndex < 0:
            raise GCN_EXCEPTION("Trying to focus a none existing widget.")
        
        oldFocused=self.mFocusedWidget
        if oldFocused != widget:
            self.mFocusedWidget=self.mWidgets[toBeFocusedIndex]
            if oldFocused != None:
                focusEvent=Event(oldFocused)
                self.distributeFocusGainedEvent(focusEvent)
                
    def requestModalFocus(self,widget):
        if self.mModalFocusedWidget != None and self.mModalFocusedWidget != widget:
            raise GCN_EXCEPTION("Another widget has modal focus.")
        
        self.mModalFocusedWidget=widget
        if self.mFocusedWidget != None and (not self.mFocusedWidget.isModalFocused()):
            self.focusNone()
            
    def requestModalMouseInputFocus(self,widget):
        if self.mModalMouseInputFocusedWidget != None and self.mModalMouseInputFocusedWidget != widget:
            raise GCN_EXCEPTION("Another widget already has modal mouse input focus.")
        
        self.mModalMouseInputFocusedWidget=widget
        
    def releaseModalFocus(self,widget):
        if self.mModalFocusedWidget == widget:
            self.mModalFocusedWidget = None
            
    def releaseModalMouseInputFocus(self,widget):
        if self.mModalMouseInputFocusedWidget == widget:
            self.mModalMouseInputFocusedWidget = None
            
    def getFocused(self):
        return self.mFocusedWidget

    def getModalFocused(self):
        return self.mModalFocusedWidget
    
    def getModalMouseInputFocused(self):
        return self.mModalMouseInputFocusedWidget
    
    def iterateFocus(self,direction):
        focusedWidget=-1
        for i in range(len(self.mWidgets)):
            if self.mWidgets[i] == self.mFocusedWidget:
                focusedWidget=i
                
        focused=focusedWidget
        i=len(self.mWidgets)
        while True:
            focusedWidget+=direction
            if i==0:
                focusedWidget=-1
                break
            
            i-=1
            if focusedWidget >= len(self.mWidgets):
                focusedWidget=0
            elif focusedWidget <= 0:
                focusedWidget=len(self.mWidgets)-1
            if focusedWidget == focused:
                return None
            
            if not (not self.mWidgets[focusedWidget].isFocusable()):
                break
            
        if focusedWidget >= 0:
            self.mFocusedWidget=self.mWidgets[focusedWidget]
            focusEvent=Event(self.mFocusedWidget)
            self.distributeFocusGainedEvent(focusEvent)
        
        if focused >= 0:
            focusEvent2=Event(self.mWidgets[focused])
            self.distributeFocusLostEvent(focusEvent2)
            
    def focusNext(self):
        #iterate focus forward (positive int)
        self.iterateFocus(1)
        
    def focusPrevious(self):
        #iterate focus backward (negative int)
        self.iterateFocus(-1)
        
    def isFocused(self,widget):
        return self.mFocusedWidget == widget
    
    def add(self,widget):
        self.mWidgets.append(widget)
        
    def remove(self,widget):
        if self.mWidgets.count(widget) > 0:
            self.mWidgets.remove(widget)
            
            if self.mDraggedWidget == widget:
                self.mDraggedWidget=None
                
            if self.mLastWidgetWithMouse == widget:
                self.mLastWidgetWithMouse=None
                
            if self.mLastWidgetWithModalFocus == widget:
                self.mLastWidgetWithModalFocus=None
                
            if self.mLastWidgetWithModalMouseInputFocus == widget:
                self.mLastWidgetWithModalMouseInputFocus=None
            
            if self.mLastWidgetPressed == widget:
                self.mLastWidgetPressed=None
                
    def focusNone(self):
        if self.mFocusedWidget != None:
            focused=self.mFocusedWidget
            self.mFocusedWidget=None
            
            focusEvent=Event(focused)
            self.distributeFocusLostEvent(focusEvent)
            
            
    def iterateTab(self,direction):
        if self.mFocusedWidget != None:
            if not self.mFocusedWidget.isTabOutEnabled():
                return None
            
        if len(self.mWidgets) == 0:
            self.mFocusedWidget=None
            return None
        
        focusedWidget=-1
        for i in range(len(self.mWidgets)):
            if self.mWidgets[i] == self.mFocusedWidget:
                focusedWidget=i
                
        focused=focusedWidget
        i=len(self.mWidgets)
        done=False
        while True:
            focusedWidget+=direction
            if i==0:
                focusedWidget=-1
                break
            
            i-=1
            if focusedWidget >= len(self.mWidgets):
                focusedWidget=0
            if focusedWidget <= 0:
                focusedWidget=len(self.mWidgets)-1
            if focusedWidget == focused:
                return None
            
            if self.mWidgets[focusedWidget].isFocusable() and self.mWidgets[focusedWidget].isTabInEnabled() and (self.mModalFocusedWidget == None or self.mWidgets[focusedWidget].isModalFocused() == True):
                done=True
            
            if not (done==True):
                break
            
        if focusedWidget >= 0:
            self.mFocusedWidget=self.mWidgets[focusedWidget]
            focusEvent=Event(self.mFocusedWidget)
            self.distributeFocusGainedEvent(focusEvent)
        
        if focused >= 0:
            focusEvent2=Event(self.mWidgets[focused])
            self.distributeFocusLostEvent(focusEvent2)
            
    def tabNext(self):
        self.iterateTab(self,1)
        
    def tabPrevious(self):
        self.iterateTab(self,-1)
        
    def distributeFocusLostEvent(self,event):
        sourceWidget=event.getSource()
        focusListeners=sourceWidget.getFocusListeners()
        for i in focusListeners:
            i().focusLost(event)
            
    def distributeFocusGainedEvent(self,event):
        sourceWidget=event.getSource()
        focusListeners=sourceWidget.getFocusListeners()
        for i in focusListeners:
            i().focusGained(event)

    def setDraggedWidget(self,widget):
        if widget != None:
            self.mDraggedWidget=weakref.ref(widget)
        else:
            self.mDraggedWidget=None
    
    def setLastWidgetWithMouse(self,widget):
        if widget != None:
            self.mLastWidgetWithMouse=weakref.ref(widget)
        else:
            self.mLastWidgetWithMouse=None
        
    
    def setLastWidgetWithModalFocus(self,widget):
        if widget != None:
            self.mLastWidgetWithModalFocus=weakref.ref(widget)
        else:
            self.mLastWidgetWithModalFocus=None
    
    def setLastWidgetWithModalMouseInputFocus(self,widget):
        if widget != None:
            self.mLastWidgetWithModalMouseInputFocus=weakref.ref(widget)
        else:
            self.mLastWidgetWithModalMouseInputFocus=None
    
    def setLastWidgetPressed(self,widget):
        if widget != None:
            self.mLastWidgetPressed=weakref.ref(widget)
        else:
            self.mLastWidgetPressed=None
            
    def getDraggedWidget(self):
        if self.mDraggedWidget != None:
            widget=self.mDraggedWidget()
            return widget
    
    def getLastWidgetWithMouse(self):
        if self.mLastWidgetWithMouse != None:
            widget=self.mLastWidgetWithMouse()
            return widget
    
    def getLastWidgetWithModalFocus(self):
        if self.mLastWidgetWithModalFocus != None:
            widget=self.mLastWidgetWithModalFocus()
            return widget
    
    def getLastWidgetWithModalMouseInputFocus(self):
        if self.mLastWidgetWithModalMouseInputFocus != None:
            widget=self.mLastWidgetWithModalMouseInputFocus()
            return widget
    
    def getLastWidgetPressed(self):
        if self.mLastWidgetPressed != None:
            widget=self.mLastWidgetPressed()
            return widget
    
    
    
        
        
        
        
            
        
            
            
            
