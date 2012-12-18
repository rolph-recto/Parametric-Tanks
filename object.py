#!/usr/bin/env python

from main import *
from message import *
from objType import *

class PhysicsState:
     def __init__(self):
          self.posX=0
          self.posY=0
          self.velX=0
          self.velY=0
          self.accelX=0
          self.accelY=0
        
     def copy(self,other):
          self.x=other.x
          self.y=other.y
          self.velx=other.velx
          self.vely=other.vely
          self.accelx=other.accelx
          self.accely=other.accely

class Object(Dispatcher):
     def __init__(self,type):
          Dispatcher.__init__(self)
          self.type=type
          self.name=""
          self.id=0
          self.__posX=0
          self.__posY=0
          self.__velX=0.0
          self.__velY=0.0
          self.oldPosX=0
          self.oldPosY=0
          self.oldVelX=0.0
          self.oldVelY=0.0
          self.width=type.width
          self.height=type.height
          self.maxVelX=type.maxVelX
          self.maxVelY=type.maxVelY
          self.accelX=type.accelX
          self.accelY=type.accelY
          self.jumpStart=type.jumpStart
          self.jumpHeight=type.jumpHeight
          self.bounceX=type.bounceX
          self.bounceY=type.bounceY
          self.fall=type.fall
          self.jump=False
          self.jumpSpeed=0.0
          self.collision=type.collision
          self.group=type.group
          self.colGroup=type.colGroup
          self.oldState=PhysicsState()
          self.newState=PhysicsState()
          self.sprite=Sprite( type.sprite )
          self.action=[]
          self.action.append(False)
          self.action.append(False)
          self.action.append(False)
          self.action.append(False)
          self.action.append(False)
          self.remove=False
          self.platform=None
          self.ctrl=None
          self.disabled=False
        
          #copy data dictionary from type as default
          self.data=dict(type.data)
          
     def GenerateAction(self,action):
          if self.disabled == False:
               if action==UP or action ==DOWN or action==LEFT or action==RIGHT or action==JUMP:
                    self.action[action]=True
               elif action==UP_RIGHT:
                    self.action[UP]=True
                    self.action[RIGHT]=True
               elif action==UP_LEFT:
                    self.action[UP]=True
                    self.action[LEFT]=True
               elif action==DOWN_LEFT:
                    self.action[DOWN]=True
                    self.action[LEFT]=True
               elif action==DOWN_RIGHT:
                    self.action[DOWN]=True
                    self.action[RIGHT]=True
               elif action==JUMP_LEFT:
                    self.action[JUMP]=True
                    self.action[LEFT]=True
               elif action==JUMP_RIGHT:
                    self.action[JUMP]=True
                    self.action[RIGHT]=True
          
     def ResetAction(self):
          for i in range(len(self.action)):
               self.action[i]=False
               
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
          dump(self.name, f)
          dump(self.posX, f)
          dump(self.posY, f)
          dump(self.velX, f)
          dump(self.velY, f)
          dump(self.width, f)
          dump(self.height, f)
          dump(self.maxVelX, f)
          dump(self.maxVelY, f)
          dump(self.accelX, f)
          dump(self.accelY, f)
          dump(self.jumpStart, f)
          dump(self.jumpHeight, f)
          dump(self.bounceX, f)
          dump(self.bounceY, f)
          dump(self.fall, f)
          dump(self.collision, f)
          dump(self.data,f)
               
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
          self.posX=load(f)
          self.posY=load(f)
          self.velX=load(f)
          self.velY=load(f)
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
          self.data=load(f)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
     
               
     def getposx(self):
          return self.__posX
    
     def setposx(self,x):
          self.oldPosX=self.__posX
          self.__posX=x
    
     posX=property(getposx,setposx)
    
     def getposy(self):
          return self.__posY
    
     def setposy(self,y):
          self.oldPosY=self.__posY
          self.__posY=y
    
     posY=property(getposy,setposy)
    
     def getvelx(self):
          return self.__velX
    
     def setvelx(self,velx):
          self.oldVelX=self.__velX
          self.__velX=velx
    
     velX=property(getvelx,setvelx)
     
     def getvely(self):
          return self.__velY
    
     def setvely(self,vely):
          self.oldVelY=self.__velY
          self.__velY=vely
    
     velY=property(getvely,setvely)
     
     """
     def getaccelx(self):
          return self.newState.accelX
    
     def setaccelx(self,accelx):
          self.newState.accelX=accelx
    
     accelX=property(getaccelx,setaccelx)
    
     def getaccely(self):
          return self.newState.accelY
    
     def setaccely(self,accely):
          self.newState.accelY=accely
    
     accelY=property(getaccely,setaccely)
    
     def SwapPhysicsState(self):
          #newState is ready to be modified!
          self.oldState.copy(self.newState)
     """
    