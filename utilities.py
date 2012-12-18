#!/usr/bin/env python

import math
#sine and cosine table
sin=[]
cos=[]
#there are 360 degrees, right?
for i in range(360):
    sin.append( math.sin( math.radians(i) ) )
    cos.append( math.cos( math.radians(i) ) )

class ZeroException(Exception):
     def __init__(self,msg):
          self.msg=msg
          
     def __str__(self):
          return self.msg
          
     def __repr__(self):
          return self.msg
          
class Point:
    """Class for manipulation coordinates"""
    def __init__(self,x,y):
        self.x, self.y = x, y
        
    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)
    
    def __mul__(self,other):
        return Point(self.x*other.x,self.y*other.y)
    
    def __div__(self,other):
        return Point(self.x/other.x,self.y/other.y)
    
    def __invert__(self):
        return Point(~self.x,~self.y)

    def __abs__(self):
        return Point(abs(self.x),abs(self.y))
    
    def __neg__(self):
        return Point(-self.x,-self.y)
    
    def __repr__(self):
        return "Point("+str(self.x)+","+str(self.y)+")"
    
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    
    def __getitem__(self,i):
        if i==0:
            return self.x
        elif i==1:
            return self.y

class Bitset:
    "Provides a class for manipulating bits"
    def __init__(self,val=1):
        self.set=[]
        self.Parse(val)
    
    def __getitem__(self,i):
        return self.set[i]

    def __setitem__(self,i,val):
        if val==0 or val==1:
            self.set[i]=val
    
    def __or__(self, other):
        #self and other must be same size
        if len(self.set)==len(other.set):
            set=Bitset(0)
            set.Resize(len(self.set))
            for i in range(len(self.set)):
                set[i]=self.set[i] | other.set[i]
            return set
        
        return self
        
    def __and__(self, other):
        #self and other must be same size
        if len(self.set)==len(other.set):
            set=Bitset(0)
            set.Resize(len(self.set))
            
            for i in range(len(self.set)):
                set[i]=self.set[i] & other.set[i]
            return set
        
        return self
        
    def __xor__(self, other):
        #self and other must be same size
        if len(self.set)==len(other.set):
            set=Bitset(0)
            set.Resize(len(self.set))
            for i in range(len(self.set)):
                set[i]=self.set[i] ^ other.set[i]
            return set
        
        return self
        
    def __eq__( self, other):
        if type(self)==type(other):
            if len(self.set)==len(other.set):
                eq=True
                for i in range(len(self.set)):
                    if self.set[i]!=other.set[i]:
                        eq=False
                return eq
            else:
                return False
        elif type(other)==type(True):
            return self.Zero()
        else:
            return False
    
    def __repr__(self):
        return "Bitset("+str(self.Val())+")"
    
    def __str__(self):
        s=""
        for i in self.set:
            s+=str(i)    
        return s
    
    def __len__(self):
        return len(self.set)
    
    def __nonzero__(self):
        return self.Zero()
    
    def Zero(self):
        eq=True
        for i in self.set[:]:
            if i!=0:
                eq=False
                break
        return eq
    
    def Flip(self,index=-1):
        if index==-1:
            for i in range(len(self.set)):
                self.Flip(i)
        elif index>-1:
            if index<len(self.set):
                if self.set[index]==1:
                    self.set[index]=0
                else:
                    self.set[index]=1        

    def Size(self):
        return len(self.set)
    
    def Test(self,index,val=1):
        if index>-1 and index<len(self.set):
            if self.set[index]==val:
                return True
            else:
                return False
    
    def Set(self,index=-1):
        if index>-1 and index<len(self.set):
            self.set[index]=1
        elif index==-1:
            for i in range(len(self.set)):
                self.set[i]=1
                
    def Reset(self,index=-1):
        if index>-1 and index<len(self.set):
            self.set[index]=0
        elif index==-1:
            for i in range(len(self.set)):
                self.set[i]=0
    
    def Parse(self,str):
        if type(str)==type("abc"):
            self.Resize(len(str))
            for i in range(len(str)):
                self[i]=int(str[i])
        elif type(str)==type(1):
            #must convert base 10 to base 2 (decimal to binary)
            if str > 0 or str < 0:
                if str < 0:
                    str *= -1
                    
                quotient=str
                bin=[]
                while quotient != 1:
                    bin.append(quotient%2)
                    quotient/=2
                bin.append(quotient%2)
                bin.reverse()
                self.Resize(len(bin))
                for i in range(len(bin)):
                    self[i]=bin[i]
            
            else:
                self.Resize(1)
                self[0]=0
    
    def Val(self):
        val=0
        self.set.reverse()
        for i in range(len(self.set)):
            val+=(2**i)*(self.set[i])
        self.set.reverse()    
        return val    
    
    def Resize(self,size):
        if len(self.set)<size:
            while len(self.set)<size:
                self.set.append(0)
        else:
            while len(self.set)>size:
                self.set.pop()
                
class Color:
    def __init__(self,r=-1,g=-1,b=-1,a=255):
          self.Set(r,g,b,a)
    
    def Set(self,r=-1,g=-1,b=-1,a=255):
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
            c=Color(self.r+other.r, self.g+other.g, self.b+other.b, self.a+other.a)
        else:
            c=Color(self.r+((other >> 16)&0xFF),self.g+((other >> 8)&0xFF),self.b+(other&0xFF),self.a)
        c.r=(255 if c.r>255 else (0 if c.r<0 else c.r))
        c.g=(255 if c.g>255 else (0 if c.g<0 else c.g))
        c.b=(255 if c.b>255 else (0 if c.b<0 else c.b))
        return c
    
    def __sub__(self,other):
        if type(other) == type(self):
            c=Color(self.r-other.r, self.g-other.g, self.b-other.b, self.a-other.a)
        else:
            c=Color(self.r-((other >> 16)&0xFF),self.g-((other >> 8)&0xFF),self.b-(other&0xFF),self.a)
        c.r=(0 if c.r<0 else (255 if c.r>255 else c.r))
        c.g=(0 if c.g<0 else (255 if c.g>255 else c.g))
        c.b=(0 if c.b<0 else (255 if c.b>255 else c.b))
        return c
    
    def __mul__(self,val):
        c=Color(self.r*val, self.g*val, self.b*val, self.a)
        c.r=(0 if c.r<0 else (255 if c.r>255 else c.r))
        c.g=(0 if c.g<0 else (255 if c.g>255 else c.g))
        c.b=(0 if c.b<0 else (255 if c.b>255 else c.b))
        return c
    
    def __div__(self,val):
        c=Color(self.r/val, self.g/val, self.b/val, self.a)
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
        return tuple((self.r,self.g,self.b,self.a))

class Shape:
    def __init__(self,x,y):
        self.posX=x
        self.posY=y
        self.scale=1.0
        self.rotate=0.0
        
    def SetPosition(self,x,y):
        self.posX=x
        self.posY=y
    
    def SetScale(self,scale):
        pass
    
    def SetRotate(self,rotate):
        pass    
    
    def Clone(self):
        return Shape(self.posX,self.posY)

class Rectangle(Shape):
    def __init__(self,x=0,y=0,w=0,h=0):
        if type(x) == type(123) or type(x)==type(123.0):
            self.setAll(x,y,w,h)
        else:
            self.x=x.x
            self.y=x.y
            self.w=x.w
            self.h=x.h
        
    def __repr__(self):
        return "Rectangle("+str(self.x)+","+str(self.y)+","+str(self.w)+","+str(self.h)+")"
        
    def __str__(self):
        return "Rectangle [x="+str(self.x)+", y="+str(self.y)+", w="+str(self.w)+", h="+str(self.h)+"]"

    def setAll(self,x=0,y=0,w=0,h=0):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        
    def union(self,other):    
        r=self.__add__(other)
        self.x=r.x
        self.y=r.y
        self.w=r.w
        self.h=r.h
    
    def intersection(self,other):
        if self.isIntersecting(other):
            if self.isBoundTo(other) == False:
                if other.isBoundTo(self) == True:
                    self=Rectangle(other)
                    return None
                
                minX1, minY1, maxX1, maxY1 = self.x, self.y, self.x+self.w, self.y+self.h
                minX2, minY2, maxX2, maxY2 = other.x, other.y, other.x+other.w, other.y+other.h
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
          w=self.w
          h=self.h
            
          x-=other.x
          y-=other.y
            
          if x < 0:
               w+=x
               x=0
          elif x+w > other.w:
               w=other.w-x
                
          if y < 0:
               h+=y
               y=0
          elif y+h > other.h:
               h=other.h-y
            
          if w <= 0 or h <= 0:
               return False
        
          return True
    
    def isPointInRect(self,x,y):
        return x >= self.x and y >= self.y and x <= self.x+self.w and y <= self.y+self.h
    
    def clipTo(self,other):
        if self.x < other.x:
            self.x=other.x
        if self.y < other.y:
            self.y=other.y
            
        if self.x+self.w > other.x+other.w:
            self.w=other.x+other.w-self.x
            if self.w < 0:
                self.w=0        
        if self.y+self.h > other.y+other.h:
            self.h=other.y+other.h-self.y
            if self.h < 0:
                self.h=0
                
    def isBoundTo(self,other):
        return self.x >= other.x and self.y >= other.y and self.x+self.w <= other.x+other.w and self.y <= other.y+other.h
        
    def __add__(self,other):
        minX, minY, maxX, maxY = self.x, self.y, self.w+self.x, self.h+self.y
        
        if other.x < minX:
            minX=other.x
        
        if other.y < minY:
            minY=other.y
            
        if other.x+other.w > maxX:
            maxX=other.x+other.w

        if other.y+other.h > maxY:
            maxY=other.y+other.h
        
        return Rectangle(minX, minY, maxX-minX, maxY-minY)
    
    def __sub__(self,other):
        if self.isIntersecting(other):
            if self.isBoundTo(other) == False:
                if other.isBoundTo(self) == True:
                    return Rectangle(other)
                
                minX1, minY1, maxX1, maxY1 = self.x, self.y, self.x+self.w, self.y+self.h
                minX2, minY2, maxX2, maxY2 = other.x, other.y, other.x+other.w, other.y+other.h
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
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h
    
    def __ne__(self,other):
        return not (self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h)
        
    def ToTuple(self):
        return tuple((self.x,self.y,self.w,self.h))
        
    def Clone(self):
        return Rectangle(self.x,self.y,self.w,self.h)
            
        
class Polygon(Shape):
    """Class for representing polygons"""
    
    def __init__(self,p,x,y):
        Shape.__init__(self,x, y)
        
        self.basepoints=list(p)
        self.points=[]
        for i in self.basepoints:
            self.points.append(list(i))
            
        self.numpoints=len(p)
        self.rotate=0.0
        self.scaleX=1.0
        self.scaleY=1.0
        self.scale=(self.scaleX+self.scaleY)/2
        
        self.Reset()
            
    def Reset(self):
        for i in range(len(self.points)):
            self.points[i][0]=int(self.basepoints[i][0]*self.scaleX)
            self.points[i][1]=int(self.basepoints[i][1]*self.scaleY)
            
            #rotate
            rx=(math.cos(math.radians(self.rotate)) * self.points[i][0]) - (math.sin(math.radians(self.rotate)) * self.points[i][1])
            ry=(math.sin(math.radians(self.rotate)) * self.points[i][0]) + (math.cos(math.radians(self.rotate)) * self.points[i][1])
            self.points[i][0]=int(rx+self.posX)
            self.points[i][1]=int(ry+self.posY)
    
    def SetPosition(self,x,y):
        dx=x-self.posX
        dy=y-self.posY
        self.posX=x
        self.posY=y
        
        #add position
        for i in range(len(self.points)):
            self.points[i][0]=self.points[i][0]+dx
            self.points[i][1]=self.points[i][1]+dy
            
    def SetScale(self,x=0.0,y=0.0):
        if x > 0.0:
            self.scaleX=x
            
            if y > 0.0:
                self.scaleY=y
            else:
                self.scaleY=x

            self.scale=(self.scaleX+self.scaleY)/2
            self.Reset()
            
    def SetRotate(self,r):
        self.rotate=r
        
        #find coterminals
        if self.rotate < 0.0:
            self.rotate+=360.0
        elif self.rotate >= 360.0:
            self.rotate-=360.0
        
        self.Reset()
        
    def Clone(self):
        p=Polygon(self.basepoints,self.posX,self.posY)
        p.SetRotate(self.rotate)
        p.SetScale(self.scaleX,self.scaleY)
        
        return p
        
            
class Circle(Shape):
    def __init__(self,x,y,r):
        Shape.__init__(self,x,y)
        self.baseradius=r
        self.radius=r
        self.scale=1.0
        self.rotate=0.0
    
    def SetScale(self,scale):
        self.scale=scale
        self.radius=int(self.baseradius*scale)
    
    def SetRotate(self,rotate):
        #Can't rotate a circle!
        pass
    
    def Clone(self):
        c=Circle(self.posX,self.posY,self.radius)
        c.SetScale(self.scale)
        return c
        

def SetBound(val,min,max):
     if val < min:
          return min
     elif val > max:
          return max
     else:
          return val
          
def Swap(a,b):
     return b, a
   
def BrensenhamLine(a,b):
     result=[]
     steep = abs(b.y-a.y) > abs(b.x-a.x)
     
     if steep:
          a.x, a.y=Swap(a.x, a.y)
          b.x, b.y=Swap(b.x, b.y)
     
     if a.x > b.x:
          a.x, b.x=Swap(a.x, b.x)
          a.y, b.y=Swap(a.y, b.y)
          
     deltaX=b.x-a.x
     deltaY=abs(b.y-a.y)
     error=0
     ystep=0
     y=a.y
     
     if a.y < b.y:
          ystep=1
     else:
          ystep=-1
     
     for x in range(a.x,b.x+1):
          if steep:
               result.append( Point(y,x) )
          else:
               result.append( Point(x,y) )
          error=error+deltaY
          if 2*error >= deltaX:
               y=y+ystep
               error=error-deltaX
               
     return result

          
          
        