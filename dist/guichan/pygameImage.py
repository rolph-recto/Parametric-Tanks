#!/usr/bin/env python

import pygame
#from pygame.locals import *
#There's two Colors! Error!

from guichan import *
from image import Image

def GuichanToPygameColor(color):
    return (color.r,color.g,color.b,color.a)

class PygameImage(Image):
    def __init__(self,surface,autoFree):
        self.mSurface=surface
        self.mAutoFree=autoFree
        
    def __del__(self):
        if self.mAutoFree == True:
            del self.mSurface
    
    def getSurface(self):
        return self.mSurface
    
    def getWidth(self):
        if self.mSurface == None:
            raise GCN_EXCEPTION("Trying to get the width of a non loaded image.")
        
        return self.mSurface.get_width()
    
    def getHeight(self):
        if self.mSurface == None:
            raise GCN_EXCEPTION("Trying to get the height of a non loaded image.")
        
        return self.mSurface.get_height()
    
    def getPixel(self,x,y):
        if self.mSurface == None:
            raise GCN_EXCEPTION("Trying to get a pixel of a non loaded image.")
        
        c=self.mSurface.get_at( (x,y) )
        return Color(c[0],c[1],c[2],c[3])
    
    def putPixel(self,x,y,color):
        if self.mSurface == None:
            raise GCN_EXCEPTION("Trying to put a pixel of a non loaded image.")
        self.mSurface( (x,y), GuichanToPygameColor(color) )
        
    def setColorkey(self,color):
        self.mSurface.set_colorkey( GuichanToPygameColor(color) )
        
    def getColorkey(self):
        c=self.mSurface.get_colorkey()
        if c != None:
            return Color(c[0],c[1],c[2])
        else:
            return None
    
    def setAlpha(self,alpha):
        if (alpha > -1 and alpha < 256) or alpha == None: 
            self.mSurface.set_alpha(alpha)
    
    def getAlpha(self):
        return self.mSurface.get_alpha()

    def convertToDisplayFormat(self):
        temp=self.mSurface.convert()
        self.mSurface=temp
        
    def free(self):
        del self.mSurface
        
        