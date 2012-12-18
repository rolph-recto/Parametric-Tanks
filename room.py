#!/usr/bin/env python

from main import *
from object import *
from objType import *
from controller import *
from map import *
from message import *
from message_class import *
from particle import *

#database structures
OBJTYPE="OBJTYPE"
CONTROLLER="CONTROLLER"
SOUND="SOUND"
MUSIC="MUSIC"
SPRITE="SPRITE"
TILESET="TILESET"
TILETEMPLATE="TILETEMPLATE"
IMAGE="IMAGE"

class RoomDatabase:
     def __init__(self):
          self.database={}
          self.database[OBJTYPE]={}
          self.database[CONTROLLER]={}
          self.database[SOUND]={}
          self.database[MUSIC]={}
          self.database[SPRITE]={}
          self.database[TILESET]={}
          self.database[TILETEMPLATE]={}
          self.database[IMAGE]={}
     
     def __getitem__(self,key):
          if key == OBJTYPE or key == CONTROLLER or key == SOUND or key == MUSIC or key == SPRITE or key == TILESET or key == TILETEMPLATE or key == IMAGE:
               return self.database[key]
     
     def __setitem__(self,key):
          pass
     
     def IsTypeValid(self,type):
          if type == OBJTYPE or type == CONTROLLER or type == SOUND or type == MUSIC or type == SPRITE or type == TILESET or type == TILETEMPLATE or type == IMAGE:
               return True
          
          return False
     
     def ItemExists(self,type,name):
          if self.IsTypeValid(type):
               if self.database[type].has_key(name):
                    return True
          
          return False
     
     def Add(self,type,name,data):
          if self.IsTypeValid(type):
               self.database[type][name]=data
               
     def Remove(self,type,name,data):
          if self.IsTypeValid(type):
               if self.database[type].has_key(name):
                    del self.database[type][name]
                    
     def LoadXML(self,file):
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
          doc=xml.dom.minidom.parseString(f.read()).documentElement
          resourceList=doc.getElementsByTagName("resource")
          for i in resourceList:
               name=i.getAttribute("name")
               resourcetype=i.getAttribute("type").upper()
               group=i.getAttribute("group")
               file=i.getAttribute("file")
               tempPath=i.getAttribute("path")
               path=""
               
               if tempPath == "abs":
                    path=file
               else:
                    if group == "":
                         path=os.path.join(RESOURCEDIR,resourcetype.lower(),file)
                    else:
                         path=os.path.join(RESOURCEDIR,resourcetype.lower(),group,file)
               
               #Convert unicode to string
               path=str(path)
               
               if resourcetype == OBJTYPE:
                    objtype=ObjectType(name)
                    objtype.Load(path)
                    self.Add(OBJTYPE, name, objtype)
               elif resourcetype == CONTROLLER:     
                    f=open(path)
                    i=os.path.basename(path)
                    mod=imp.load_module(i.split('.')[0], f, i, (i.split('.')[1],"r",imp.PY_SOURCE) )
                    self.Add(CONTROLLER, name, mod)
               elif resourcetype == SOUND:
                    sound=pygame.mixer.Sound(path)
                    self.Add(SOUND, name, sound)
               elif resourcetype == MUSIC:
                    self.Add(MUSIC, name, path)
               elif resourcetype == SPRITE:
                    spr=Sprite()
                    spr.Load(path)
                    self.Add(SPRITE, name, spr)
               elif resourcetype == TILESET:
                    tile=Tileset()
                    tile.Load(path)
                    self.Add(TILESET, name, tile)
               elif resourcetype == TILETEMPLATE:
                    tiletemplate=dict()
                    tiletemplate["tileset"]=Tileset()
                    tiletemplate["tilelist"]=[]
                    f=None
                    #if file is a string
                    if type(path) == type("abc"):
                         f=open(path,"rb")
          
                    #file is a file object
                    else:
                         f=path
               
                    if f == None:
                         return None

                    #commence reading
                    tiletemplate["tileset"].Load(f)
                    n=load(f)
                    for i in range(n):
                         tile=TileTemplate("")
                         tile.Load(f)
                         tiletemplate["tilelist"].append(tile)
               
                    #if file is a string, close file object
                    if type(file) == type("abc"):
                         f.close()
                    
                    self.Add(TILETEMPLATE, name, tiletemplate)
                    
               elif resourcetype == IMAGE:
                    img=pygame.image.load(path)
                    self.Add(IMAGE, name, img)
                    
                    
class Room(Dispatcher):
     def __init__(self):
          Dispatcher.__init__(self)
          #map
          self.map=MapData()
          #object
          self.objList=[]
          self.objMap=[]
          self.dynObjList=[]
          self.platformList=[]
          #object ids
          self.objIDList=[]
          self.objID=0
          #controller
          self.controllerList=[]
          #controller ids
          self.controllerIDList=[]
          self.controllerID=0
          self.database=RoomDatabase()
          #alarms
          self.alarmList=[]
          self.alarmIDList=[]
          self.alarmID=0
          #gravity
          self.gravity=0.5
          #particle engine
          self.particle=ParticleEngine()
          self.key=None
          self.mouse=None
          self.player=None
          self.editor=False
          
     def PopFreeObjectId(self):
          id=0
          if len(self.objIDList) == 0:
               id=self.objID
               self.objID+=1
          else:
               id=self.objIDList.pop(0)
               
          return id
          
     def PushFreeObjectId(self,id):
          if self.objIDList.count(id) > 0:
               self.objIDList.remove(id)
               
     def PopFreeControllerId(self):
          id=0
          if len(self.controllerIDList) == 0:
               id=self.controllerID
               self.controllerID+=1
          else:
               id=self.controllerIDList.pop(0)
               
          return id
          
     def PushFreeControllerId(self,id):
          if self.controllerIDList.count(id) > 0:
               self.controllerIDList.remove(id)

     def IsControllerIdValid(self,id):
          if id <= self.controllerID and self.controllerIDList.count(id) == 0:
               return True
               
          return False
          
     def GetControllerById(self,id):
          for i in self.controllerList:
               if i.id == id:
                    return i
                    
          return None
     
     def GetControllerByObj(self,obj):
          for i in self.controllerList:
               if i.object == obj:
                    return i
                    
          return None	
     
     def IsPositionValid(self,posx,posy):
          pass
          
     def IsObjectIdValid(self,id):
          if id <= self.objID and self.objIDList.count(id) == 0:
               return True
               
          return False
          
     def GetObjectById(self,id):
          for i in self.objList:
               if i.id == id:
                    return i
                    
          return None
          
     def GetObjectNameById(self,id):
          for i in self.objList:
               if i.id == id:
                    return i.name
                    
          return ""
     
     def GetObjectByPos(self,x,y):
          objRect=Rectangle()
          for i in self.objList:
               objRect.x=i.posX
               objRect.y=i.posY
               objRect.w=i.width
               objRect.h=i.height
               if objRect.isPointInRect(x,y):
                    return i
               
          return None
     
     def GetObjectByName(self,name):
          if name == "": return None
          
          for i in self.objList:
               if i.name == name:
                    return i
               
          return None
          
     def GetObjectIdByName(self,name):
          if name == "": return None
          
          for i in self.objList:
               if i.name == name:
                    return i.id
               
          return -1
     
     def GetObjectIndexById(self,id):
          for i in range(0,len(self.objList)):
               if self.objList[i].id == id:
                    return i
               
          return -1
          
     def GetObject(self,id):
          if type(id) == type(1):
               return self.GetObjectById(id)
          else:
               return id
     
     def ValidateObject(self,otype,posx,posy):
          #check if type is valid
          if type(otype) == type("abc"):
               if self.database[OBJTYPE].has_key(otype) == False:
                    return False
     
     def InsertObject(self,obj):
          obj.id=self.PopFreeObjectId()
          
          self.objList.append(obj)
          self.AddObjectToMap(obj.id)
          if obj.group != PLATFORM:
               self.dynObjList.append(obj)
          else:
               self.platformList.append(obj)
               
     
     def AddObject(self,otype,posx=0,posy=0,name="",args=()):
          if self.ValidateObject(otype,posx,posy) == False:
               return None
          
          if type(otype) == type("abc"):
               obj=Object(self.database[OBJTYPE][otype])
          else:
               obj=Object(otype)
               
          obj.posX=posx
          obj.posY=posy
          obj.name=name
          
          self.InsertObject(obj)
          self.BroadcastMessage(ObjectMessage(obj,OBJECT_CREATED))
          
          #create controller
          ctrl=None
          if self.GetController(obj.type.controller) != None and self.editor==False:
               ctrl=self.AddController(obj.type.controller,0,(self,obj,args))
               
          obj.ctrl=ctrl
               
          return obj.id
          
     def RemoveObject(self,id):
          if self.IsObjectIdValid(id):
               obj=self.GetObjectById(id)
               self.BroadcastMessage(ObjectMessage(obj,OBJECT_DESTROYED))
               obj.BroadcastMessage(ObjectMessage(obj,OBJECT_DESTROYED))
               index=-1
               for i in range(len(self.objList)):
                    if self.objList[i].id==obj.id:
                         index=i
                         
               if index >= 0:
                    self.objList.pop(index)
                    
               self.objMap.remove(obj.id)
               self.PushFreeObjectId(obj.id)
               if self.platformList.count(obj) > 0:
                    self.platformList.remove(obj)
               if self.dynObjList.count(obj) > 0:
                    self.dynObjList.remove(obj)
               if obj==self.player:
                    self.player=None
               
     def RemoveAllObjects(self):
          for obj in self.objList:
               self.BroadcastMessage(ObjectMessage(obj,OBJECT_DESTROYED))
               obj.BroadcastMessage(ObjectMessage(obj,OBJECT_DESTROYED))
               
          del self.objList[:]
          del self.objIDList[:]
          del self.objMap[:]
          del self.dynObjList[:]
          del self.platformList[:]
          self.player=None
          #self.objList=[]
          #self.objIDList=[]
          #self.objMap=[]
          self.objID=0
     
     def AddObjectToMap(self,id):
          #sort objects based on x position
          if self.IsObjectIdValid(id):
               obj=self.GetObjectById(id)
               n=len(self.objMap)
               insert=True
               if n < 1:
                    self.objMap.append(obj.id)
                    return
               
               off=0
               index=int(floor(n/2))+off
               objIndex=self.GetObjectById(self.objMap[index])
               while n > 1:
                    objIndex=self.GetObjectById(self.objMap[index])
                    if obj.posX < objIndex.posX:
                         n=index-off
                         index=SetBound(int(floor(n/2))+off,0,len(self.objMap)-1)
                    elif obj.posX == objIndex.posX:
                         self.objMap.insert(index,obj.id)
                         insert=False
                         break
                    else:
                         n=len(self.objMap[index+1:off+n-1])
                         off=index+1
                         index=SetBound(int(floor(n/2))+off,0,len(self.objMap)-1)
               
               if insert:
                    objIndex=self.GetObjectById(self.objMap[index])
                    if obj.posX < objIndex.posX:
                         self.objMap.insert(index,obj.id)
                    
                    else:
                         if index+1 <= len(self.objMap):
                              self.objMap.insert(index+1,obj.id)
                         else:
                              self.objMap.append(obj.id)
                         
     def RemoveObjectFromMap(self,id):
          if self.IsObjectIdValid(id):
               if self.objMap.count(id) > 0:
                    self.objMap.remove(id)
               
     def MoveObjectIndex(self,id,index):
          if self.IsObjectIdValid(id) and index>=0 and index<=len(self.objList):
               obj=self.GetObject(id)
               self.objList.remove(obj)
               self.objList.insert(index,obj)
     
     def InsertController(self,ctrl):
          insert=False
          for i in range(len(self.controllerList)):
               if ctrl.priority > self.controllerList[i].priority:
                    self.controllerList.insert(i,ctrl)
                    insert=True
                    break
                    
          if insert == False:
               self.controllerList.append(ctrl)     
     
     def GetController(self,ctype):
          if type(ctype) == type("abc"):
               if self.database[CONTROLLER].has_key(ctype):
                    return self.database[CONTROLLER][ctype].Controller
               elif ctype == "PlayerController" or ctype == "player":
                    return PlayerController
               else:
                    return Controller
          elif isinstance(ctype,Controller):
               return ctype
          else:
               return None
     
     def AddController(self,ctype,priority=0,args=None):
          ctrl=None
          ctrl=self.GetController(ctype)(args)
               
          ctrl.id=self.PopFreeControllerId()
          ctrl.priority=priority
          self.InsertController(ctrl)
          self.BroadcastMessage(ControllerMessage(ctrl,CONTROLLER_CREATED))
          
          if ctrl != None:
               return ctrl.id
          else:
               return 0
          
     def RemoveController(self,id):
          if self.IsControllerIdValid(id):
               ctrl=self.GetControllerById(id)
               self.BroadcastMessage(ControllerMessage(ctrl,CONTROLLER_DESTROYED))
               if self.controllerList.count(ctrl) > 0:
                    self.controllerList.remove(ctrl)
               
     def RemoveAllControllers(self):
          del self.controllerList[:]
          del self.controllerIDList[:]
          #self.controllerList=[]
          #self.controllerIDList=[]
          self.controllerID=0
               
     def SetControllerPriority(self,id,priority):
          if self.IsControllerIdValid(id):
               ctrl=self.GetControllerById(id)
               self.RemoveController(id)
               ctrl.priority=priority
               self.InsertController(ctrl)
               
     def UpdateControllers(self,args=None):
          args=(self,)
          for i in self.controllerList[:]:
               i.Update(args)
               
     def MoveObject(self,obj,velx,vely,object=True):
          r=self.CollisionData(obj,velx,vely,object)
          o1=r["obj"]
          thud=False
          wallthud=False
                    
          if velx < 0:
               if r["upLeft"] and r["centerLeft"] and r["downLeft"]:
                    """
                    if obj.posX+velx<0:
                         obj.posX=0
                         obj.velX=0.0
                    else:
                         obj.posX=obj.posX+velx
                    """
                    if obj.posX+velx < 0:
                         wallthud=True
                         
                    obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
               else:
                    deaccel=False
                    if r["obj"] == None:
                         obj.posX=int(SetBound(r["centerX"]*TILEWIDTH,0,self.map.width*TILEWIDTH-obj.width))
                         deaccel=True
                         wallthud=True
                    elif r["obj"].collision == SOLID and obj.collision != GHOST:
                         if obj.group != PLATFORM:
                              obj.posX=int(SetBound(r["obj"].posX+r["obj"].width,0,self.map.width*TILEWIDTH-obj.width))
                              thud=True
                              deaccel=True
                         else:
                              obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
                              self.MoveObject(r["obj"], -(r["obj"].posX+r["obj"].width-obj.posX), 0)
                              if obj.posX <= r["obj"].posX+r["obj"].width:
                                   obj.posX=r["obj"].posX+r["obj"].width
                    elif r["obj"].collision == PUSHABLE  and obj.collision != GHOST:
                         obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
                         self.MoveObject(r["obj"], -(r["obj"].posX+r["obj"].width-obj.posX), 0)
                         if obj.posX <= r["obj"].posX+r["obj"].width:
                              obj.posX=r["obj"].posX+r["obj"].width
                    else:
                         if r["upLeftTile"] and ~r["centerLeftTile"] and r["downLeftTile"]:
                              obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
                         else:
                              obj.posX=int(SetBound(r["centerX"]*TILEWIDTH,0,self.map.width*TILEWIDTH-obj.width))
                              deaccel=True
                              wallthud=True
                              
                                   
                    if deaccel: obj.velX=int(abs(floor( float(obj.velX)*float(obj.bounceX) )))
                    
          elif velx > 0:
               if r["upRight"] and r["centerRight"] and r["downRight"]:
                    """
                    if obj.posX+velx>self.map.width*TILEWIDTH-obj.width:
                         obj.posX=self.map.width*TILEWIDTH-obj.width
                         obj.velX=0.0
                    else:
                         obj.posX=obj.posX+velx
                    """
                    if obj.posX+velx > (self.map.width*TILEWIDTH)-obj.width:
                         wallthud=True
                         
                    obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
               else:
                    deaccel=False
                    if r["obj"] == None:
                         obj.posX=int(SetBound(r["leftX"]*TILEWIDTH,0,(self.map.width*TILEWIDTH)-obj.width))
                         deaccel=True
                         wallthud=True
                    elif r["obj"].collision == SOLID and obj.collision != GHOST:
                         if obj.group != PLATFORM:
                              obj.posX=int(SetBound(r["obj"].posX-obj.width,0,self.map.width*TILEWIDTH-obj.width))
                              thud=True
                              deaccel=True
                         else:
                              obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
                              self.MoveObject(r["obj"], (obj.posX+obj.width-r["obj"].posX), 0)
                              if obj.posX+obj.width >= r["obj"].posX:
                                   obj.posX=int(SetBound(r["obj"].posX-obj.width,0,self.map.width*TILEWIDTH-obj.width))
                    elif r["obj"].collision == PUSHABLE and obj.collision != GHOST:
                         obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
                         self.MoveObject(r["obj"], (obj.posX+obj.width-r["obj"].posX), 0)
                         if obj.posX+obj.width >= r["obj"].posX:
                              obj.posX=int(SetBound(r["obj"].posX-obj.width,0,self.map.width*TILEWIDTH-obj.width))  
                    else:
                         if r["upRightTile"] and r["centerRightTile"] and r["downRightTile"]:
                              obj.posX=int(SetBound(obj.posX+velx,0,(self.map.width*TILEWIDTH)-obj.width))
                         else:
                              obj.posX=int(SetBound(r["leftX"]*TILEWIDTH,0,(self.map.width*TILEWIDTH)-obj.width))
                              deaccel=True
                              wallthud=True
                         
                    if deaccel: obj.velX=int(-abs(floor( float(obj.velX)*float(obj.bounceX) )))
                    
          if thud and o1 != None:
               obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(o1,COLLISION_THUD)) )
               o1.BroadcastMessage( ObjectMessage(o1,OBJECT_COLLISION,(obj,COLLISION_THUD)) )

          #r=self.CollisionData(obj,0.0,vely,object)
          o2=r["obj"]
          thud=False
          if vely < 0:
               if r["upLeft"] and r["upCenter"] and r["upRight"]:
                    """
                    if obj.posY+vely<0:
                         obj.posY=0
                         obj.velY=0.0
                    else:
                         obj.posY=obj.posY+vely
                    """
                    if obj.posY+vely < 0:
                         wallthud=True
                         
                    obj.posY=int(SetBound(obj.posY+vely,0,(self.map.height*TILEHEIGHT)-obj.height))
               else:
                    deaccel=False
                    if r["obj"] == None:
                         obj.posY=r["centerY"]*TILEHEIGHT
                         deaccel=True
                         wallthud=True
                    elif r["obj"].collision == SOLID and obj.collision != GHOST:
                         if obj.group != PLATFORM:
                              thud=True
                              deaccel=True
                              if r["obj"].group == PLATFORM and obj.posY+obj.height<=r["obj"].posY:
                                   obj.platform=r["obj"].id
                              else:
                                   obj.posY=int(SetBound(r["obj"].posY+r["obj"].height,0,self.map.height*TILEHEIGHT-obj.height))
                         elif r["upLeftTile"] and r["upCenterTile"] and r["upRightTile"]:
                              obj.posY=int(SetBound(obj.posY+vely,0,(self.map.height*TILEHEIGHT)-obj.height))
                              r["obj"].platform=obj.id
                              o2y1=r["obj"].posY
                              self.MoveObject(r["obj"], 0, -(r["obj"].posY+r["obj"].height-obj.posY))
                              if obj.posY <= r["obj"].posY+r["obj"].height:
                                   obj.posY=r["obj"].posY+r["obj"].height
                                   if o2y1 == r["obj"].posY:
                                        obj.velY=0.0
                         else:
                              obj.posY=r["downY"]*TILEHEIGHT
                              deaccel=True
                    else:
                         if r["upLeftTile"] and r["upCenterTile"] and r["upRightTile"]:
                              obj.posY=int(SetBound(obj.posY+vely,0,(self.map.height*TILEHEIGHT)-obj.height))
                         else:
                              obj.posY=r["centerY"]*TILEHEIGHT
                              deaccel=True
                              wallthud=True
                         
                    
                    if deaccel:
                         obj.velY=0.0
                         obj.jump=False
                    #obj.jumpSpeed=0.0
                    
          elif vely > 0:
               if r["downLeft"] and r["downCenter"] and r["downRight"]:
                    """
                    if obj.posY+vely>self.map.height*TILEHEIGHT-obj.height:
                         obj.posY=self.map.height*TILEHEIGHT-obj.height
                         obj.velY=0.0
                    else:
                         obj.posY=obj.posY+vely
                    """
                    if obj.posY+vely > (self.map.height*TILEHEIGHT)-obj.height:
                         wallthud=True
                    
                    obj.posY=int(SetBound(obj.posY+vely,0,(self.map.height*TILEHEIGHT)-obj.height))
               else:
                    deaccel=False
                    if r["obj"] == None:
                         if obj.height < TILEHEIGHT:
                              obj.posY=int(r["centerY"]*TILEHEIGHT)+(TILEHEIGHT-obj.height)
                         else:
                              obj.posY=int(r["centerY"]*TILEHEIGHT)
                         deaccel=True
                         wallthud=True
                         obj.platform=None
                    elif r["obj"].collision == SOLID and obj.collision != GHOST:
                         if obj.group != PLATFORM:
                              thud=True
                              deaccel=True
                              if r["obj"].group == PLATFORM and obj.posY+obj.height<=r["obj"].posY:
                                   obj.platform=r["obj"].id
                              else:
                                   obj.posY=int(SetBound(r["obj"].posY-obj.height,0,self.map.height*TILEHEIGHT-obj.height))
                                   deaccel=True
                                   
                         else:
                              #move objects above to go down with platform
                              obj.posY=int(SetBound(obj.posY+vely,0,(self.map.height*TILEHEIGHT)-obj.height))
                              if r["obj"].posY+r["obj"].height<=obj.posY:
                                   r["obj"].platform=obj.id
                              self.MoveObject(r["obj"], 0, (obj.posY+obj.height-r["obj"].posY))
                              if obj.posY+obj.height >= r["obj"].posY:
                                   obj.posY=r["obj"].posY-obj.height
                                   obj.velY=0.0
                    else:
                         if r["downLeftTile"] and r["downCenterTile"] and r["downRightTile"]:
                              obj.posY=int(SetBound(obj.posY+vely,0,(self.map.height*TILEHEIGHT)-obj.height))
                         else:
                              if obj.height < TILEHEIGHT:
                                   obj.posY=int(r["centerY"]*TILEHEIGHT)+(TILEHEIGHT-obj.height)
                              else:
                                   obj.posY=int(r["centerY"]*TILEHEIGHT)
                              deaccel=True
                              wallthud=True
                         
                    if deaccel: obj.velY=int(-floor( float(obj.velY)*float(obj.bounceY) ))
                    if obj.velY == 0.0:
                         obj.jump=False
                         obj.BroadcastMessage(ObjectMessage(obj,OBJECT_LANDED))
                    #obj.jumpSpeed=0.0
                    
          if thud and o1 != None and o2 != None:
               if o1 != o2:
                    obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(o1,COLLISION_THUD)) )
                    o1.BroadcastMessage( ObjectMessage(o1,OBJECT_COLLISION,(obj,COLLISION_THUD)) )
               
          if wallthud:
               obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(None,COLLISION_WALL)) )
          
     def MoveObjectToPos(self,id,xpos,ypos):
          if self.IsObjectIdValid(id):
               obj=self.GetObjectById(id)
               obj.posX=SetBound(xpos,0,(self.map.width*TILEWIDTH)-obj.width)
               obj.posY=SetBound(ypos,0,(self.map.height*TILEHEIGHT)-obj.height)

     def RaycastPoint(self,id,velx,vely):
          obj=self.GetObject(id)
          addx, addy=0, 0
          x, y=obj.posX, obj.posY
          
          if velx+vely == 0.0:
               return Point(x,y)
               
          else:
               r=BrensenhamLine( Point(x, y), Point(x+velx, y+vely) )
               for i in r:
                    i.x=SetBound(i.x,0,self.map.width*TILEWIDTH)
                    i.y=SetBound(i.y,0,self.map.height*TILEHEIGHT)
                    
                    tile=self.map.base[ int(float(i.x+addx)/float(TILEWIDTH)) ][ int(float(i.y+addy)/float(TILEHEIGHT)) ]
                    tileIndex=self.map.tileIndexList[tile]
                    if self.map.tileList[ tileIndex ].walkable == False:
                         return Point(i.x, i.y)
               
               return Point(x+velx, y+vely)
          
     
     def CollisionData(self,id,velx,vely,col=True):
          r={}
          obj=self.GetObject(id)
          a=Point(obj.posX+velx,obj.posY+vely)

          r["centerX"]=SetBound( int(floor( (float(a.x)+float(obj.width/2))/float(TILEWIDTH) )), 0, self.map.width-1)
          r["centerY"]=SetBound( int(floor( (float(a.y)+float(obj.height/2))/float(TILEHEIGHT) )), 0, self.map.height-1)
          r["leftX"]=SetBound( int( floor( float(a.x)/float(TILEWIDTH) ) ), 0, self.map.width-1)
          r["upY"]=SetBound( int( floor( float(a.y)/float(TILEHEIGHT) ) ), 0, self.map.height-1)
          r["rightX"]=SetBound( int( floor( (float(obj.width-1+a.x)/float(TILEWIDTH) ) ) ), 0, self.map.width-1 )
          r["downY"]=SetBound( int( floor( (float(obj.height-1+a.y)/float(TILEHEIGHT) ) ) ), 0, self.map.height-1 )
          
          r["centerLeft"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["leftX"]][r["centerY"]]] ].walkable
          r["centerLeftTile"]=r["centerLeft"]
          r["centerRight"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["rightX"]][r["centerY"]]] ].walkable 
          r["centerRightTile"]=r["centerRight"]
          r["upCenter"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["centerX"]][r["upY"]]] ].walkable
          r["upCenterTile"]=r["upCenter"]
          r["downCenter"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["centerX"]][r["downY"]]] ].walkable
          r["downCenterTile"]=r["downCenter"]
          r["upLeft"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["leftX"]][r["upY"]]] ].walkable
          r["upLeftTile"]=r["upLeft"]
          r["upRight"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["rightX"]][r["upY"]]] ].walkable
          r["upRightTile"]=r["upRight"]
          r["downLeft"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["leftX"]][r["downY"]]] ].walkable
          r["downLeftTile"]=r["downLeft"]
          r["downRight"]=self.map.tileList[ self.map.tileIndexList[self.map.base[r["rightX"]][r["downY"]]] ].walkable
          r["downRightTile"]=r["downRight"]
          r["obj"]=None
          
          if col:
               #check object collisions
               objRect=Rectangle(int(obj.posX+velx), int(obj.posY+vely), obj.width, obj.height)
               iterRect=Rectangle(objRect)
               iterID=self.objMap.index(obj.id)
               objc=None
               obj2=self.GetObjectById(self.objMap[iterID])
               #go backwards first
               #while obj2.posX+obj2.width<=obj.posX+obj.width and obj2.posX+obj2.width>=obj.posX:
               while True:
                    iterID=iterID-1
                    if iterID < 0: break
                    obj2=self.GetObjectById(self.objMap[iterID])
                    iterRect=Rectangle(obj2.posX, obj2.posY, obj2.width, obj2.height)
                    if objRect.isIntersecting(iterRect) and obj2 != obj:
                         objc=obj2
                         break
                    
               iterID=self.objMap.index(obj.id)
               obj2=self.GetObjectById(self.objMap[iterID])
               #then forwards
               #while obj2.posX>=obj.posX and obj2.posX<=obj.posX+obj.width:
               while True:
                    iterID=iterID+1
                    if iterID >= len(self.objMap): break
                    obj2=self.GetObjectById(self.objMap[iterID])
                    iterRect=Rectangle(obj2.posX, obj2.posY, obj2.width, obj2.height)
                    if objRect.isIntersecting(iterRect) and obj2 != obj:
                         objc=obj2
                         break
          
               #generate response to collision
               if objc != None:
                    iterRect=Rectangle(objc.posX, objc.posY, objc.width, objc.height)
                    if objc.collision == SOLID or objc.collision == PUSHABLE:
                         r["centerLeft"]=iterRect.isPointInRect(obj.posX+velx, obj.posY+int(obj.height/2)+vely) == False
                         r["centerRight"]=iterRect.isPointInRect(obj.posX+obj.width+velx, obj.posY+int(obj.height/2)+vely) == False
                         r["downCenter"]=iterRect.isPointInRect(obj.posX+int(obj.width/2)+velx,obj.posY+obj.height+vely) == False
                         r["upCenter"]=iterRect.isPointInRect(obj.posX+int(obj.width/2)+velx,obj.posY+vely) == False
                         r["upLeft"]=iterRect.isPointInRect(obj.posX+velx, obj.posY+vely) == False
                         r["upRight"]=iterRect.isPointInRect(obj.posX+obj.width+velx, obj.posY+vely) == False
                         r["downLeft"]=iterRect.isPointInRect(obj.posX+velx, obj.posY+obj.height+vely) == False
                         r["downRight"]=iterRect.isPointInRect(obj.posX+obj.width+velx, obj.posY+obj.height+vely) == False
                    
                    r["obj"]=objc
          
          return r
          
     def ObjectCollisionData(self,id,velx,vely,):
               r={}
               obj=self.GetObject(id)
               r["centerLeft"]=True
               r["centerRight"]=True
               r["downCenter"]=True
               r["upCenter"]=True
               r["upLeft"]=True
               r["upRight"]=True
               r["downLeft"]=True
               r["downRight"]=True
               r["obj"]=None
               #check object collisions
               objRect=Rectangle(int(obj.posX+velx), int(obj.posY+vely), obj.width, obj.height)
               iterRect=Rectangle(objRect)
               iterID=self.objMap.index(obj.id)
               objc=None
               obj2=self.GetObjectById(self.objMap[iterID])
               #go backwards first
               #while obj2.posX+obj2.width<=obj.posX+obj.width and obj2.posX+obj2.width>=obj.posX:
               while True:
                    iterID=iterID-1
                    if iterID < 0: break
                    obj2=self.GetObjectById(self.objMap[iterID])
                    iterRect=Rectangle(obj2.posX, obj2.posY, obj2.width, obj2.height)
                    if objRect.isIntersecting(iterRect) and obj2 != obj:
                         objc=obj2
                         break
                    
               iterID=self.objMap.index(obj.id)
               obj2=self.GetObjectById(self.objMap[iterID])
               #then forwards
               #while obj2.posX>=obj.posX and obj2.posX<=obj.posX+obj.width:
               while True:
                    iterID=iterID+1
                    if iterID >= len(self.objMap): break
                    obj2=self.GetObjectById(self.objMap[iterID])
                    iterRect=Rectangle(obj2.posX, obj2.posY, obj2.width, obj2.height)
                    if objRect.isIntersecting(iterRect) and obj2 != obj:
                         objc=obj2
                         break
          
               #generate response to collision
               if objc != None:
                    iterRect=Rectangle(objc.posX, objc.posY, objc.width, objc.height)
                    if objc.collision == SOLID or objc.collision == PUSHABLE:
                         r["centerLeft"]=iterRect.isPointInRect(obj.posX+velx, obj.posY+int(obj.height/2)+vely) == False
                         r["centerRight"]=iterRect.isPointInRect(obj.posX+obj.width+velx, obj.posY+int(obj.height/2)+vely) == False
                         r["downCenter"]=iterRect.isPointInRect(obj.posX+int(obj.width/2)+velx,obj.posY+obj.height+vely) == False
                         r["upCenter"]=iterRect.isPointInRect(obj.posX+int(obj.width/2)+velx,obj.posY+vely) == False
                         r["upLeft"]=iterRect.isPointInRect(obj.posX+velx, obj.posY+vely) == False
                         r["upRight"]=iterRect.isPointInRect(obj.posX+obj.width+velx, obj.posY+vely) == False
                         r["downLeft"]=iterRect.isPointInRect(obj.posX+velx, obj.posY+obj.height+vely) == False
                         r["downRight"]=iterRect.isPointInRect(obj.posX+obj.width+velx, obj.posY+obj.height+vely) == False
                    
                    r["obj"]=objc
                    
               return r
     
     def LogicObject(self,obj):
               #little hack to update old positions to current frame *before calculation*
               obj.posX=obj.posX
               obj.posY=obj.posY
               moved=False
               
               if obj.action[LEFT] or obj.action[RIGHT] or obj.action[UP] or obj.action[DOWN] or obj.action[JUMP] \
               or obj.velX != 0.0 or obj.velY != 0.0:
                    moved=True
             
               #if object is on platform, move obj accordingly
               if obj.platform != None:
                    platform=self.GetObjectById(obj.platform)
                    self.MoveObject(obj, platform.velX, -(obj.posY+obj.height-platform.posY))
                    moved=True
                    self.RemoveObjectFromMap(obj.id)
                    self.AddObjectToMap(obj.id)
                    
               platformY=obj.posY
               objfall=-1
               if obj.fall:
                    objfall=self.Fall(obj)
                    if objfall==Room.OBJFALL:
                         moved=True
               
               if obj.jump: moved=True
               
               if moved:
                    r=self.CollisionData(obj,0.0,1.0,True)
                    centerX=SetBound( int(floor( (float(obj.posX)+float(obj.width/2))/float(TILEWIDTH) )), 0, self.map.width-1)
                    downY=SetBound( int( floor( (float(obj.height-1+obj.posY+1)/float(TILEHEIGHT) ) ) ), 0, self.map.height-1 )
                    
                    friction=self.map.tileList[ self.map.tileIndexList[self.map.base[centerX][downY]] ].friction
                    fwalk=self.map.tileList[ self.map.tileIndexList[self.map.base[centerX][downY]] ].walkable
                    if objfall==Room.OBJCOLLIDE: friction=1.0
               
                    accel=obj.accelX
                    #if friction > 0.0 and friction < accel:
                         #accel=friction
               
                    if obj.action[LEFT]:
                         if obj.velX > 0.0 and friction >= 0.0:
                              accel*=friction
                         
                         obj.velX=SetBound(obj.velX-accel, -obj.maxVelX, obj.maxVelX)
                         obj.BroadcastMessage(ObjectMessage(obj,OBJECT_MOVED))
                    elif obj.action[RIGHT]:
                         if obj.velX < 0.0  and friction >= 0.0:
                              accel*=friction
                         
                         obj.velX=SetBound(obj.velX+accel, -obj.maxVelX, obj.maxVelX)
                         obj.BroadcastMessage(ObjectMessage(obj,OBJECT_MOVED))
                    elif obj.type.group != PROJECTILE:
                         #apply friction
                         if friction >= 0.0 and friction < 1.0:
                              if obj.velX > 0.0:
                                   obj.velX=SetBound(obj.velX-friction,0.0,obj.velX)
                              if obj.velX < 0.0:
                                   obj.velX=SetBound(obj.velX+friction,obj.velX,0.0)
                         elif friction >= 1.0:
                              obj.velX=0.0
               
                    if obj.group == ITEM or obj.group == PLATFORM or obj.group == PROJECTILE:
                         if obj.action[UP]:
                              obj.velY=SetBound(obj.velY-obj.accelY, -obj.maxVelY, obj.maxVelY)
                         elif obj.action[DOWN]:
                              obj.velY=SetBound(obj.velY+obj.accelY, -obj.maxVelY, obj.maxVelY)
               
                    if obj.group == PLAYER or obj.group == ENEMY or obj.name == "player" or obj.name == "player2":
                         if obj.action[DOWN]:
                              if r["obj"] != None:
                                   r["obj"].BroadcastMessage(ObjectMessage(r["obj"],OBJECT_ACTION, (obj,)))
               
                         if obj.action[JUMP]:
                              if obj.jump == False:
                                   obj.jump=True
                                   obj.velY=-obj.jumpStart
                                   obj.jumpSpeed=-obj.jumpStart
                                   obj.BroadcastMessage(ObjectMessage(obj,OBJECT_JUMPED))
                         
                              else:
                                   if abs(obj.jumpSpeed) < obj.jumpHeight or obj.jumpHeight < 0.0:
                                        obj.velY=obj.velY-obj.accelY
                                        obj.jumpSpeed=obj.jumpSpeed-obj.accelY
                              
                    obj.ResetAction()
                    if obj.jump: self.Jump(obj)
                    if obj.fall:
                         self.MoveObject(obj,obj.velX,0.0)
                    else:
                         self.MoveObject(obj,obj.velX,obj.velY)
                    
                    #check if object is still on platform
                    if obj.platform != None and obj.posY != platformY:
                         obj.platform=None
                         """
                         platform=self.GetObjectById(obj.platform)
                         if obj.posY+obj.height <= platform.posY+platform.height and obj.posY+obj.height >= platform.posY:
                              if obj.posX+obj.width>platform.posX and obj.posX+obj.width<platform.posX+platform.width:
                                   obj.platform=None
                              elif obj.posX>platform.posX and obj.posX<platform.posX+platform.width:
                                   obj.platform=None
                         """
                              
                    #only change position in map if object moved (duh)
                    #if obj.posX != obj.oldPosX and obj.posY != obj.oldPosY:
                    self.RemoveObjectFromMap(obj.id)
                    self.AddObjectToMap(obj.id)
                    
                    r=self.ObjectCollisionData(obj,0.0,0.0)
                    if r["obj"] != None:
                         if r["obj"].collision == SOLID:
                              if obj.collision == SOLID:
                                   obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(r["obj"],COLLISION_THUD)) )
                                   r["obj"].BroadcastMessage( ObjectMessage(r["obj"],OBJECT_COLLISION,(obj,COLLISION_THUD)) )
                              elif obj.collision == GHOST:
                                   obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(r["obj"],COLLISION_IMPACT)) )
                                   r["obj"].BroadcastMessage( ObjectMessage(r["obj"],OBJECT_COLLISION,(obj,COLLISION_IMPACT)) )
                         elif r["obj"].collision == GHOST:
                              if obj.collision == SOLID:
                                   obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(r["obj"],COLLISION_IMPACT)) )
                                   r["obj"].BroadcastMessage( ObjectMessage(r["obj"],OBJECT_COLLISION,(obj,COLLISION_IMPACT)) )
                              elif obj.collision == GHOST:
                                   obj.BroadcastMessage( ObjectMessage(obj,OBJECT_COLLISION,(r["obj"],COLLISION_PASS)) )
                                   r["obj"].BroadcastMessage( ObjectMessage(r["obj"],OBJECT_COLLISION,(obj,COLLISION_PASS)) )
               
               if obj.remove:
                    self.RemoveObject(obj.id)
     
     def Logic(self):
          for obj in self.platformList:
               self.LogicObject(obj)
          for obj in self.dynObjList:
               self.LogicObject(obj)
               
          self.particle.Update()
          self.UpdateAlarms()
     
     OBJFALL, OBJCOLLIDE, OBJFLOOR = 0, 1, 2
     def Fall(self,id):
          obj=self.GetObject(id)
          if obj.jump == False:
               r=self.CollisionData(obj,0.0,1.0)
               if r["downLeft"] and r["downCenter"] and r["downRight"] and r["obj"]==None:
                    obj.velY=0.0
                    obj.jump=True
                    obj.BroadcastMessage(ObjectMessage(obj,OBJECT_FELL))
                    return Room.OBJFALL
               
               #obj collides with another obj
               if r["obj"]!=None:
                    return Room.OBJCOLLIDE
               
               #obj collides with floor
               else:
                    return Room.OBJFLOOR
                    
     def Jump(self,id):
          obj=self.GetObject(id)
          
          #gravity
          if obj.fall:
               obj.velY=SetBound(obj.velY+self.gravity, -obj.maxVelY, obj.maxVelY)
               
          self.MoveObject(obj,0.0,obj.velY)
         
     def LoadObjects(self,file):
          f=None
          #if file is a string
          if type(file) == type("abc"):
               f=open(file,"rb")
          
          #file is a file object
          else:
               f=file
               
          self.RemoveAllObjects()
          num=load(f)
          for i in range(num):
               objtype=load(f)
               if self.database.ItemExists(OBJTYPE, objtype):
                    obj=Object(self.database[OBJTYPE][objtype])
                    obj.Load(f)
                    obj.maxVelX=obj.type.maxVelX
                    obj.maxVelY=obj.type.maxVelY
                    obj.accelX=obj.type.accelX
                    obj.accelY=obj.type.accelY
                    obj.jumpStart=obj.type.jumpStart
                    obj.jumpHeight=obj.type.jumpHeight
                    obj.bounceX=obj.type.bounceX
                    obj.bounceY=obj.type.bounceY
                    obj.fall=obj.type.fall
                    obj.collision=obj.type.collision
                    
                    #create controller
                    if self.GetController(obj.type.controller) != None and self.editor==False:
                         self.AddController(obj.type.controller,0,(self,obj))
                         
                    self.InsertObject(obj)
                    
          self.player=self.GetObjectByName("player")
          
          if f == None:
               return None
         
     def SaveObjects(self,file):
          f=None
          #if file is a string
          if type(file) == type("abc"):
               f=open(file,"wb")
          
          #file is a file object
          else:
               f=file
               
          dump(len(self.objList), f, HIGHEST_PROTOCOL)
          for i in self.objList:
               dump(i.type.name, f, HIGHEST_PROTOCOL)
               i.Save(f)
               
          if f == None:
               return None
          
     def SetTileTemplate(self,name):
          if self.database.ItemExists(TILETEMPLATE, name):
               self.map.ClearTileTemplates()
               self.map.tileset=self.database[TILETEMPLATE][name]["tileset"]
               for i in self.database[TILETEMPLATE][name]["tilelist"]:
                    self.map.AddTileTemplate(i)
              
     def PopFreeAlarmId(self):
          id=0
          if len(self.alarmIDList) == 0:
               id=self.alarmID
               self.alarmID+=1
          else:
               id=self.alarmIDList.pop(0)
               
          return id
          
     def PushFreeAlarmId(self,id):
          if self.alarmIDList.count(id) > 0:
               self.alarmIDList.remove(id)
              
     def AddAlarm(self,listener,time,data=None,loop=1):
          alarm=AlarmMessage(listener,time,data,loop)
          alarm.id=self.PopFreeAlarmId
          self.alarmList.append(alarm)
          return alarm.id
          
     def RemoveAlarm(self,id):
          aList=self.alarmList[:]
          for i in range(len(aList)):
               if aList[i].id==id:
                    self.PushFreeAlarmId(aList[i].id)
                    self.alarmList.remove(aList[i])
                    
          
     def UpdateAlarms(self):
          aList=self.alarmList[:]
          for i in range(len(aList)):
               alarm=aList[i]
               if alarm.startFrame+alarm.time <= main.frame:
                    alarm.iterations=alarm.iterations+1
                    self.SendMessage(alarm.listener,alarm)
                    
                    if alarm.iterations >= alarm.loop and alarm.loop > 0:
                         self.PushFreeAlarmId(aList[i].id)
                         self.alarmList.remove(aList[i])
                    else:
                         alarm.startFrame=main.frame
     
     def GetAlarmById(self,id):
          for i in self.alarmList:
               if i.id == id:
                    return i
          
          return None
     
     def SetGravity(self,g):
          if g >= 0.0:
               self.gravity=g
               
     def RemoveAll(self):
          self.RemoveAllObjects()
          self.RemoveAllControllers()
          self.particle.RemoveAllParticles()
          
     def PlaySound(self,sound,x=-1,y=-1):
          if self.database.ItemExists(SOUND,sound):
               if x < 0 or y < 0:
                    self.database[SOUND][sound].set_volume(1.0)
               #set volume according to how far player is from sound
               else:
                    vol=(400-sqrt((self.player.posX-x)**2+(self.player.posY-y)**2))/400
                    self.database[SOUND][sound].set_volume(vol)
                    
               self.database[SOUND][sound].play()
                    
               
          
          
                    