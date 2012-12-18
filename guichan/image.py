#!/usr/bin/env python

from guichan import *
from imageLoader import ImageLoader

class Image:
    mImageLoader=None
    def setImageLoader(self,loader):
        if isinstance(loader,ImageLoader) == True:
            Image.mImageLoader=loader
            
    def getImageLoader(self):
        return Image.mImageLoader
    
    @staticmethod
    def load(fileName,convertToDisplayFormat=True):
        if Image.mImageLoader == None:
            raise GCN_EXCEPTION("Trying to load an image but no image loader is set.")
        
        return Image.mImageLoader.load(fileName,convertToDisplayFormat)
    
    def free(self):
        pass
    
    def getWidth(self):
        pass
    
    def getHeight(self):
        pass
    
    def getPixel(self,x,y):
        pass
    
    def putPixel(self,x,y,color):
        pass
    
    def convertToDisplayFormat(self):
        pass
    
    def setColorkey(self,color):
        pass
        
    def getColorkey(self):
        pass
    
    def setAlpha(self,alpha):
        pass
    
    def getAlpha(self):
        pass
            
            