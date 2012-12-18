from main import *
from controller import *

class CannonballController(PersonController):
     def __init__(self,args):
          PersonController.__init__(self,args)
          self.velocity=args[2][0]
          self.angle=args[2][1]
          self.origX=self.object.posX
          self.origY=self.object.posY
          self.frame=main.frame
          self.cos=cos[self.angle]
          self.sin=sin[self.angle]
          self.phase=args[2][2]
          self.owner=args[2][3]
          
     def Update(self,args):
          global config
          
          #for fireballs
          if self.phase == 2:
               self.room.particle.AddParticle("circle5",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height/2),0,0,3.0,-0.01)
               self.room.particle.AddParticle("circle6",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height/2),0,0,3.0,-0.01)
          
          dframe=main.frame-self.frame
          #convert frames into seconds
          t=float(dframe)/config["PROJECTILE_SPEED"]
          #projectile motion formula
          x=(self.velocity*self.cos)*t+self.origX
          y=-((self.velocity*self.sin)*t-config["GRAVITY"]*(t**2))+self.origY
          #convert from 1st quadrant to 4th quadrant
          self.object.velX=-(self.object.posX-int(x))
          self.object.velY=-(self.object.posY-int(y))
          #self.object.posX=int(x)
          #self.object.posY=int(y)
          
     def OnObjectLand(self,message):
          self.object.remove=True
          self.room.RemoveController(self.id)
          
     def OnObjectCollision(self,message):
          if message.obj2 != None:
               if message.obj2.type.name=="cannonball":
                    return None
               elif message.obj2.type.name=="player2" or message.obj2.type.name=="player1":
                    ctrl=self.room.GetControllerByObj(message.obj2)
                    if self.phase == 2:
                         ctrl.Hit(3)
                    elif self.phase == 1:
                         ctrl.Hit(1)
                         
                    self.room.particle.AddParticle("circle3",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height/2),-5,-5,3.0,-0.01)
                    self.room.particle.AddParticle("circle3",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height/2),5,-5,3.0,-0.01)
                    self.room.particle.AddParticle("circle3",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height/2),-3,-5,3.0,-0.01)
                    self.room.particle.AddParticle("circle3",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height/2),3,-5,3.0,-0.01) 
                    
          self.object.remove=True
          
          if message.collision_type == COLLISION_WALL and (self.phase==3 or self.phase==4):
               tx=int(self.object.posX/TILEWIDTH)
               ty=int(self.object.posY/TILEHEIGHT)
               startX=SetBound(tx-5,0,self.room.map.width)
               startY=SetBound(ty-5,0,self.room.map.height)
               endX=SetBound(startX+10,0,self.room.map.width)
               endY=SetBound(startY+10,0,self.room.map.height-1)
               
               fill=0
               #for terrashot
               if self.phase==3:
                    fill=1
               #for dynamite
               elif self.phase==4:
                    fill=0
               
               for y in range(startY,endY):
                    for x in range(startX,endX):
                         self.room.map.SetLayer(self.room.map.baseLayer.name, x, y, fill)
                              
               startX=SetBound(startX-1,0,self.room.map.width-1)
               startY=SetBound(startY-1,0,self.room.map.height)
               endX=SetBound(endX+1,0,self.room.map.width-1)
               endY=SetBound(endY+1,0,self.room.map.height-1)
               
               for y in range(startY,endY):
                    for x in range(startX,endX):
                         if self.room.map.base[x][y] != 0:
                              #determine if it is a slope
                              left=self.room.map.base[SetBound(x-1,0,x)][y]
                              right=self.room.map.base[SetBound(x+1,0,self.room.map.width-1)][y]
                              up=self.room.map.base[x][SetBound(y-1,0,y)]
                         
                              if left == 0 and right != 0 and up == 0:
                                   self.room.map.SetLayer(self.room.map.baseLayer.name, x, y, 2)
                              elif left != 0 and right == 0 and up == 0:
                                   self.room.map.SetLayer(self.room.map.baseLayer.name, x, y, 3)
                              else:     
                                   self.room.map.SetLayer(self.room.map.baseLayer.name, x, y, 1)
          
Controller=CannonballController