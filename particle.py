#!/usr/bin/env python

from utilities import *

class ParticleTemplate:
     def __init__(self,name,shape,life=-1,gravity=1.0,fall=True,color=Color(255,255,255,255),decay=Color(0,0,0,0),fill=True):
          self.shape=shape
          self.shape.SetPosition(0,0)
          self.shape.SetRotate(0.0)
          self.shape.SetScale(1.0)
          self.name=name
          self.id=-1
          self.life=life
          self.gravity=1.0
          self.fall=fall
          self.color=color
          self.decay=decay
          self.fill=fill
          
class Particle:
     def __init__(self):
          self.name=""
          self.life=0
          self.gravity=0.0
          self.fall=True
          self.color=Color()
          self.decay=Color()
          self.fill=True
          self.velX=0.0
          self.velY=0.0
          self.velRotate=0.0
          self.velScale=0.0
     

class ParticleEngine:
     def __init__(self):
          self.templateList=[]
          self.particleList=[]
          self.particleIDList=[]
          self.particleID=0
          self.templateIDList=[]
          self.templateID=0
          
     def PopFreeParticleId(self):
          id=-1
          if len(self.particleIDList) == 0:
               id=self.particleID
               self.particleID+=1
          else:
               id=self.particleIDList.pop(0)
               
          return id
          
     def PushFreeParticleId(self,id):
          if self.particleIDList.count(id) > 0:
               self.particleIDList.remove(id)
               
     def PopFreeTemplateId(self):
          id=-1
          if len(self.templateIDList) == 0:
               id=self.templateID
               self.templateID+=1
          else:
               id=self.templateIDList.pop(0)
               
          return id
          
     def PushFreeTemplateId(self,id):
          if self.templateIDList.count(id) > 0:
               self.templateIDList.remove(id)          
     
     def CreateTemplate(self,name,shape,life,gravity=1.0,fall=True,color=Color(255,255,255,255),decay=Color(0,0,0,0),fill=True):
          p=ParticleTemplate(name,shape,life,gravity,fall,color,decay,fill)
          self.AddTemplate(p)
          
     def AddTemplate(self,template):
          template.id=self.PopFreeTemplateId()
          self.templateList.append(template)
          
     def RemoveTemplate(self,name):
          #check if there are particles using this template
          for i in self.particleList:
               if i.name == name:
                    return None
          
          if type(name) == type("abc"):
               if self.TemplateExists(name):
                    self.RemoveTileTemplate(self.GetTemplateIdByName(name))
                    
          else:          
               id=self.GetTemplateIdByName(name)
               self.PushFreeTemplateId(id)
               for i in range(len(self.templateList)):
                    if self.templateList[i].id == id:
                         self.templateList.pop(i)
                         break
     
     def TemplateExists(self,name):
          exist=False
          for i in self.templateList:
               if i.name == name:
                    exist=True
                    break
                    
          return exist
          
     def GetTemplateIdByName(self,name):
          for i in self.templateList:
               if i.name == name:
                    return i.id
                    
          return -1
     
     def GetTemplateByName(self,name):
          for i in self.templateList:
               if i.name == name:
                    return i
                    
          return None
          
     def GetTemplateNameById(self,id):
          for i in self.templateList:
               if i.id == id:
                    return i.name
                    
          return ""
          
     def GetTemplateIndexByName(self,name):
          for i in range(len(self.templateList)):
               if self.templateList[i].name == name:
                    return i
                    
          return -1
          
     def GetTemplateIndexById(self,id):
          for i in range(len(self.templateList)):
               if self.templateList[i].id == id:
                    return i
                    
          return -1
     
     def AddParticle(self,name,posX,posY,velX,velY,velR=0.0,velS=0.0,life=-1,gravity=-1,fall=-1,color=None,decay=None,fill=None):
          if self.TemplateExists(name):
               t=self.GetTemplateByName(name)
               p=Particle()
               p.shape=t.shape.Clone()
               p.name=name
               p.shape.SetPosition(posX,posY)
               p.velX=velX
               p.velY=velY
               p.velRotate=velR
               p.velScale=velS
               p.life=(life if life!=-1 else t.life)
               p.gravity=(gravity if gravity!=-1 else t.gravity)
               p.fall=(fall if fall!=-1 else t.fall)
               p.color=(color if color!=None else t.color)
               p.decay=(decay if decay!=None else t.decay)
               p.decay.a=255/p.life
               p.fill=(fill if fill!=None else t.fill)
               
               self.particleList.append(p)
               
     def RemoveAllParticles(self):
          del self.particleList[:]
          
     def Update(self):
          p=None
          killList=[]
          for i in range(len(self.particleList)):
               p=self.particleList[i]
               p.life-=1
               if p.life <= 0 or p.color.a-p.decay.a <= 0 or p.shape.scale+p.velScale <= 0.0:
                    killList.append(p)
                    
               else:
                    #color decay
                    p.color-=p.decay
                    #velocity
                    if p.fall:
                         p.velY+=p.gravity
                         
                    p.shape.SetPosition(p.shape.posX+p.velX, p.shape.posY+p.velY)
                    #scale and rotation
                    p.shape.SetRotate(p.shape.rotate+p.velRotate)
                    p.shape.SetScale(p.shape.scale+p.velScale)
                    
          for i in killList:
               self.particleList.remove(i)
                    
                    
          
          
          