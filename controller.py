#!/usr/bin/env python

import main
import room
from message import *
from message_class import *

class Controller:
     def __init__(self,args):
          self.id=0
          self.priority=0
          self.room=args[0]
          self.object=args[1]
          
     def Update(self,args):
          pass     
          
     def OnMessage(self,message):
          pass

class PersonController(Controller):
     def __init__(self,args):
          Controller.__init__(self,args)
          self.object.AddSubscriber(self,OBJECT)
          
     def Update(self,args):
          pass
     
     def OnObjectDestroy(self,message):
          self.room.RemoveController(self.id)
     
     def OnMessage(self,message):
          pass
               
     def OnKeyDown(self,message):
          pass
                    
     def OnObjectMove(self,message):
          pass
         
     def OnObjectFall(self,message):
          pass
         
     def OnObjectJump(self,message):
          pass
          
     def OnObjectLand(self,message):
          pass
     
     def OnObjectCollision(self,message):
          pass
          
     def OnAlarm(self,message):
          pass
          
class PlayerController(PersonController):
     def __init__(self,args): 
          PersonController.__init__(self,args)
          self.LEFT=K_LEFT
          self.RIGHT=K_RIGHT
          self.UP=K_UP
          self.DOWN=K_DOWN
          self.JUMP=K_SPACE
          self.object.data["angle"]=0
          self.object.data["power"]=100
          del self.object.data["seeker"]
          self.object.data["fireball"]=0
          self.object.data["terra"]=0
          self.object.data["dynamite"]=0
          self.object.data["spreadshot"]=0
          self.object.data["spreadfire"]=0
          self.object.data["score"]=100
          self.object.data["move"]=200

     def Hit(self,damage=1):
          self.object.data["current_hp"]=SetBound(self.object.data["current_hp"]-damage,0,self.object.data["current_hp"]-damage)
          if self.object.data["current_hp"] <= 0:
               self.object.BroadcastMessage(PlayerMessage(self.object,PLAYER_DIED))
          else:
               self.object.BroadcastMessage(PlayerMessage(self.object,PLAYER_HIT))
     
     def Score(self,points):  
          self.object.data["score"]=self.object.data["score"]+points
          self.object.BroadcastMessage(PlayerMessage(self.object,PLAYER_SCORED))
     
     def Update(self,args):
          key=pygame.key.get_pressed()
          
          if self.object.disabled == False:
               if key[self.LEFT]:
                    self.object.GenerateAction(LEFT)
                    self.object.sprite.Resume()
                    self.object.sprite.SetAnimation(0)
                    self.room.particle.AddParticle("circle",self.object.posX+self.object.width,self.object.posY+(self.object.height/2),0,0,3.0,0.0)
               elif key[self.RIGHT]:
                    self.object.GenerateAction(RIGHT)
                    self.object.sprite.Resume()
                    self.object.sprite.SetAnimation(1)
                    self.room.particle.AddParticle("circle",self.object.posX,self.object.posY+(self.object.height/2),0,0,3.0,0.0)
               else:
                    self.object.sprite.Pause()
               
               if key[self.UP]:
                    self.object.GenerateAction(UP)
               if key[self.DOWN]:
                    self.object.GenerateAction(DOWN)
               
               if key[self.JUMP]:
                    self.object.GenerateAction(JUMP)
                    if key[self.LEFT] == False and key[self.RIGHT] == False:
                         self.room.particle.AddParticle("circle",self.object.posX+(self.object.width/2),self.object.posY+(self.object.height),0,0,3.0,0.0)
     
     def OnAlarm(self,message):
          pass
     
     def OnMessage(self,message):
          if message.type == INPUT_KEYDOWN:
               pass
     
     """
     def OnKeyDown(self,message):
          if message.type == INPUT_KEYDOWN:
               if message.event.key == K_LEFT:
                    self.object.GenerateAction(LEFT)
               if message.event.key == K_RIGHT:
                    self.object.GenerateAction(RIGHT)
               if message.event.key == K_UP:
                    self.object.GenerateAction(UP)
               if message.event.key == K_DOWN:
                    self.object.GenerateAction(DOWN)
               if message.event.key == K_SPACE:
                    self.object.GenerateAction(JUMP)
     """
     
