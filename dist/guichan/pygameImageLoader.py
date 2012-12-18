#!/usr/bin/env python

import pygame
from pygame.locals import *

from imageLoader import ImageLoader
from exception import *
from pygameImage import PygameImage

class PygameImageLoader(ImageLoader):
    def load(self,fileName,convert):
        loadedSurface=pygame.image.load(fileName)
        
        if loadedSurface == None:
            raise GCN_EXCEPTION("Unable to load image file: "+fileName)
        
        surface = self.convertToStandardFormat(loadedSurface)
        del loadedSurface
        
        if surface == None:
            raise GCN_EXCEPTION("Not enough memory to load: "+fileName)
        
        image = PygameImage(surface,True)
        
        if convert == True:
            image.convertToDisplayFormat()
            
        return image
            
    def loadSurface(self,fileName):
        return pygame.image.load(fileName)
    
    def convertToStandardFormat(self,surface):
        return surface