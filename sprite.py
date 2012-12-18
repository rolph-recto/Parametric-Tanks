#!/usr/bin/env python

from main import *

#animation types
ONE_SHOT=0
NORMAL=2
PING_PONG=3

class Animation:
     def __init__(self):
          self.startFrame=0
          self.endFrame=0
          self.type=NORMAL
          self.direction=0
          
class AnimData:
     def __init__(self):
          self.name=""
          self.offX=0
          self.offY=0
          self.surface=None
          self.animSet=[]
          self.colorKey=Color(0xFFFFFF)
     
class Sprite:
     def __init__(self,spr=None):
          self.posX=0
          self.posY=0
          self.currentAnim=0
          self.currentFrame=0
          self.animData=AnimData()
          self.paused=False
          self.drawNum=0
          self.animFactor=0
          self.alpha=255
          if spr != None:
               self.Clone(spr)
     
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
          dump(self.animData.name,f)
          dump(self.animData.offX,f)
          dump(self.animData.offY,f)
          dump(self.animFactor,f)
          dump(self.alpha,f)
          dump(self.animData.colorKey,f)
          dump(len(self.animData.animSet),f)
          for i in self.animData.animSet[:]:
               dump(i.type,f)
               dump(i.startFrame,f)
               dump(i.endFrame,f)
               dump(i.direction,f)
          
          dump(self.animData.surface.get_width(),f)
          dump(self.animData.surface.get_height(),f)
          dump(pygame.image.tostring(self.animData.surface,"RGB"), f, HIGHEST_PROTOCOL)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
               
     def Load(self,file):
          f=None
          #if file is a string
          if type(file) == type("abc") or type(file) == type(unicode("abc")):
               f=open(file,"rb")
          
          #file is a file object
          else:
               f=file
               
          if f == None:
               return None
               
          #commence reading
          self.animData=AnimData()
          
          self.animData.name=load(f)
          self.animData.offX=load(f)
          self.animData.offY=load(f)
          self.animFactor=load(f)
          self.alpha=load(f)
          self.animData.colorKey=load(f)
          len=load(f)
          for i in range(len):
               a=Animation()
               a.type=load(f)
               a.startFrame=load(f)
               a.endFrame=load(f)
               a.direction=load(f)
               self.animData.animSet.append(a)
          
          width=load(f)
          height=load(f)
          self.animData.surface=pygame.image.frombuffer(load(f),(width,height),"RGB")
          
          self.SetColorKey(self.animData.colorKey)
          self.SetAlpha(self.alpha)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
     
     def Create(self,tsurface,tname,x,y):
          if tsurface!=None and tsurface.get_width()%x==0 and tsurface.get_height()%y==0:
               temp=Animation()
               temp.startFrame=0
               temp.endFrame=tsurface.get_width()/x-1
               temp.type=NORMAL
               self.animData=AnimData()
               self.animData.surface=tsurface
               self.animData.offX=x
               self.animData.offY=y
               self.animData.colorKey.Set(0)
               self.animData.name=tname
               for i in range(self.animData.surface.get_height()/y):
                    self.animData.animSet.append(temp)
               
               return True
               
          return False
     
     def CreateFromFile(self,file,name,x,y):
          img=pygame.image.load(file)
          self.Create(img,name,x,y)
          
     def Clone(self,s):
          if s==None: return False
          self.animData=s.animData
          self.alpha=s.alpha
          self.posX=s.posX
          self.posY=s.posY
          self.currentFrame=s.currentFrame
          self.currentAnim=s.currentAnim
          self.animFactor=s.animFactor
     
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
     
     def SetColorKey(self,c):
          self.animData.colorKey=c
          self.animData.surface.set_colorkey(c.ToTuple())
          
     def SetAnimation(self,a):
          if a>-1 and a<len(self.animData.animSet):
               self.currentAnim=a
               
     def SetAnimProperties(self,a,type=NORMAL,start=-1,end=-1):
          if a>-1 and a<len(self.animData.animSet):
               self.animData.animSet[a].type=type
               if start != -1:
                    self.animData.animSet[a].startFrame=start
               if end != -1:
                    self.animData.animSet[a].endFrame=end
     
     def SetFrame(self,frame):
          if frame > -1:
               if frame > self.animData.animSet[currentAnim].endFrame:
                    self.currentFrame=self.animData.animSet[currentAnim].endFrame
               else:
                    self.currentFrame=frame
                    
     def SetAnimFactor(self,anim):
          if type(anim) == type(0):
               if anim > -1:
                    self.animFactor=anim
          
          elif type(anim) == type(0.123):
               self.animFactor=int(1/anim)
               
     def getname(self):
          return self.animData.name
          
     name=property(getname)
               
     def getcolorkey(self):
          return self.animData.colorKey
          
     colorKey=property(getcolorkey)
               
     def getoffx(self):
          return self.animData.offX
    
     offX=property(getoffx)
     
     def getoffy(self):
          return self.animData.offY
    
     offY=property(getoffy)
               
     def Pause(self):
          self.paused=True
     
     def Resume(self):
          if self.paused and self.animData.animSet[self.currentAnim].type == ONE_SHOT:
               self.currentFrame=self.animData.animSet[self.currentAnim].startFrame
               
          self.paused=False
          
     def Draw(self,dest,autoUpdate=True, tx=0, ty=0, tw=-1, th=-1):
          if dest != None:
               temp=Rectangle()
               temp2=Rectangle()
               
               temp.x=self.currentFrame*self.animData.offX+tx
               temp.y=self.currentAnim*self.animData.offY+ty
               if tw >= 0:
                    temp.w=tw
               else:
                    temp.w=self.animData.offX
                         
               if th >= 0:
                    temp.h=th
               else:
                    temp.h=self.animData.offY
                         
               temp2.x=self.posX+tx
               temp2.y=self.posY+ty
               
               self.animData.surface.set_alpha(self.alpha)
               dest.blit(self.animData.surface,Rect(temp2.ToTuple()),Rect(temp.ToTuple()))
               self.animData.surface.set_alpha(255)
               
               if autoUpdate:
                    self.Update()
                
     def Update(self):
          if self.drawNum >= self.animFactor:
               if self.animData.animSet[self.currentAnim].type == NORMAL:
                    if self.paused != True:
                         if self.currentFrame >= self.animData.animSet[self.currentAnim].endFrame:
                              self.currentFrame=self.animData.animSet[self.currentAnim].startFrame
                         else:
                              self.currentFrame=self.currentFrame+1
                        
               elif self.animData.animSet[self.currentAnim].type == ONE_SHOT:
                    if self.currentFrame >= self.animData.animSet[self.currentAnim].endFrame:
                         self.paused=True
                    if self.paused != True:
                         self.currentFrame=self.currentFrame+1
                    
               self.drawNum=0
            
          else:
               self.drawNum=self.drawNum+1
                
               
               
               
               
               
     
       