#!/usr/bin/env python

from guichan import *
from graphics import Graphics
from font import Font
from widget import Widget
from image import Image

class Icon(Widget):
    def __init__(self,image=None):
        Widget.__init__(self)
        self.mImage=None
        self.mInternalImage=False
        if isinstance(image,Image) == True:
            self.mImage=image
            self.mInternalImage=False
            self.setSize(self.mImage.getWidth(),self.mImage.getHeight())
        elif type(image) == type("abc"):
            self.mImage=Image.load(image,True)
            self.mInternalImage=True
            self.setSize(self.mImage.getWidth(),self.mImage.getHeight())
        else:
            self.setSize(0,0)
            
    def __del__(self):
        if self.mInternalImage == True:
            del self.mImage
            
    def setImage(self,image):
        if self.mInternalImage == True:
            del self.mImage
            
        self.mImage=image
        self.mInternalImage=False
        self.setSize(self.mImage.getWidth(),self.mImage.getHeight())
        self.addDirtyRect()
        
    def getImage(self):
        return self.mImage
    
    def setAlpha(self,alpha):
        c=Color(self.getBaseColor())
        c.a=alpha
        self.setBaseColor(c)
        
    def getAlpha(self):
        return self.getBaseColor().a
    
    def draw(self,graphics):
        if self.mImage != None:
            oldAlpha=self.mImage.getAlpha()
            self.mImage.setAlpha(self.getAlpha())
            x=(self.getWidth()-self.mImage.getWidth())/2
            y=(self.getHeight()-self.mImage.getHeight())/2
            graphics.drawImage(self.mImage,x,y)
            self.mImage.setAlpha(oldAlpha)
        
        
