#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from widget import Widget

class ProgressBar(Widget):
     class Orientation:
          HORIZONTAL=0
          VERTICAL=1
     
     def __init__(self, max=0.0, value=0.0):
          Widget.__init__(self)
          
          self.mMax=max
          self.mValue=value
          self.mOrientation=ProgressBar.Orientation.HORIZONTAL
          
     def setMax(self, max=0.0):
          if max >= 0.0:
               self.mMax=max
               self.addDirtyRect()
               
     def setValue(self, value=0.0):
          if value >= 0.0 and value <= self.mMax:
               self.mValue=value
               self.addDirtyRect()
               
     def getMax(self):
          return self.mMax
     
     def getValue(self):
          return self.mValue
               
     def draw(self, graphics):
          graphics.setColor(self.mBaseColor)
          graphics.fillRectangle( Rectangle(0,0,self.getWidth(),self.getHeight()) )
          
          graphics.setColor(self.mForegroundColor)
          width, height=self.getWidth(), self.getHeight()
          if self.mOrientation == ProgressBar.Orientation.HORIZONTAL:
               width=int( (float(self.mValue)/float(self.mMax))*float(self.getWidth()) )
          if self.mOrientation == ProgressBar.Orientation.VERTICAL:
               height=int( (float(self.mValue)/float(self.mMax))*float(self.getHeight()) )
               
          graphics.fillRectangle( Rectangle(0,0,width,height) )
               
     
          
