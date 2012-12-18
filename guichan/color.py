#!/usr/bin/env python

from guichan import *

class Color:
    def __init__(self,r=-1,g=-1,b=-1,a=255):
        if type(r) == type(0):
            if r == -1:
                self.r=0
                self.g=0
                self.b=0
                self.a=a
            elif r != -1 and g == -1 and b == -1:
                self.r=(r >> 16)&0xFF
                self.g=(r >> 8)&0xFF
                self.b=(r)&0xFF
                self.a=a
            else:
                self.r=r
                self.g=g
                self.b=b
                self.a=a
        else:
            self.r=r.r
            self.g=r.g
            self.b=r.b
            self.a=r.a
            
        if self.r > 255:
            self.r=255
        if self.g > 255:
            self.g=255
        if self.b > 255:
            self.b=255
        if self.a > 255:
            self.a=255            
            
    def __repr__(self):
        return "Color("+str(self.r)+","+str(self.g)+","+str(self.b)+","+str(self.a)+")"
        
    def __str__(self):
        return "Color [r="+str(self.r)+", g="+str(self.g)+", b="+str(self.b)+", a="+str(self.a)+"]"
    
    def __add__(self,other):
        if type(other) == type(self):
            c=Color(self.r+other.r, self.g+other.g, self.b+other.b, self.a)
        else:
            c=Color(self.r+((other >> 16)&0xFF),self.g+((other >> 8)&0xFF),self.b+(other&0xFF),self.a)
        c.r=(255 if c.r>255 else (0 if c.r<0 else c.r))
        c.g=(255 if c.g>255 else (0 if c.g<0 else c.g))
        c.b=(255 if c.b>255 else (0 if c.b<0 else c.b))
        return c
    
    def __sub__(self,other):
        if type(other) == type(self):
            c=Color(self.r-other.r, self.g-other.g, self.b-other.b, self.a)
        else:
            c=Color(self.r-((other >> 16)&0xFF),self.g-((other >> 8)&0xFF),self.b-(other&0xFF),self.a)
        c.r=(0 if c.r<0 else (255 if c.r>255 else c.r))
        c.g=(0 if c.g<0 else (255 if c.g>255 else c.g))
        c.b=(0 if c.b<0 else (255 if c.b>255 else c.b))
        return c
    
    def __mul__(self,val):
        c=Color(self.r*val, self.g*val, self.b*val, 255)
        c.r=(0 if c.r<0 else (255 if c.r>255 else c.r))
        c.g=(0 if c.g<0 else (255 if c.g>255 else c.g))
        c.b=(0 if c.b<0 else (255 if c.b>255 else c.b))
        return c
    
    def __div__(self,val):
        c=Color(self.r/val, self.g/val, self.b/val, 255)
        c.r=(0 if c.r<0 else (255 if c.r>255 else c.r))
        c.g=(0 if c.g<0 else (255 if c.g>255 else c.g))
        c.b=(0 if c.b<0 else (255 if c.b>255 else c.b))
        return c
    
    def __eq__(self,other):
        if type(other) == type(self):
            return self.r == other.r and self.g == other.g and self.b == other.b #and self.a == other.a
        else:
            c=Color(other)
            return self == c
        
    def __ne__(self,other):
        if type(other) == type(self):
            return not (self.r == other.r and self.g == other.g and self.b == other.b) #and self.a == other.a)
        else:
            c=Color(other)
            return not (self == c)
            
    def ToTuple(self):
        return (self.r,self.g,self.b,self.a)
    