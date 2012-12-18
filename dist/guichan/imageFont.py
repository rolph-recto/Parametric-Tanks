#!/usr/bin/env python

from guichan import *
from font import Font
from image import Image
from graphics import Graphics

class ImageFont(Font):
    def __init__(self,image,startGlyph=32,endGlyph=126):
        self.mHeight=0
        self.mGlyphSpacing=0
        self.mRowSpacing=0
        self.mImage=None
        self.mFilename=""
        self.mGlyph={}
        glyphRange=[]
        #if image is an image...
        if isinstance(image,Image):
            self.mFilename="Image*"
            if image == None:
                raise GCN_EXCEPTION("Font image is NULL")
            self.mImage=image
            
        #or a filename
        elif type(image) == type("abc"):
            self.mFilename=image
            self.mImage=Image.load(self.mFilename,False)
            
        #ASCII code range of glyphs
        if type(startGlyph) == type(1) and type(endGlyph) == type(1):
            for i in range(endGlyph-startGlyph+1):
                glyphRange.append(startGlyph+i)
                
        #string range of glyphs
        elif type(startGlyph) == type("abc"):
            for i in range(len(startGlyph)):
                glyphRange.append( ord(startGlyph[i]) )
            
        separator=self.mImage.getPixel(0,0)
        i=0
        while not (separator == self.mImage.getPixel(i,0) and i < self.mImage.getWidth()):
            i+=1
                    
        if i >= self.mImage.getWidth():
            raise GCN_EXCEPTION("Corrupt image.")
                
        for j in range(self.mImage.getHeight()):
            if separator == self.mImage.getPixel(i,j):
                break
                    
        self.mHeight=self.mImage.getHeight()
        x, y = 0, 0
        for i in glyphRange:
            self.mGlyph[i]=self.scanForGlyph(i,x,y,separator)
            #Update x och y with new coordinates.
            x=self.mGlyph[i].x+self.mGlyph[i].width
            y=self.mGlyph[i].y
                    
        w=self.mImage.getWidth()
        h=self.mImage.getHeight()
        self.mImage.convertToDisplayFormat()
            
        self.mHeight=self.mImage.getHeight()
        self.mRowSpacing=0
        self.mGlyphSpacing=0
                
    def scanForGlyph(self,glyph,x,y,separator):
        color=Color()
        #find x and y coords of glpyh
        while True:
            x+=1
            if x >= self.mImage.getWidth():
                y+=self.mHeight+1
                x=0
                if y >= self.mImage.getHeight():
                    raise GCN_EXCEPTION("Image "+self.mFilename+" with font is corrupt near character '"+chr(glyph)+"'.")

            color=self.mImage.getPixel(x,y)
            if not (color==separator):
                break
            
        #find width of glyph
        width=0
        while True:
            width+=1
            if x+width >= self.mImage.getWidth():
                raise GCN_EXCEPTION("Image "+self.mFilename+" with font is corrupt near character '"+chr(glyph)+"'.")
            
            color=self.mImage.getPixel(x+width,y)
            if not (color!=separator):
                break
        
        #return glyph rectangle
        return Rectangle(x,y,width,self.mHeight)
    
    def setRowSpacing(self,spacing):
        self.mRowSpacing=spacing
        
    def setGlyphSpacing(self,spacing):
        self.mGlyphSpacing=spacing

    def getWidth(self,glyph):
        if len(glyph) == 1:
            if self.mGlyph[ord(glyph)].width==0:
                return self.mGlyph[ord(' ')].width + self.mGlyphSpacing
            else:
                return self.mGlyph[ord(glyph)].width + self.mGlyphSpacing
        elif len(glyph) > 1:
            size=0
            for i in range(len(glyph)):
                size+=self.getWidth(glyph[i])
                
            return size-self.mGlyphSpacing
        else:
            return 0
            
        
    def getHeight(self):
        return self.mHeight+self.mRowSpacing
    
    def getRowSpacing(self):
        return self.mRowSpacing
    
    def getGlyphSpacing(self):
        return self.mRowSpacing

    def getStringIndexAt(self,glyph,x):
        size=0
        for i in range(len(glyph)):
            size+=self.getWidth(glyph[i])
            if size > x:
                return i
            
        return len(glyph)
    
    def setColorkey(self,color):
        self.mImage.setColorkey(color)
        
    def getColorkey(self):
        return self.mImage.getColorkey()
    
    def setAlpha(self,alpha):
        self.mImage.setAlpha(alpha)
    
    def getAlpha(self):
        return self.mImage.getAlpha()
        
    def drawGlyph(self,graphics,glyph,x,y):
        yOffset=int(self.getRowSpacing()/2)
        glyphNum=ord(glyph)
        if self.mGlyph.has_key(glyphNum) == False:
            r=Rectangle(x,y+1+yOffset,self.mGlyph[ord(' ')].width-1,self.mGlyph[ord(' ')].height-2)
            graphics.drawRectangle(r)
            
            return self.mGlyph[ord(' ')].width + self.mGlyphSpacing
        
        else:
            graphics.drawImage(self.mImage,self.mGlyph[glyphNum].x,self.mGlyph[glyphNum].y,x,y+yOffset,self.mGlyph[glyphNum].width,self.mGlyph[glyphNum].height)
            
            return self.mGlyph[glyphNum].width+self.mGlyphSpacing
        
    def drawText(self,graphics,text,x,y,color=None):
        for i in range(len(text)):
            self.drawGlyph(graphics,text[i],x,y)
            x+=self.getWidth(text[i])
        
    
        
                    
                 
                