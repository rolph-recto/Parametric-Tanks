#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from actionListener import ActionListener
from keyListener import KeyListener
from keyEvent import KeyEvent
from key import Key
from mouseListener import MouseListener
from mouseEvent import MouseEvent
from mouseInput import MouseInput
from focusListener import FocusListener
from widget import Widget
from basicContainer import BasicContainer
from container import Container
from label import Label
from tab import Tab

class TabbedArea(BasicContainer,MouseListener,KeyListener,ActionListener,FocusListener):
    def __init__(self):
        BasicContainer.__init__(self)
        self.mSelectedTab=None
        self.mTabs=[]
        self.setFocusable(True)
        self.addKeyListener(self)
        self.addMouseListener(self)
        self.addFocusListener(self)
        
        self.mTabContainer=Container()
        self.mTabContainer.setOpaque(False)
        self.mWidgetContainer=Container()
        
        self.add(self.mTabContainer)
        self.add(self.mWidgetContainer)
        
    def __del__(self):
        self.remove(self.mTabContainer)
        self.remove(self.mWidgetContainer)
        self.mTabs=None
        self.mSelectedTab=None
        
    def addTab(self,t,widget):
        if type(t) == type("abc"):
            tab=Tab()
            tab.setCaption(t)
            self.addTab(tab,widget)
        elif isinstance(t,Tab) == True:
            t.setTabbedArea(self)
            t.addActionListener(self)
            
            self.mTabContainer.add(t)
            self.mTabs.append( (t,widget) )
            
            if self.mSelectedTab == None:
                self.setSelectedTab(t)
                
            self.adjustTabPositions()
            self.adjustSize()
            
    def removeTab(self,tab):
        if type(tab) == type(0):
            if tab >= len(self.mTabs) or tab < 0:
                raise GCN_EXCEPTION("No such tab index.")
            
            self.removeTab(self.mTabs[tab][0])
            
        else:
            tabIndexToBeSelected=-1
            
            if tab == self.mSelectedTab:
                index=self.getSelectedTabIndex()
                
                if index == len(self.mTabs)-1 and len(self.mTabs) >= 2:
                    tabIndexToBeSelected=index
                    index-=1
                
                elif index == len(self.mTabs)-1 and len(self.mTabs) == 1:
                    tabIndexToBeSelected=-1
                    
                else:
                    tabIndexToBeSelected=index
                    
            
            for i in self.mTabs[:]:
                if i[0] == tab:
                    self.mTabContainer.remove(tab)
                    self.mTabs.remove(i)
                    break
                
            if tabIndexToBeSelected == -1:
                self.mSelectedTab=None
                self.mWidgetContainer.clear()
                
            else:
                self.setSelectedTab(tabIndexToBeSelected)
                
            self.adjustSize()
            self.adjustTabPositions()
            
    def isTabSelected(self,tab):
        if type(tab) == type(0):
            if tab >= len(self.mTabs) or tab < 0:
                raise GCN_EXCEPTION("No such tab index.")
            
            return self.mSelectedTab == self.mTabs[tab][0]
        
        else:
            return self.mSelectedTab == tab
        
    def setSelectedTab(self,tab):
        if type(tab) == type(0):
            if tab >= len(self.mTabs) or tab < 0:
                raise GCN_EXCEPTION("No such tab index.")
            
            self.setTabSelected(self.mTabs[tab][0])
            
        else:
            for i in self.mTabs:
                if i[0] == self.mSelectedTab:
                    if isinstance(i[1],Widget):
                        self.mWidgetContainer.remove(i[1])
                    else:
                        for j in i[1]:
                            self.mWidgetContainer.remove(j[0])
                    
            for i in self.mTabs:
                if i[0] == tab:
                    self.mSelectedTab=tab
                    if isinstance(i[1],Widget):
                        self.mWidgetContainer.add(i[1])
                        if isinstance(i[1],BasicContainer):
                            i[1].setSize( self.mWidgetContainer.getWidth(), self.mWidgetContainer.getHeight())
                    else:
                        #widgets is a list of widgets ex. [ (ListBox,0,0), (Button,10,20) ]
                        for j in i[1]:
                            self.mWidgetContainer.add(j[0],j[1],j[2])
                            
            self.addDirtyRect()
                    
    def getSelectedTabIndex(self):
        for i in range(len(self.mTabs)):
            if self.mTabs[i][0] == self.mSelectedTab:
                return i
            
        return -1
    
    def getSelectedTab(self):
        return self.mSelectedTab
    
    def draw(self,graphics):
        faceColor=self.getBaseColor()
        alpha=faceColor.a
        highlightColor=faceColor+0x303030
        highlightColor.a=alpha
        shadowColor=faceColor-0x303030
        shadowColor.a=alpha
        
        #Draw a border.
        graphics.setColor(highlightColor)
        graphics.drawLine(0, self.mTabContainer.getHeight(), 0, self.getHeight()-2)
        graphics.setColor(shadowColor)
        graphics.drawLine(self.getWidth()-1, self.mTabContainer.getHeight()+1, self.getWidth()-1, self.getHeight()-1)
        graphics.drawLine(1, self.getHeight()-1, self.getWidth()-1, self.getHeight()-1)
        graphics.setColor(self.getBaseColor())
        graphics.fillRectangle( Rectangle(1,1,self.getWidth()-2,self.getHeight()-2) )
        
        #Draw a line underneath the tabs.
        graphics.setColor(highlightColor)
        graphics.drawLine(1, self.mTabContainer.getHeight(), self.getWidth()-1, self.mTabContainer.getHeight())
        
        #If a tab is selected, remove the line right underneath
        #the selected tab.
        if self.mSelectedTab != None:
            graphics.setColor( self.getBaseColor() )
            graphics.drawLine(self.mSelectedTab.getX()+1, self.mTabContainer.getHeight(), self.mSelectedTab.getX()+self.mSelectedTab.getWidth()-2, self.mTabContainer.getHeight())
           
        self.drawChildren(graphics)
        
    def logic(self):
        BasicContainer.logic(self)
    
    def adjustSize(self):
        maxTabHeight=0
        for i in self.mTabs:
            if i[0].getHeight() > maxTabHeight:
                maxTabHeight=i[0].getHeight()
        
        self.mTabContainer.setSize(self.getWidth()-2, maxTabHeight)
        self.mWidgetContainer.setPosition(1, maxTabHeight+1)
        self.mWidgetContainer.setSize(self.getWidth()-2, self.getHeight()-maxTabHeight-2)
        self.addDirtyRect()
        
    def adjustTabPositions(self):
        maxTabHeight=0
        for i in self.mTabs:
            if i[0].getHeight() > maxTabHeight:
                maxTabHeight=i[0].getHeight()
                
        x=0
        for i in self.mTabs:
            tab=i[0]
            tab.setPosition(x, maxTabHeight-tab.getHeight())
            x+=tab.getWidth()
            
        self.addDirtyRect()
            
    def setWidth(self,width):
        self.mDimension.width=width
        self.adjustSize()
        
    def setHeight(self,height):
        self.mDimension.height=height
        self.adjustSize()
        
    def setSize(self,width,height):
        self.mDimension.width=width
        self.mDimension.height=height
        self.adjustSize()
    
    def setDimension(self,dimension):
        self.mDimension.x=dimension.x
        self.mDimension.y=dimension.y
        TabbedArea.setSize(self,dimension.width,dimension.height)
        self.addDirtyRect()
        
    def keyPressed(self,keyEvent):
        if keyEvent.isConsumed() == True or self.isFocused() == False:
            return None
        
        elif keyEvent.getKey().getValue() == Key.LEFT:
            index=self.getSelectedTabIndex()
            
            index-=1
            if index < 0:
                return None
            
            else:
                self.setSelectedTab(self.mTabs[index][0])
                
            keyEvent.consume()
            
        elif keyEvent.getKey().getValue() == Key.RIGHT:
            index=self.getSelectedTabIndex()
            
            index+=1
            if index >= len(self.mTabs):
                return None
            
            else:
                self.setSelectedTab(self.mTabs[index][0])
                
            keyEvent.consume()
            
    def mousePressed(self,mouseEvent):
        if mouseEvent.isConsumed() == True and mouseEvent.getSource().isFocusable() == True:
            return None
        
        if mouseEvent.getButton() == MouseEvent.LEFT:
            tab=self.mTabContainer.getWidgetAt(mouseEvent.getX(),mouseEvent.getY())
            if isinstance(tab,Tab):
                self.setSelectedTab(tab)

        """DO NOT UNCOMMENT THE FOLLOWING LINE
        IT WILL MAKE WIDGETS IN TABS UNRESPONSIVE
        TO KEY EVENTS, EVEN IF THEY ARE FOCUSED"""
        #self.requestFocus()
        
    def death(self,event):
        tab=event.getSource()
        if isinstance(tab,Tab):
            self.removeTab(tab)
        else:
            BasicContainer.death(self,event)
            
    def action(self,actionEvent):
        tab=actionEvent.getSource()
        if isinstance(tab,Tab):
            self.setSelectedTab(tab)
        else:
            raise GCN_EXCEPTION("Received an action from a widget that's not a tab!")
        
    def focusGained(self,event):
        self.addDirtyRect()
        
    def focusLost(self,event):
        self.addDirtyRect()
        
 