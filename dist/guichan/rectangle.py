#!/usr/bin/env python

from guichan import *

class Rectangle:
    def __init__(self,x=0,y=0,width=0,height=0):
        if type(x) == type(0):
            self.setAll(x,y,width,height)
        else:
            self.x=x.x
            self.y=x.y
            self.width=x.width
            self.height=x.height
        
    def __repr__(self):
        return "Rectangle("+str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)+")"
        
    def __str__(self):
        return "Rectangle [x="+str(self.x)+", y="+str(self.y)+", width="+str(self.width)+", height="+str(self.height)+"]"

    def setAll(self,x=0,y=0,width=0,height=0):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
    def union(self,other):    
        r=self.__add__(other)
        self.x=r.x
        self.y=r.y
        self.width=r.width
        self.height=r.height
    
    def intersection(self,other):
        if self.isIntersecting(other):
            if self.isBoundTo(other) == False:
                if other.isBoundTo(self) == True:
                    self=Rectangle(other)
                    return None
                
                minX1, minY1, maxX1, maxY1 = self.x, self.y, self.x+self.width, self.y+self.height
                minX2, minY2, maxX2, maxY2 = other.x, other.y, other.x+other.width, other.y+other.height
                x, y, w, h = 0, 0, 0, 0
        
                if minX1 <= minX2:
                    x=minX2
                    w=maxX1-minX2
            
                else:
                    x=minX1
                    w=maxX2-minX1
                
                if minY1 <= minY2:
                    y=minY2
                    h=maxY1-minY2
            
                else:
                    y=minY1
                    h=maxY2-minY1
                
                self.setAll(x,y,w,h)
        
    def isIntersecting(self,other):
        x=self.x
        y=self.y
        width=self.width
        height=self.height
            
        x-=other.x
        y-=other.y
            
        if x < 0:
            width+=x
            x=0
        elif x+width > other.width:
            width=other.width-x
                
        if y < 0:
            height+=y
            y=0
        elif y+height > other.height:
            height=other.height-y
            
        if width <= 0 or height <= 0:
            return False
        
        return True
    
    def isPointInRect(self,x,y):
        return x >= self.x and y >= self.y and x <= self.x+self.width and y <= self.y+self.height
    
    def clipTo(self,other):
        if self.x < other.x:
            self.x=other.x
        if self.y < other.y:
            self.y=other.y
            
        if self.x+self.width > other.x+other.width:
            self.width=other.x+other.width-self.x
            if self.width < 0:
                self.width=0        
        if self.y+self.height > other.y+other.height:
            self.height=other.y+other.height-self.y
            if self.height < 0:
                self.height=0
                
    def isBoundTo(self,other):
        return self.x >= other.x and self.y >= other.y and self.x+self.width <= other.x+other.width and self.y <= other.y+other.height
        
    def __add__(self,other):
        minX, minY, maxX, maxY = self.x, self.y, self.width+self.x, self.height+self.y
        
        if other.x < minX:
            minX=other.x
        
        if other.y < minY:
            minY=other.y
            
        if other.x+other.width > maxX:
            maxX=other.x+other.width

        if other.y+other.height > maxY:
            maxY=other.y+other.height
        
        return Rectangle(minX, minY, maxX-minX, maxY-minY)
    
    def __sub__(self,other):
        if self.isIntersecting(other):
            if self.isBoundTo(other) == False:
                if other.isBoundTo(self) == True:
                    return Rectangle(other)
                
                minX1, minY1, maxX1, maxY1 = self.x, self.y, self.x+self.width, self.y+self.height
                minX2, minY2, maxX2, maxY2 = other.x, other.y, other.x+other.width, other.y+other.height
                x, y, w, h = 0, 0, 0, 0
        
                if minX1 <= minX2:
                    x=minX2
                    w=maxX1-minX2
            
                else:
                    x=minX1
                    w=maxX2-minX1
                
                if minY1 <= minY2:
                    y=minY2
                    h=maxY1-minY2
            
                else:
                    y=minY1
                    h=maxY2-minY1
                
                return Rectangle(x,y,w,h)
                
        else:
            return Rectangle(self)
        
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height
    
    def __ne__(self,other):
        return not (self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height)
    
class ClipRectangle(Rectangle):
    def __init__(self,x=0,y=0,width=0,height=0,xOffset=0,yOffset=0):
        if type(x) == type(0):
            self.setAll(x,y,width,height,xOffset,yOffset)
        elif isinstance(x,ClipRectangle) == False:
            self.x=x.x
            self.y=x.y
            self.width=x.width
            self.height=x.height
            self.xOffset=0
            self.yOffset=0
        else:
            self.x=x.x
            self.y=x.y
            self.width=x.width
            self.height=x.height
            self.xOffset=x.xOffset
            self.yOffset=x.yOffset
        
    def __repr__(self):
        return "ClipRectangle("+str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)+","+str(self.xOffset)+","+str(self.yOffset)+")"
        
    def __str__(self):
        return "ClipRectangle [x="+str(self.x)+", y="+str(self.y)+", width="+str(self.width)+", height="+str(self.height)+", xOffset="+str(self.xOffset)+", yOffset="+str(self.yOffset)+"]"

    def setAll(self,x=0,y=0,width=0,height=0,xOffset=0,yOffset=0):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.xOffset=xOffset
        self.yOffset=yOffset