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

class TextBox(Widget,MouseListener,KeyListener):
    def __init__(self,text=""):
        Widget.__init__(self)
        self.mTextRows=[]
        self.mCaretColumn=0
        self.mCaretRow=0
        self.mEditable=True
        self.mOpaque=True
        self.mInsert=False
        self.mTabSize=4
        
        self.setFocusable(True)
        self.setTabOutEnabled(False)
        
        self.addMouseListener(self)
        self.addKeyListener(self)
        self.setText(text)
        self.adjustSize()
        
    def setText(self,text):
        self.mCaretColumn=0
        self.mCaretRow=0
        
        del self.mTextRows[:]
        
        pos, lastPos, length=0, 0, 0
        while True:
            part=text.partition("\n")
            
            self.mTextRows.append(part[0])
            if part[1]+part[2] != "":
                text=part[2]
            else:
                break
            
        self.adjustSize()
        self.addDirtyRect()
    
    def setTextRow(self,row,text):
        self.mTextRows[row]=text
        if self.mCaretRow == row:
            self.setCaretColumn(self.mCaretColumn)
            
        self.adjustSize()
        self.addDirtyRect()
        
    def addRow(self,row):
        self.mTextRows.append(row)
        self.adjustSize()
        self.addDirtyRect()
        
    def setEditable(self,editable):
        self.mEditable=editable
        self.addDirtyRect()
        
    def setOpaque(self,opaque):
        self.mOpaque=opaque
        self.addDirtyRect()
    
    def setCaretRow(self,row):
        self.mCaretRow=row
        
        if self.mCaretRow >= len(self.mTextRows):
            self.mCaretRow=len(self.mTextRows)-1
            
        if self.mCaretRow < 0:
            self.mCaretRow=0

        self.setCaretColumn(self.mCaretColumn)
        
    
    def setCaretColumn(self,column):
        self.mCaretColumn=column
        
        if self.mCaretColumn > len(self.mTextRows[self.mCaretRow]):
            self.mCaretColumn=len(self.mTextRows[self.mCaretRow])
            
        if self.mCaretColumn < 0:
            self.mCaretColumn=0
            
        self.addDirtyRect()

    def setCaretRowColumn(self,row,column):
        self.setCaretRow(row)
        self.setCaretColumn(column)
        
    def setCaretPosition(self,pos):
        for row in range( len(self.mTextRows) ):
            if pos <= len(self.mTextRows[row]):
                self.mCaretRow=row
                self.mCaretColumn=position
                return None
            
            else:
                pos-=1
            
        #Position beyond end of text
        self.mCaretRow=len(self.mTextRows)-1
        self.mCaretColumn=len(self.mTextRows[self.mCaretRow])
        self.addDirtyRect()
        
    def setInsert(self,insert):
        self.mInsert=insert
        self.addDirtyRect()
        
    def toggleInsert(self):
        if self.mInsert == False:
            self.setInsert(True)
        else:
            self.setInsert(False)
            
    def setTabSize(self,size):
        self.mTabSize=size
        
    def getTabSize(self):
        return self.mTabSize
        
    def isInsert(self):
        return self.mInsert
    
    def getTextRow(self,row):
        return self.mTextRows[row]
    
    def getText(self):
        if len(self.mTextRows) == 0:
            return ""
        
        text=""
        for i in range(len(self.mTextRows)-1):
            text+=self.mTextRows[i]+"\n"
            
        text+=self.mTextRows[i]
        
        return text
    
    def isEditable(self):
        return self.mEditable
        
    def isOpaque(self):
        return self.mOpaque
    
    def getCaretRow(self):
        return self.mCaretRow
    
    def getCaretColumn(self):
        return self.mCaretColumn
    
    def getCaretPosition(self):
        pos=0
        for row in range(self.mCaretRow):
            pos+=len(self.mTextRows[row])
            
        return pos+self.mCaretColumn
    
    def fontChanged(self):
        Widget.fontChanged(self)
        self.adjustSize()
        
    def scrollToCaret(self):
        scroll=Rectangle()
        scroll.x=self.getFont().getWidth(self.mTextRows[self.mCaretRow][0:self.mCaretColumn])
        scroll.y=self.getFont().getHeight()*self.mCaretRow
        scroll.width=self.getFont().getWidth(" ")
        scroll.height=self.getFont().getHeight()+2 #add 2 for some extra space
        
        self.showPart(scroll)
        self.addDirtyRect()
        
    def adjustSize(self):
        width=0
        for i in range(len(self.mTextRows)):
            w=self.getFont().getWidth(self.mTextRows[i])
            if width < w:
                width=w
                
        self.setWidth(width+1)
        self.setHeight( self.getFont().getHeight() * (len(self.mTextRows)) )
        self.addDirtyRect()
        
    def draw(self,graphics):
        width=self.getWidth()+self.getFrameSize()*2-1
        height=self.getHeight()+self.getFrameSize()*2-1
        
        graphics.setColor(self.getBackgroundColor())
        
        for i in range(self.getFrameSize()):
            graphics.drawLine(i, i, width-i, i)
            graphics.drawLine(i, i+1, i, height-i-1)
            graphics.drawLine(width-i, i+1, width-i, height-i)
            graphics.drawLine(i, height-i, width-i-1, height-i)
            
        if self.mOpaque == True:
            graphics.setColor(self.getBackgroundColor())
            graphics.fillRectangle( Rectangle(0,0,self.getWidth(),self.getHeight()) )
            
        if self.isFocused() == True and self.isEditable() == True:
            self.drawCaret(graphics, self.getFont().getWidth(self.mTextRows[self.mCaretRow][0:self.mCaretColumn]), self.mCaretRow*self.getFont().getHeight())
            
        graphics.setColor(self.getForegroundColor())
        graphics.setFont(self.getFont())
        
        for i in range(len(self.mTextRows)):
            #Move the text one pixel so we can have a caret before a letter.
            graphics.drawText(self.mTextRows[i], 1, i*self.getFont().getHeight(), self.getTextColor())
            
    def drawCaret(self,graphics,x,y):
        graphics.setColor(self.getForegroundColor())
        if self.mInsert == False:
            graphics.drawLine(x, y, x, self.getFont().getHeight()+y)
        else:
            graphics.drawLine(x, y, x,self.getFont().getHeight()/2+y)
            graphics.drawLine(x, self.getFont().getHeight()/2+y+2, x,self.getFont().getHeight()+y)
            
        
    def mousePressed(self,mouseEvent):
        if mouseEvent.getButton() == MouseEvent.LEFT:
            self.mCaretRow=mouseEvent.getY()/self.getFont().getHeight()
            if self.mCaretRow >= len(self.mTextRows):
                self.mCaretRow=len(self.mTextRows)-1
                
            self.mCaretColumn=self.getFont().getStringIndexAt(self.mTextRows[self.mCaretRow], mouseEvent.getX())
            self.addDirtyRect()
            
    def mouseDragged(self,mouseEvent):
        mouseEvent.consume()
        
    def keyPressed(self,keyEvent):
        key=keyEvent.getKey()
        
        if key.getValue() == Key.LEFT:
            self.mCaretColumn-=1
            if self.mCaretColumn < 0:
                self.mCaretRow-=1
                if self.mCaretRow < 0:
                    self.mCaretRow=0
                    self.mCaretColumn=0
                    
                else:
                    self.mCaretColumn=len(self.mTextRows[self.mCaretRow])
                    
        elif key.getValue() == Key.RIGHT:
            self.mCaretColumn+=1
            if self.mCaretColumn > len(self.mTextRows[self.mCaretRow]):
                self.mCaretRow+=1
                if self.mCaretRow >= len(self.mTextRows):
                    self.mCaretRow=len(self.mTextRows)-1
                    if self.mCaretRow < 0:
                        self.mCaretRow=0
                        
                    self.mCaretColumn=len(self.mTextRows[self.mCaretRow])
                    
                else:
                    self.mCaretColumn=0
                    
        elif key.getValue() == Key.DOWN:
            self.setCaretRow( self.getCaretRow()+1 )
            
        elif key.getValue() == Key.UP:
            self.setCaretRow( self.getCaretRow()-1 )
            
        elif key.getValue() == Key.HOME:
            self.mCaretColumn=0
            
        elif key.getValue() == Key.END:
            self.mCaretColumn=len(self.mTextRows[self.mCaretRow])
            
        elif key.getValue() == Key.ENTER and self.mEditable == True:
            if self.mCaretRow < len(self.mTextRows)-1:
                self.mTextRows.insert(self.mCaretRow+1, self.mTextRows[self.mCaretRow][self.mCaretColumn:])
            else:
                self.mTextRows.append(self.mTextRows[self.mCaretRow][self.mCaretColumn:])
            tr=self.mTextRows[self.mCaretRow][:self.mCaretColumn]
            self.mTextRows[self.mCaretRow]=tr
            self.mCaretRow+=1
            self.mCaretColumn=0
            self.adjustSize()

        elif key.getValue() == Key.BACKSPACE and self.mCaretColumn != 0 and self.mEditable == True:
            self.mTextRows[self.mCaretRow]=self.mTextRows[self.mCaretRow][:self.mCaretColumn-1]+self.mTextRows[self.mCaretRow][self.mCaretColumn:]
            self.setCaretColumn(self.getCaretColumn()-1)
            
        elif key.getValue() == Key.BACKSPACE and self.mCaretColumn == 0 and self.mCaretRow != 0 and self.mEditable == True:
            self.mCaretColumn=len(self.mTextRows[self.mCaretRow-1])
            self.mTextRows[self.mCaretRow-1]+=self.mTextRows[self.mCaretRow]
            del self.mTextRows[self.mCaretRow]
            self.mCaretRow-=1
            
        elif key.getValue() == Key.DELETE and self.mCaretColumn < len(self.mTextRows[self.mCaretRow]) and self.mEditable:
            self.mTextRows[self.mCaretRow]=self.mTextRows[self.mCaretRow][:self.mCaretColumn]+self.mTextRows[self.mCaretRow][self.mCaretColumn+1:]

        elif key.getValue() == Key.DELETE and self.mCaretColumn == len(self.mTextRows[self.mCaretRow]) and self.mCaretRow < len(self.mTextRows)-1 and self.mEditable:
            self.mTextRows[self.mCaretRow]+=self.mTextRows[self.mCaretRow+1]
            del self.mTextRows[self.mCaretRow+1]
            
        elif key.getValue() == Key.PAGE_UP:
            par=self.getParent()
            if par != None:
                rowsPerPage=par.getChildrenArea().height/self.getFont().getHeight()
                self.mCaretRow-=rowsPerPage
                if self.mCaretRow < 0:
                    self.mCaretRow=0
                    
        elif key.getValue() == Key.PAGE_DOWN:
            par=self.getParent()
            if par != None:
                rowsPerPage=par.getChildrenArea().height/self.getFont().getHeight()
                self.mCaretRow+=rowsPerPage
                if self.mCaretRow >= len(self.mTextRows):
                    self.mCaretRow=len(self.mTextRows)-1
                    
        elif key.getValue() == Key.TAB:
            tr=self.mTextRows[self.mCaretRow][:self.mCaretColumn]+(" "*self.mTabSize)+self.mTextRows[self.mCaretRow][self.mCaretColumn:]
            self.mTextRows[self.mCaretRow]=tr    
            self.mCaretColumn+=self.mTabSize
            
        elif key.getValue() == Key.INSERT:
            self.toggleInsert()
            
        elif key.isCharacter() == True and self.mEditable == True:
            if self.mInsert == False:
                tr=self.mTextRows[self.mCaretRow][:self.mCaretColumn]+chr(key.getValue())+self.mTextRows[self.mCaretRow][self.mCaretColumn:]
            else:
                tr=self.mTextRows[self.mCaretRow][:self.mCaretColumn]+chr(key.getValue())+self.mTextRows[self.mCaretRow][self.mCaretColumn+1:]
            
            self.mTextRows[self.mCaretRow]=tr    
            self.mCaretColumn+=1
            
        self.addDirtyRect()
        self.adjustSize()
        self.scrollToCaret()
                    


        
        

        
        