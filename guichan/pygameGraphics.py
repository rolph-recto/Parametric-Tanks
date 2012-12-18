#!/usr/bin/env python

import pygame
import pygame.surface
#from pygame.locals import *
#There's two Colors! Error!

from guichan import *
from graphics import Graphics
from pygameImage import PygameImage
from pygameImage import GuichanToPygameColor
import pygame.gfxdraw
from font import Font

def GuichanToPygameDirtyRect(dirtyRect):
    pRect=[]
    for i in dirtyRect:
        pRect.append( (i.x, i.y, i.width, i.height) )
    
    #if len(pRect) > 1:
        #print pRect
    return pRect

class PygameGraphics(Graphics):
    def __init__(self):
        Graphics.__init__(self)
        self.mAlpha=True
        self.mTarget=None
        self.mColor=Color(255,255,255,255)
        
    def beginDraw(self):
        self.pushClipArea( Rectangle(0,0,self.mTarget.get_width(),self.mTarget.get_height()) )
        self.mTarget.lock()
        
    def endDraw(self):
        self.popClipArea()
        self.mTarget.unlock()
        
    def setTarget(self,surface):
        self.mTarget=surface
        
    def getTarget(self):
        return self.mTarget
        
    def pushClipArea(self,area):
        result=Graphics.pushClipArea(self,area)
        top=self.mClipStack[-1]
        self.mTarget.set_clip( pygame.Rect(top.x,top.y,top.width,top.height) )
        
        return result
    
    def popClipArea(self):
        Graphics.popClipArea(self)
        if len(self.mClipStack) > 0:
            top=self.mClipStack[-1]
            self.mTarget.set_clip( pygame.Rect(top.x,top.y,top.width,top.height) )
            
    def drawImage(self,image,srcX,srcY,dstX=-1,dstY=-1,width=-1,height=-1):
        if width == -1 or height == -1 or dstX == -1 or dstY == -1:
            self.drawImage(image,0,0,srcX,srcY,image.getWidth(),image.getHeight())
        else:                
            if len(self.mClipStack) == 0:
                raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
            if srcX < 0 or srcY < 0:
                raise GCN_EXCEPTION("Source coordinates can't be negative!")
            
            top=ClipRectangle(self.mClipStack[-1])
            src = pygame.Rect(srcX,srcY,width,height)
            dst = pygame.Rect(dstX+top.xOffset,dstY+top.yOffset,0,0)
            
            if isinstance(image,PygameImage) == False:
                raise GCN_EXCEPTION("Trying to draw an image of unknown format, must be a PygameImage.")
            self.mTarget.unlock()    
            self.mTarget.blit(image.getSurface(),dst,src)
            self.mTarget.lock()
            
    def fillRectangle(self,rect):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
        
        top=self.mClipStack[-1]
        area=Rectangle(rect)
        area.x+=top.xOffset
        area.y+=top.yOffset
        
        if area.isIntersecting(top) == False:
            return None
        
        #pygame.GFX.box(self.mTarget, area.x, area.x+area.width, area.y, area.y+area.height, self.mColor.r, self.mColor.g, self.mColor.b, self.mColor.a)
        pygame.gfxdraw.box(self.mTarget, (area.x,area.y,area.width,area.height), self.mColor.ToTuple())
        
    def drawPoint(self,x,y):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
        
        top=self.mClipStack[-1]
        x+=top.xOffset
        y+=top.yOffset
        
        if top.isPointInRect(x,y) == False:
            return None
        
        #pygame.GFX.pixel(self.mTarget, x, y, self.mColor.r, self.mColor.g, self.mColor.b, self.mColor.a)
        pygame.gfxdraw.pixel(self.mTarget, x, y, self.mColor.ToTuple())
        
    def drawHLine(self,x1,y,x2,surf=None):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
        Ox1=x1
        Ox2=x2
        Oy=y
        top=self.mClipStack[-1]
        x1+=top.xOffset
        y+=top.yOffset
        x2+=top.xOffset
        
        if y < top.y or y >= top.y+top.height:
            return None
        
        #if x1 is bigger, switch values
        if x1 > x2:
           x1^=x2
           x2^=x1
           x1^=x2
           
        if top.x > x1:
            if top.x > x2:
                return None
            
            x1=top.x
            
        if top.x+top.width <= x2:
            if top.x+top.width <= x1:
                return None
            
            x2=top.x+top.width-1
            
        #if self.mColor.a == 255 or self.mAlpha == False:
        #pygame.GFX.hline(self.mTarget, x1, x2, y, self.mColor.r, self.mColor.g, self.mColor.b, self.mColor.a)
        pygame.gfxdraw.hline(self.mTarget, x1, x2, y, self.mColor.ToTuple())
        """    
        elif self.mColor.a > 0 and surf != None:
            pygame.draw.line(surf,GuichanToPygameColor(self.mColor),(Ox1,Oy),(Ox2,Oy))
            
        elif self.mColor.a > 0:
            surf=pygame.surface.Surface((Ox2-Ox1,1), pygame.SWSURFACE, 32)
            surf.fill(GuichanToPygameColor(self.mColor))
            surf.set_alpha(self.mColor.a,pygame.RLEACCEL)
            self.mTarget.blit(surf,(x1,y))
        """
            
            
    
    def drawVLine(self,x,y1,y2,surf=None):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
        
        top=self.mClipStack[-1]
        Ox=x
        Oy1=y1
        Oy2=y2
        x+=top.xOffset
        y1+=top.yOffset
        y2+=top.yOffset
        
        if x < top.x or x >= top.x+top.width:
            return None
        
        if y1 > y2:
           y1^=y2
           y2^=y1
           y1^=y2
           
        if top.y > y1:
            if top.y > y2:
                return None
            
            y1=top.y
            
        if top.y+top.height <= y2:
            if top.y+top.height <= y1:
                return None
            
            y2=top.y+top.height-1
        
        #if self.mColor.a == 255 or self.mAlpha == False:
        #pygame.GFX.vline(self.mTarget, x, y1, y2, self.mColor.r, self.mColor.g, self.mColor.b, self.mColor.a)
        pygame.gfxdraw.vline(self.mTarget, x, y1, y2, self.mColor.ToTuple())
        """    
        elif self.mColor.a > 0 and surf != None:
            pygame.draw.line(surf,GuichanToPygameColor(self.mColor),(Ox,y1),(Ox,y2))
            
        elif self.mColor.a > 0:
            surf=pygame.surface.Surface((1,Oy2-Oy1), pygame.SWSURFACE, 32)
            surf.fill(GuichanToPygameColor(self.mColor))
            surf.set_alpha(self.mColor.a,pygame.RLEACCEL)
            self.mTarget.blit(surf,(x,y1))
        """
        
    def drawRectangle(self,rect):
        x1=rect.x
        x2=rect.x+rect.width-1
        y1=rect.y
        y2=rect.y+rect.height-1
        
        #if self.mColor.a == 255 or self.mAlpha == False:
        #pygame.GFX.rectangle(self.mTarget, x1, x2, y1, y2, self.mColor.r, self.mColor.g, self.mColor.b, self.mColor.a)
        #pygame.gfxdraw.rectangle(self.mTarget, (x1, y1, rect.width, rect.height), self.mColor.ToTuple())
                  
        self.drawHLine(x1, y1, x2)
        self.drawHLine(x1, y2, x2)

        self.drawVLine(x1, y1, y2)
        self.drawVLine(x2, y1, y2)
        """
        elif self.mColor.a > 0:
            surf=pygame.surface.Surface((rect.width,rect.height), pygame.SWSURFACE, 32)
            if self.mColor != 0x000000:
                surf.set_colorkey((0,0,0), pygame.RLEACCEL)
            else:
                surf.fill((255,0,255))
                surf.set_colorkey((255,0,255), pygame.RLEACCEL)
                
            self.drawHLine(x1, y1, x2, surf)
            self.drawHLine(x1, y2, x2, surf)

            self.drawVLine(x1, y1, y2, surf)
            self.drawVLine(x2, y1, y2, surf)
            
            top=self.mClipStack[-1]
            x1+=top.xOffset
            y1+=top.yOffset
            surf.set_alpha(self.mColor.a,pygame.RLEACCEL)
            self.mTarget.blit(surf,(x1,y1))
        """
        
    def drawLine(self,x1,y1,x2,y2):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
        
        top=self.mClipStack[-1]
        Ox1=x1
        Ox2=x2
        Oy1=y1
        Oy2=y2
        x1+=top.xOffset
        y1+=top.yOffset
        x2+=top.xOffset
        y2+=top.yOffset        
        
        #if self.mColor.a == 255 or self.mAlpha == False:
        #pygame.GFX.line(self.mTarget, x1, x2, y1, y2, self.mColor.r, self.mColor.g, self.mColor.b, self.mColor.a)
        pygame.gfxdraw.line(self.mTarget, x1, y1, x2, y2, self.mColor.ToTuple())
        """    
        elif self.mColor.a > 0:
            surf=pygame.surface.Surface( (abs(x2-x1), abs(y2-y1)), pygame.SWSURFACE, 32)
            if self.mColor != 0x000000:
                surf.set_colorkey((0,0,0), pygame.RLEACCEL)
            else:
                surf.fill((255,0,255))
                surf.set_colorkey((255,0,255), pygame.RLEACCEL)
                
            pygame.draw.line(surf,GuichanToPygameColor(self.mColor),(Ox1,Oy1),(Ox2,Oy2))
            surf.set_alpha(self.mColor.a)
            x, y = 0, 0
            if x1 < x2:
                x=x1
            else:
                x=x2
                
            if y1 < y2:
                y=y1
            else:
                y=y2
                
            self.mTarget.blit(surf,(x,y))
        """
            
    def setColor(self,color):
        self.mColor=color
        
    def getColor(self):
        return self.mColor
    
    def drawSurface(self,surface,dst,src=None):
        if len(self.mClipStack) == 0:
            raise GCN_EXCEPTION("Clip stack is empty, perhaps you called a draw funtion outside of beginDraw() and endDraw()?")
        
        top=self.mClipStack[-1]
        dst.x+=top.xOffset
        dst.y+=top.yOffset
        
        self.mTarget.unlock()
        
        if src != None:
            self.mTarget.blit(surface,pygame.Rect(dst.x,dst.y,0,0),pygame.Rect(src.x,src.y,src.width,src.height))
        
        else:
            self.mTarget.blit(surface,pygame.Rect(dst.x,dst.y,0,0))
            
        self.mTarget.lock()
    
            
        
        
        
        
    
    