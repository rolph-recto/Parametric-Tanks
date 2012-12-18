#!/usr/bin/env python

import pygame

from guichan import *
from font import Font
from pygameGraphics import *

class PygameFont(Font):
    def __init__(self,file="",size=0,color=Color(0,0,0,255)):
        self.mGlyphSpacing=0
        self.mRowSpacing=0
        self.mAntiAlias=True
        self.mFilename=""
        self.mColor=color
        self.mAlpha=color.a
        
        self.mFont=pygame.font.Font(file,size)
        self.mFilename=file
        
        if self.mFont == None:
            raise GCN_EXCEPTION("Cannot load font file: "+self.mFilename)
    
    def setAntiAlias(self,antiAlias):
        self.mAntiAlias=antiAlias
    
    def setRowSpacing(self,rowSpacing):
        self.mRowSpacing=rowSpacing
        
    def setGlyphSpacing(self,glyphSpacing):
        self.mGlyphSpacing=glyphSpacing
        
    def setColor(self,color):
        self.mColor=color
        
    def setAlpha(self,alpha):
        self.mAlpha=alpha
        
    def isAntiAlias(self):
        return self.mAntiAlias
        
    def getRowSpacing(self):
        return self.mRowSpacing
    
    def getGlyphSpacing(self):
        return self.mGlyphSpacing
        
    def getWidth(self,text):
        return self.mFont.size(text)[0]
    
    def getHeight(self):
        return self.mFont.get_height()
    
    def getColor(self):
        return self.mColor
    
    def getAlpha(self):
        return self.mAlpha
    
    def drawText(self,graphics,text,x,y,color=None):
        if text == "":
            return None
        
        if isinstance(graphics,PygameGraphics) == False:
            raise GCN_EXCEPTION("Graphics object is not PygameGraphics.")
        
        yOffset=self.getRowSpacing()/2
        tcolor=color if isinstance(color,Color) else self.mColor
        
        textSurface=self.mFont.render(text,True,GuichanToPygameColor(tcolor))
        
        src, dst=Rectangle(), Rectangle()
        currentClipArea=ClipRectangle(graphics.getCurrentClipArea())
        dst.x=x
        dst.y=y
        dst.w=0
        dst.h=0
        src.w=textSurface.get_width()
        src.h=textSurface.get_height()
        src.x=0
        src.y=0
        
        textSurface.set_alpha(self.mAlpha)

        graphics.drawSurface(textSurface,Rectangle(dst.x,dst.y))
        
        
            
        
        
        
        