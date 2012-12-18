#!/usr/bin/env python

from main import *
from sprite import Sprite
#Object collision types
SOLID, PUSHABLE, GHOST = 0, 1, 2

#Object group
PLAYER, ENEMY, ITEM, PROJECTILE, PLATFORM = 0, 1, 2, 3, 4

#Object collision groups
#Examples:
#if PLAYER obj hits ENEMY, it is registered
#if PLAYER obj hit PLAYER, it is not registered
#if NEUTRAL hits PLAYER or ENEMY, it is registered
#INVISIBLE objs does not register on any collision
PLAYER_GROUP, ENEMY_GROUP, NEUTRAL_GROUP, INVISIBLE_GROUP = 1, 2, 4, 16

class ObjectType:
     def __init__(self,name):
          self.name=name
          self.width=0
          self.height=0
          self.maxVelX=0.0
          self.maxVelY=0.0
          self.accelX=0.0
          self.accelY=0.0
          self.jumpStart=0.0
          self.jumpHeight=0.0
          self.bounceX=0.0
          self.bounceY=0.0
          self.fall=True
          self.collision=SOLID
          self.group=ENEMY
          self.colGroup=NEUTRAL_GROUP
          self.controller=""
          self.sprite=Sprite()
          self.data={}
          
     def SetSprite(self,sprite):
          self.sprite=sprite
          self.width=sprite.offX
          self.height=sprite.offY
          
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
          dump(self.width,f)
          dump(self.height,f)
          dump(self.maxVelX,f)
          dump(self.maxVelY,f)
          dump(self.accelX,f)
          dump(self.accelY,f)
          dump(self.jumpStart,f)
          dump(self.jumpHeight,f)
          dump(self.bounceX,f)
          dump(self.bounceY,f)
          dump(self.fall,f)
          dump(self.collision,f)
          dump(self.controller,f)
          self.sprite.Save(f)
          dump(self.data,f)
          
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
          self.name=load(f)
          self.width=load(f)
          self.height=load(f)
          self.maxVelX=load(f)
          self.maxVelY=load(f)
          self.accelX=load(f)
          self.accelY=load(f)
          self.jumpStart=load(f)
          self.jumpHeight=load(f)
          self.bounceX=load(f)
          self.bounceY=load(f)
          self.fall=load(f)
          self.collision=load(f)
          self.controller=load(f)
          self.sprite.Load(f)
          self.data=load(f)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()