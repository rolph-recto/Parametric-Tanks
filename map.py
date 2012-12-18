#!/usr/bin/env python

from main import *

class TileTemplate:
     def __init__(self,name=""):
          self.name=name
          self.walkable=True
          self.cloud=False
          self.friction=0.0
          self.slope=False
          self.tile_id=-1
          self.id=-1
          
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
               
          dump(self.name,f, HIGHEST_PROTOCOL)
          dump(self.walkable,f, HIGHEST_PROTOCOL)
          dump(self.cloud,f, HIGHEST_PROTOCOL)
          dump(self.friction,f, HIGHEST_PROTOCOL)
          dump(self.slope,f, HIGHEST_PROTOCOL)
          dump(self.tile_id,f, HIGHEST_PROTOCOL)
          
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
          self.walkable=load(f)
          self.cloud=load(f)
          self.friction=load(f)
          self.slope=load(f)
          self.tile_id=load(f)
          
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()

LAYER_VERSION=1.0

class Layer:
     def __init__(self,name,width,height,order=0):
          self.map=[]
          self.name=name
          self.order=order
          self.id=-1
          self.visible=True
          
          self.Resize(width,height)
          
     def Resize(self,width,height,fill=-1):
          tempMap=self.map[:]
          oldWidth=len(self.map)
          if oldWidth > 0:
               oldHeight=len(self.map[0])
          else:
               oldHeight=0
               
          self.map=[]
          row=[]
          for x in range(width):
               rowMap=[]
               for y in range(height):
                    if x < oldWidth and y < oldHeight:
                         rowMap.append(tempMap[x][y])
                    else:
                         rowMap.append(fill)
                    
               self.map.append( array('h', rowMap) )
               
          self.width=len(self.map)
          self.height=len(self.map[0])
               
     def Copy(self,layer):
          map=None
          if isinstance(layer,Layer):
               map=layer.map
          else:
               map=layer
               
          self.Resize(len(map),len(map[0]))
          
          for x in range(len(map)):
               for y in range(len(map[0])):
                    self.map[x][y]=map[x][y]
                    
     def Save(self,file,version=LAYER_VERSION):
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
          dump(version, f)
          if version==1.0:
               dump(self.name, f)
               dump(self.order, f)
               dump(self.map, f, HIGHEST_PROTOCOL)
               
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
          version=load(f)
          if version==1.0:
               self.name=load(f)
               self.order=load(f)
               map=load(f)
               self.Copy(map)
               
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
                    
     def __getitem__(self,key):
          if key>=0 and key<self.width:
               return self.map[key]
     
     def __setitem__(self,key):
          pass
                    
                    
#MAP_VERSION = 1.0
MAP_VERSION = 1.5

class MapData:
     def __init__(self):
          self.baseLayer=None
          self.overlay=[]
          self.tileIDList=[]
          self.tileID=0
          self.tileList=[]
          self.tileIndexList=[]
          self.layerList=[]
          self.layerID=0
          self.layerIDList=[]
          self.tileset=Tileset()
          self.id=0
     
     def getwidth(self):
          return len(self.base)
    
     width=property(getwidth)
     
     def getheight(self):
          return len(self.base[0])
    
     height=property(getheight)
     
     def getbase(self):
          return self.baseLayer.map
          
     base=property(getbase)
     
     def Resize(self,width,height,fill=-1):
          self.baseLayer.Resize(width,height,fill)
          
          """
          tempBase=self.base[:]
          tempOverlay=self.overlay[:]
          oldWidth=len(self.base)
          if oldWidth > 0:
               oldHeight=len(self.base[0])
          else:
               oldHeight=0
               
          self.base=[]
          self.overlay=[]
          row=[]
          for x in range(width):
               rowBase=[]
               rowOverlay=[]
               for y in range(height):
                    if x < oldWidth and y < oldHeight:
                         rowBase.append(tempBase[x][y])
                         rowOverlay.append(tempOverlay[x][y])
                    else:
                         rowBase.append(fill)
                         rowOverlay.append(-1)
                    
               self.base.append( array('h', rowBase) )
               self.overlay.append( array('h', rowOverlay) )
               
          self.width=len(self.base)
          if self.width > 0:
               self.height=len(self.base[0])
          else:
               self.height=0
          """
     
     def SetBase(self,x,y,template=-1):
          if x >= 0 and x <= self.width-1 and y >=0 and y <= self.height-1:
               if type(template) == type("abc"):
                    self.base[x][y]=self.GetTemplateIdByName(template)
               elif type(template) == type(123):
                    self.base[x][y]=template
               
     def SetOverlay(self,x,y,template=-1):
          if x >= 0 and x <= self.width-1 and y >=0 and y <= self.height-1:
               if type(template) == type("abc"):
                    self.overlay[x][y]=self.GetTemplateIdByName(template)
               elif type(template) == type(123):
                    self.overlay[x][y]=template             
     
     def FillBase(self,template):
          index=-1
          if type(template) == type("abc"):
               index=self.GetTemplateIdByName(template)
          elif type(template) == type(123):
               index=template
          else:
               index=template.id
          
          for x in range(len(self.base)):
               for y in range(len(self.base[0])):
                    self.base[x][y]=index
                         
     def FillOverlay(self,template):
          index=-1
          if type(template) == type("abc"):
               index=self.GetTemplateIdByName(template)
          elif type(template) == type(123):
               index=template
          else:
               index=template.id
      
          for x in range(len(self.overlay)):
               for y in range(len(self.overlay[0])):
                    self.overlay[x][y]=index

     def PopFreeTileId(self):
          id=0
          if len(self.tileIDList) == 0:
               id=self.tileID
               self.tileID+=1
          else:
               id=self.tileIDList.pop(0)
               
          return id
          
     def PushFreeTileId(self,id):
          if self.tileIDList.count(id) > 0:
               self.tileIDList.remove(id)
               
     def TemplateExists(self,name):
          exist=False
          for i in self.tileList:
               if i.name == name:
                    exist=True
                    break
                    
          return exist
          
     def GetTemplateIdByName(self,name):
          for i in self.tileList:
               if i.name == name:
                    return i.id
                    
          return -1
          
     def GetTemplateNameById(self,id):
          for i in self.tileList:
               if i.id == id:
                    return i.name
                    
          return ""
          
     def GetTemplateIndexByName(self,name):
          for i in range(len(self.tileList)):
               if self.tileList[i].name == name:
                    return i
                    
          return -1
          
     def GetTemplateIndexById(self,id):
          for i in range(len(self.tileList)):
               if self.tileList[i].id == id:
                    return i
                    
          return -1
                      
     def AddTileTemplate(self,template):
          if self.TemplateExists(template.name) == False:
               template.id=self.PopFreeTileId()
               self.tileList.append(template)
               self.tileIndexList.append(template.id)
                      
     def CreateTileTemplate(self,name,tile_id,walkable=True,cloud=False,ladder=False,slope=False,friction=1.0):
          if self.TemplateExists(name) == False:
               tile=TileTemplate(name)
               tile.walkable=walkable
               tile.cloud=cloud
               tile.ladder=ladder
               tile.slope=slope
               tile.friction=friction
               tile.tile_id=tile_id
               self.AddTileTemplate(tile)
               return self.GetTemplateIndexByName(tile.name)
          
          return -1
          
     def RemoveTileTemplate(self,name):
          if type(name) == type("abc"):
               if self.TemplateExists(name):
                    self.RemoveTileTemplate(self.GetTemplateIdByName(name))
                    
          else:          
               id=self.GetTemplateIdByName(name)
               self.PushFreeTileId(id)
               for i in range(len(self.tileList)):
                    if self.tileList[i].id == id:
                         self.tileList.pop(i)
                         self.tileIndexList.pop(i)
                         break
                    
     def ClearTileTemplates(self):
          #clear tileList
          del self.tileList[:]
          self.tileId=0
          del self.tileIDList[:]
          
     def PopFreeLayerId(self):
          id=0
          if len(self.layerIDList) == 0:
               id=self.layerID
               self.layerID+=1
          else:
               id=self.layerIDList.pop(0)
               
          return id
          
     def PushFreeLayerId(self,id):
          if self.layerIDList.count(id) > 0:
               self.layerIDList.remove(id)
               
     def GetLayerByName(self,name):
          for i in self.layerList:
               if i.name==name:
                    return i
          
          return None

     def GetLayerById(self,id):
          for i in self.layerList:
               if i.id==id:
                    return i
          
          return None          
     
     def LayerExists(self,name):
          exist=False
          for i in self.layerList:
               if i.name == name:
                    exist=True
                    break
                    
          return exist
     
     def SetBaseLayer(self,layer):
          if self.LayerExists(layer):
               l=self.GetLayerByName(layer)
               self.baseLayer=l
          else:
               self.baseLayer=None
     
     def SetLayer(self,layer,x,y,template=-1):
          l=None
          if type(layer) == type("abc"):
               l=self.GetLayerByName(layer)
          elif type(layer) == type(123):
               l=self.GetLayerById(layer)
               
          if l==None: return None
          
          if x >= 0 and x <= self.width-1 and y >=0 and y <= self.height-1:
               if type(template) == type("abc"):
                    l[x][y]=self.GetTemplateIdByName(template)
               elif type(template) == type(123):
                    l[x][y]=template
                    
     def FillLayer(self,layer,template=-1):
          l=None
          if type(layer) == type("abc"):
               l=self.GetLayerByName(layer)
          elif type(layer) == type(123):
               l=self.GetLayerById(layer)
               
          if l==None: return None
     
          index=-1
          if type(template) == type("abc"):
               index=self.GetTemplateIdByName(template)
          elif type(template) == type(123):
               index=template
          else:
               index=template.id
          
          for x in range(len(l.map)):
               for y in range(len(l.map[0])):
                    l[x][y]=index
     
     def AddLayer(self,layer):
          layer.id=self.PopFreeLayerId()
     
          if len(self.layerList) == 0:
               self.layerList.append(layer)
               
          else:
               last=True
               for i in range(len(self.layerList)):
                    if layer.order<self.layerList[i].order:
                         self.layerList.insert(i,layer)
                         last=False
               
               if last:
                    self.layerList.append(layer)
                         
          return layer.id
          
     def RemoveLayer(self,layer):
          l=None
          if type(layer) == type("abc"):
               l=self.GetLayerByName(layer)
          elif type(layer) == type(123):
               l=self.GetLayerById(layer)
               
          if l==None: return None
          
          self.PushFreeLayerId(l.id)
          self.layerList.remove(l)
          
     def ClearAllLayers(self):
          #clear tileList
          del self.layerList[:]
          self.layerId=0
          del self.layerIDList[:]
     
     def CreateLayer(self,name,width,height,order=0):
          layer=Layer(name,width,height,order)
          self.AddLayer(layer)
               
     def SaveTemplates(self,file):
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
          self.tileset.Save(f)
          dump(len(self.tileList),f, HIGHEST_PROTOCOL)
          for i in self.tileList:
               i.Save(f)
               
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
               
     def LoadTemplates(self,file):
          f=None
          #if file is a string
          if type(file) == type("abc"):
               f=open(file,"rb")
          
          #file is a file object
          else:
               f=file
               
          if f == None:
               return None
          
          self.ClearTileTemplates()
          
          #commence reading
          self.tileset.Load(f)
          n=load(f)
          for i in range(n):
               tile=TileTemplate("")
               tile.Load(f)
               self.AddTileTemplate(tile)
               
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
               
     def Save(self,file,version=MAP_VERSION):
          f=None
          #if file is a string
          if type(file) == type("abc"):
               f=open(file,"wb")
          
          #file is a file object
          else:
               f=file
               
          if f == None:
               return None
               
          dump(version, f)     
          if version==1.0:
               dump(self.base, f, HIGHEST_PROTOCOL)
               dump(self.overlay, f, HIGHEST_PROTOCOL)
          elif version==1.5:
               dump(len(self.layerList), f)
               for i in self.layerList:
                    dump(1.0, f) #version
                    dump(i.name, f)
                    dump(i.order, f)
                    dump(i.map, f, HIGHEST_PROTOCOL)
               dump(self.baseLayer.name, f)
               
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
          
          #load arrays
          self.ClearAllLayers()
          version=load(f)
          
          if version == 1.0:
               base=load(f)
               overlay=load(f)
               width=len(base)
               height=len(base[0])
               self.CreateLayer("base",width,height,0)
               self.CreateLayer("overlay",width,height,1)
               self.GetLayerByName("base").Copy(base)
               self.GetLayerByName("overlay").Copy(overlay)
               self.SetBaseLayer("base")
               
          elif version == 1.5:
               n=load(f)
               for i in range(n):
                    lversion=load(f)
                    if lversion==1.0:
                         name=load(f)
                         order=load(f)
                         map=load(f)
                         layer=Layer(name,len(map),len(map[0]),order)
                         layer.Copy(map)
                         self.AddLayer(layer)
                         
               lbase=load(f)
               self.SetBaseLayer(lbase)
               
          #if file is a string, close file object
          if type(file) == type("abc"):
               f.close()
               
     def GetMinWidth(self):
          width=self.width
          for i in self.layerList:
               if i.width<width:
                    width=i.width
          
          return width
          
     def GetMinHeight(self):
          height=self.height
          for i in self.layerList:
               if i.height<height:
                    height=i.height
          
          return height
          
          
          
          
           