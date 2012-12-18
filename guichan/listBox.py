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
from selectionListener import SelectionListener
from selectionEvent import SelectionEvent
from listModel import ListModel

class ListBox(Widget,MouseListener,KeyListener):
    def __init__(self,listModel=None):
        Widget.__init__(self)
        self.mSelected=-1
        self.mSelectionListeners=[]
        self.mListModel=listModel
        self.mWrappingEnabled=False
        
        self.setWidth(100)
        self.setFocusable(True)
        
        self.addMouseListener(self)
        self.addKeyListener(self)
        
        self.adjustSize()
        
    def logic(self):
        self.adjustSize()
    
    def setSelected(self,selected):
        if self.mListModel == None:
            self.mSelected=-1
        else:
            if selected < 0:
                self.mSelected=-1
            elif selected >= self.mListModel.getNumberOfElements():
                self.mSelected=self.mListModel.getNumberOfElements()-1
            else:
                self.mSelected=selected
                
            scroll=Rectangle()
            
            if self.mSelected < 0:
                scroll.y=0
            else:
                scroll.y=self.getRowHeight()*self.mSelected
                
            scroll.height=self.getRowHeight()
            self.showPart(scroll)
            
        self.distributeValueChangedEvent()
        self.addDirtyRect()
        
    def getSelected(self):
        return self.mSelected
    
    def setWrappingEnabled(self,wrap):
        self.mWrappingEnabled=wrap
        
    def isWrappingEnabled(self):
        return self.mWrappingEnabled
    
    def getRowHeight(self):
        return self.getFont().getHeight()
    
    def setListModel(self,listModel):
        self.mSelected=-1
        self.mListModel=listModel
        self.adjustSize()
        
    def getListModel(self):
        return self.mListModel
    
    def addSelectionListener(self,widget):
        self.mSelectionListeners.append(widget)
        
    def removeSelectionListener(self,widget):
        if self.mSelectionListeners.count(widget) > 0:
            self.mSelectionListeners.remove(widget)
            
    def distributeValueChangedEvent(self):
        for i in self.mSelectionListeners:
            event=SelectionEvent(self)
            i.valueChanged(event)
            
    def adjustSize(self):
        if self.mListModel != None:
            self.setHeight(self.getRowHeight()*self.mListModel.getNumberOfElements())
            self.addDirtyRect()
            
    def draw(self,graphics):
        graphics.setColor( self.getBackgroundColor() )
        graphics.fillRectangle( Rectangle(0,0,self.getWidth(),self.getHeight()) )
        
        if self.mListModel == None:
            return None
        
        graphics.setColor( self.getForegroundColor() )
        graphics.setFont( self.getFont() )
        
        #Check the current clip area so we don't draw unnecessary items
        #that are not visible.
        
        currentClipArea = ClipRectangle( graphics.getCurrentClipArea() )
        rowHeight = self.getRowHeight()
        
        #Calculate the number of rows to draw by checking the clip area.
        #The addition of two makes covers a partial visible row at the top
        # and a partial visible row at the bottom.
        numberOfRows=(currentClipArea.height/rowHeight)+2
        if numberOfRows > self.mListModel.getNumberOfElements():
            numberOfRows=self.mListModel.getNumberOfElements()
            
        #Calculate which row to start drawing. If the list box 
        #has a negative y coordinate value we should check if
        #we should drop rows in the begining of the list as
        #they might not be visible. A negative y value is very
        #common if the list box for instance resides in a scroll
        #area and the user has scrolled the list box downwards.
        startRow=0
        if self.getY() < 0:
            startRow = -1 * (self.getY()/rowHeight)
        else:
            startRow=0
        
        #numberOfRows=numberOfRows-startRow
        endRow=startRow+numberOfRows
        if startRow > 0:
            startRow=startRow-1
            endRow=startRow+numberOfRows-1
        #if endRow > self.mListModel.getNumberOfElements(): endRow=self.mListModel.getNumberOfElements()
        y=rowHeight*startRow
        for i in range(startRow,endRow):
            if i == self.mSelected:
                graphics.setColor( self.getSelectionColor() )
                graphics.fillRectangle( Rectangle(0,y,self.getWidth(),rowHeight) )
                graphics.setColor( self.getForegroundColor() )
            
            #If the row height is greater than the font height we
            #draw the text with a center vertical alignment.
            if rowHeight > self.getFont().getHeight():
                graphics.drawText(self.mListModel.getElementAt(i), 1, y + (rowHeight / 2) - (self.getFont().getHeight() / 2), self.getTextColor() )
            else:
                graphics.drawText(self.mListModel.getElementAt(i), 1, y, self.getTextColor())
            
            y+=rowHeight
        
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        
        if key.getValue() == Key.ENTER or key.getValue() == Key.SPACE:
            self.distributeActionEvent()
            keyEvent.consume()
        
        elif key.getValue() == Key.UP:
            self.setSelected( self.mSelected-1 )
            if self.mSelected == -1:
                if self.mWrappingEnabled == True:
                    self.setSelected( self.mListModel.getNumberOfElements()-1 )
                else:
                    self.setSelected(0)
            
            keyEvent.consume()
            
        elif key.getValue() == Key.DOWN:
            if self.mWrappingEnabled == True and self.getSelected() == self.mListModel.getNumberOfElements()-1:
                self.setSelected( 0 )
            else:
                self.setSelected( self.getSelected()+1 )
            
            keyEvent.consume()
            
        elif key.getValue() == Key.HOME:
            self.setSelected( 0 )
            keyEvent.consume()
            
        elif key.getValue() == Key.END:
            self.setSelected( self.mListModel.getNumberOfElements()-1 )
            keyEvent.consume()
            
    def mousePressed(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT:
            self.setSelected( mouseEvent.getY()/self.getRowHeight() )
            self.distributeActionEvent()
            
    def mouseWheelMovedUp(self,mouseEvent):
        if self.isFocused() == True:
            if self.getSelected () > 0:
                self.setSelected( self.getSelected()-1 )
            
            mouseEvent.consume()
            
    def mouseWheelMovedDown(self,mouseEvent):
        if self.isFocused() == True:
            self.setSelected( self.getSelected()+1 )
            mouseEvent.consume()
            
    def mouseDragged(self,mouseEvent):
        mouseEvent.consume()
        
            
            






        