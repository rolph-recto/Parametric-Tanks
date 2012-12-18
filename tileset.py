#!/usr/bin/env python

from main import *

class Tileset:
     def __init__(self):
          self.surface=None
          self.posX=0
          self.posY=0
          self.offX=0
          self.offY=0
          self.alpha=255
          self.colorKey=Color(0xFFFFFF)
          self.xNum=0
          self.yNum=0
          self.name=""
     
     def Save(self,file):
          f=None
          #if file is a string
          if type(file) == type("abc"):
               f=open(file,"wb")
          
          #file is a file object
          else:
               f=file
               
          if f == None:
               return None
               
          #commence writing
          dump(self.name,f)
          dump(self.offX,f)
          dump(self.offY,f)
          dump(self.alpha,f)
          dump(self.colorKey,f)
          dump(self.xNum,f)
          dump(self.yNum,f)
          dump(self.surface.get_width(),f)
          dump(self.surface.get_height(),f)
          dump(pygame.image.tostring(self.surface,"RGB"),f, HIGHEST_PROTOCOL)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
          
     def Load(self,file):
          f=None
          #if file is a string
          if type(file) == type("abc"):
               f=open(file,"rb")
          
          #file is a file object
          else:
               f=file
               
          if f == None:
               return None
               
          #commence reading
          self.name=load(f)
          self.offX=load(f)
          self.offY=load(f)
          self.alpha=load(f)
          self.colorKey=load(f)
          self.xNum=load(f)
          self.yNum=load(f)
          width=load(f)
          height=load(f)
          self.surface=pygame.image.frombuffer(load(f),(width,height),"RGB")
          
          self.SetAlpha(self.alpha)
          self.SetColorKey(self.colorKey)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
     
     def Create(self,surface,name,offx,offy):
          #surface is a file
          if type(surface)==type("abc"):
               img=pygame.image.load(surface)
               surface=img
          
          if surface == None or surface.get_width()%offx != 0 or surface.get_height()%offy != 0:
               return False
          
          self.surface=surface
          self.offX=offx
          self.offY=offy
          self.xNum=surface.get_width()/offx
          self.yNum=surface.get_height()/offy
          return True
          
     def SetName(self,name):
          self.name=name
          
     def SetPosition(self,x,y):
          self.posX=x
          self.posY=y
          
     def SetPosX(self,x):
          self.posX=x      

     def SetPosY(self,y):
          self.posy=y        

     def SetAlpha(self,alpha):
          if alpha >= 0 and alpha <= 255:
               self.alpha=alpha
               self.surface.set_alpha(self.alpha, pygame.RLEACCEL)
     
     def SetColorKey(self,c):
          self.colorKey=c
          self.surface.set_colorkey(c.ToTuple())
          
     def Draw(self,dest,tileNum, tx=0, ty=0, tw=-1, th=-1):
          if dest == None or tileNum > self.xNum*self.yNum:
               return None
               
          y=floor(tileNum/self.xNum)
          x=tileNum-(y*self.xNum)
          temp=Rectangle()
          temp2=Rectangle()
          temp.x=x*self.offX+tx
          temp.y=y*self.offY+ty
          if tw >= 0:
               temp.w=tw
          else:
               temp.w=self.offX
          if th >= 0:
               temp.h=th
          else:
               temp.h=self.offY
          temp2.x=self.posX+tx
          temp2.y=self.posY+ty
          
          dest.blit(self.surface,temp2.ToTuple(),temp.ToTuple())
