#!/usr/bin/env python

from main import *
from room import *

class View(Dispatcher):
     def __init__(self,map=None,width=0,height=0):
          Dispatcher.__init__(self)
          self.map=map
          self.width=width
          self.height=height
          self.camX=0
          self.camY=0
          self.posX=0
          self.posY=0
          self.alpha=255
          self.ResetToMap()
          self.scrollX=-1.0
          self.scrollY=-1.0
          self.tscrollX=-1.0
          self.tscrollY=-1.0
          self.tscrolltime=0
          
     def SetCamPosition(self,x,y):
          self.camX=SetBound(x,0,(len(self.map.base)-self.width)*TILEWIDTH )
          if self.width > 0:
               self.camY=SetBound(y,0,(len(self.map.base[0])-self.height)*TILEHEIGHT )
          else:
               self.camY=0
          
     def SetPosition(self,x,y):
          self.posX=x
          self.posY=y
               
     def SetAlpha(self,alpha):
          self.alpha=SetBound(alpha,0,255)
          
     def SetMap(self,map):
          self.map=map
          self.ResetToMap()
          
     def ResetToMap(self,pref_width=-1,pref_height=-1):
          mapwidth=self.map.GetMinWidth()
          mapheight=self.map.GetMinHeight()
          if pref_width < 0: pref_width=self.width
          if pref_height < 0: pref_height=self.height
          
          self.width=SetBound(pref_width,0,mapwidth)
          if self.width > 0:
               self.height=SetBound(pref_height,0,mapheight)
          else:
               self.height=0
               
          self.camX=SetBound(self.camX,0,(mapwidth-self.width)*TILEWIDTH)
          if self.width > 0:
               self.camY=SetBound(self.camY,0,(mapheight-self.height)*TILEHEIGHT)
          else:
               self.camY=0
          
     def Draw(self,screen):
          rect=Rectangle()
          orig_alpha=self.map.tileset.alpha
          self.map.tileset.SetAlpha(orig_alpha*(float(self.alpha)/255.0))
          
          for layer in self.map.layerList:
               camX=self.camX
               camY=self.camY
               camX=SetBound(int(camX*(float(layer.width)/float(self.map.baseLayer.width))**2.0),0,(layer.width-self.width)*TILEWIDTH)
               camY=SetBound(int(camY*(float(layer.height)/float(self.map.baseLayer.height))**2.0),0,(layer.height-self.height)*TILEHEIGHT)
               #camX=SetBound(int(camX*(float(self.map.baseLayer.width)/float(layer.width))),0,(layer.width-self.width)*TILEWIDTH)
               #camY=SetBound(int(camY*(float(self.map.baseLayer.height)/float(layer.height))),0,(layer.height-self.height)*TILEHEIGHT)
               
               tileX=int(floor(camX)/float(TILEWIDTH))
               tileY=int(floor(camY)/float(TILEHEIGHT))
               offX=camX-(floor(tileX*TILEWIDTH))
               offY=camY-(floor(tileY*TILEHEIGHT))
               w=self.width
               h=self.height
               if offX > 0:
                    w=w+1
               if offY > 0:
                    h=h+1
          
               for x in range(w):
                    for y in range(h):
                         tileNum=layer[x+tileX][y+tileY]
                         if tileNum >= 0:
                              tileNum=self.map.tileList[ self.map.tileIndexList[layer[x+tileX][y+tileY]] ].tile_id
                              rect.x=0
                              rect.y=0
                              rect.w=TILEWIDTH
                              rect.h=TILEHEIGHT
                              
                              if (x+tileX)*TILEWIDTH < camX:
                                   rect.x=offX
                                   rect.w=TILEWIDTH-offX
                              if (y+tileY)*TILEHEIGHT < camY:
                                   rect.y=offY
                                   rect.h=TILEHEIGHT-offY
                              if (x+tileX+1)*TILEWIDTH > camX+self.width*TILEWIDTH:
                                   rect.w=offX
                              if (y+tileY+1)*TILEHEIGHT > camY+self.height*TILEHEIGHT:
                                   rect.h=offY
                              
                              self.map.tileset.SetPosition( self.posX+(x*TILEWIDTH)-offX, self.posY+(y*TILEHEIGHT)-offY )
                              self.map.tileset.Draw(screen, tileNum, rect.x, rect.y, rect.w, rect.h)
                              
          self.map.tileset.SetAlpha(orig_alpha)

BACKGROUND=0
FOREGROUND=1
class RoomView(View):
     def __init__(self,room=None,width=0,height=0):
          View.__init__(self,room.map,width,height)
          self.room=room
          self.focus=-1
          self.fade=False
          self.focusAfterScroll=-1
          
     def DrawObjects(self,screen,border=-2,color=Color(0,255,0,255)):
          origAlpha=0
          rect, sRect, oRect=Rectangle(), Rectangle(), Rectangle()
          offX=int(self.camX-(floor(self.camX/TILEWIDTH)*TILEWIDTH))
          offY=int(self.camY-(floor(self.camY/TILEHEIGHT)*TILEHEIGHT))
          sRect.x=self.camX
          sRect.y=self.camY
          sRect.w=self.width*TILEWIDTH
          sRect.h=self.height*TILEHEIGHT
          for i in range(len(self.room.objList)):
               obj=self.room.objList[i]
               oRect.w=obj.sprite.offX
               oRect.h=obj.sprite.offY
               
               oRect.x=obj.posX-( floor((obj.sprite.offX-obj.width)/2) )
               oRect.y=obj.posY-(obj.sprite.offY-obj.height)
               #oRect.x=obj.posX
               #oRect.y=obj.posY
               
               if oRect.isIntersecting(sRect):
                    rect.x=0
                    rect.y=0
                    rect.w=oRect.w
                    rect.h=oRect.h
                    if oRect.x < self.camX:
                         rect.x=self.camX-oRect.x
                         rect.w=rect.w-rect.x
                    
                    if oRect.y < self.camY:
                         rect.y=self.camY-oRect.y
                         rect.h=rect.h-rect.y
                         
                    if oRect.x+oRect.w > self.camX+(self.width*TILEWIDTH):
                         rect.w=rect.w-((oRect.x+oRect.w)-(self.camX+(self.width*TILEWIDTH)))
                         
                    if oRect.y+oRect.h > self.camY+(self.height*TILEHEIGHT):
                         rect.h=rect.h-((oRect.y+oRect.h)-(self.camY+(self.height*TILEHEIGHT)))
                    
                    origAlpha=obj.sprite.alpha
                    obj.sprite.SetAlpha( float(origAlpha) * (float(self.alpha)/float(255)) )
                    obj.sprite.SetPosition(self.posX+(oRect.x-self.camX), self.posY+(oRect.y-self.camY))
                    obj.sprite.Draw(screen, True, rect.x, rect.y, rect.w, rect.h)
                    obj.sprite.SetAlpha(origAlpha)
                    
                    if border == obj.id or border == -1:
                         bRect=Rectangle()
                         bRect.x=self.posX+(oRect.x-self.camX)+rect.x
                         bRect.y=self.posY+(oRect.y-self.camY)+rect.y
                         bRect.w=rect.w
                         bRect.h=rect.h
                         
                         pygame.draw.rect(screen, color.ToTuple(), (bRect.x,bRect.y,bRect.w,bRect.h), 1)
                         
     def DrawParticles(self,screen):
          for i in self.room.particle.particleList:
               shape=i.shape.Clone()
               shape.SetPosition(self.posX+(i.shape.posX-self.camX), self.posY+(i.shape.posY-self.camY))
               
               if isinstance(i.shape,Polygon):
                    if i.fill:
                         pygame.gfxdraw.filled_polygon(screen, shape.points, i.color.ToTuple())
                    else:
                         pygame.gfxdraw.polygon(screen, shape.points, i.color.ToTuple())
               #elif isinstance(i.shape,Circle):
               else:
                    if i.fill:
                         pygame.gfxdraw.filled_circle(screen, shape.posX, shape.posY, shape.radius, i.color.ToTuple())
                    else:
                         pygame.gfxdraw.circle(screen, shape.posX, shape.posY, shape.radius, i.color.ToTuple())
                         
     def DrawTiles(self,screen,order=BACKGROUND):
          rect=Rectangle()
          orig_alpha=self.map.tileset.alpha
          self.map.tileset.SetAlpha(orig_alpha*(float(self.alpha)/255.0))
          
          for layer in self.map.layerList:
               if ((order==BACKGROUND and layer.order<=1) or (order==FOREGROUND and layer.order>1)) and layer.visible:
                    camX=self.camX
                    camY=self.camY
                    camX=SetBound(int(camX*(float(layer.width)/float(self.map.baseLayer.width))),0,(layer.width-self.width)*TILEWIDTH)
                    camY=SetBound(int(camY*(float(layer.height)/float(self.map.baseLayer.height))),0,(layer.height-self.height)*TILEHEIGHT)
                    #camX=SetBound(int(camX*(float(self.map.baseLayer.width)/float(layer.width))),0,(layer.width-self.width)*TILEWIDTH)
                    #camY=SetBound(int(camY*(float(self.map.baseLayer.height)/float(layer.height))),0,(layer.height-self.height)*TILEHEIGHT)
               
                    tileX=int(floor(camX)/float(TILEWIDTH))
                    tileY=int(floor(camY)/float(TILEHEIGHT))
                    offX=camX-(floor(tileX*TILEWIDTH))
                    offY=camY-(floor(tileY*TILEHEIGHT))
                    w=self.width
                    h=self.height
                    if offX > 0:
                         w=w+1
                    if offY > 0:
                         h=h+1
          
                    for x in range(w):
                         for y in range(h):
                              tileNum=layer[x+tileX][y+tileY]
                              if tileNum >= 0:
                                   tileNum=self.map.tileList[ self.map.tileIndexList[layer[x+tileX][y+tileY]] ].tile_id
                                   rect.x=0
                                   rect.y=0
                                   rect.w=TILEWIDTH
                                   rect.h=TILEHEIGHT
                              
                                   if (x+tileX)*TILEWIDTH < camX:
                                        rect.x=offX
                                        rect.w=TILEWIDTH-offX
                                   if (y+tileY)*TILEHEIGHT < camY:
                                        rect.y=offY
                                        rect.h=TILEHEIGHT-offY
                                   if (x+tileX+1)*TILEWIDTH > camX+self.width*TILEWIDTH:
                                        rect.w=offX
                                   if (y+tileY+1)*TILEHEIGHT > camY+self.height*TILEHEIGHT:
                                        rect.h=offY
                              
                                   self.map.tileset.SetPosition( self.posX+(x*TILEWIDTH)-offX, self.posY+(y*TILEHEIGHT)-offY )
                                   self.map.tileset.Draw(screen, tileNum, rect.x, rect.y, rect.w, rect.h)
                              
          self.map.tileset.SetAlpha(orig_alpha)
                    
     def Draw(self,screen,border=-2,color=Color(0,255,0,255)):
          if self.scrollX < 0.0 or self.scrollY < 0.0:
               self.FocusTo(self.focus)
          else:
               self.tscrolltime-=1
               self.SetCamPosition(self.camX+self.tscrollX, self.camY+self.tscrollY)
               if (self.tscrolltime <= 0) or (int(self.scrollX)==int(self.camX) and int(self.scrollY)==int(self.camY)):
                    self.tscrolltime == 0
                    self.scrollX=-1.0
                    self.scrollY=-1.0
                    self.tscrollx=0.0
                    self.tscrolly=0.0
                    self.FocusTo(self.focusAfterScroll)
                    self.focusAfterScroll=-1
                    self.BroadcastMessage(ViewMessage(VIEW_SCROLLEND,self))
                    
          if self.fade:
               self.SetAlpha(self.fadeStart+(self.fadeStep*self.fadeInterval))
               self.fadeStep+=1
               if self.fadeStep>=self.fadeTime:
                    self.fade=False
               if self.fadeInterval < 0 and self.fadeStart <= self.fadeEnd:
                    self.fade=False
               if self.fadeInterval > 0 and self.fadeStart >= self.fadeEnd:
                    self.fade=False
                    
               if self.fade == False:
                    self.BroadcastMessage(ViewMessage(VIEW_FADEEND,self))
          
          screen.set_clip((self.posX,self.posY,self.width*TILEWIDTH,self.height*TILEHEIGHT))
          self.DrawTiles(screen,BACKGROUND)
          self.DrawObjects(screen,border,color)
          #self.DrawOverlay(screen)
          self.DrawParticles(screen)
          self.DrawTiles(screen,FOREGROUND)
          screen.set_clip(None)
          
          self.BroadcastMessage(ViewMessage(VIEW_DRAW,self))
     
     """
     def DrawOverlay(self,screen):
          rect=Rectangle()
          orig_alpha=self.map.tileset.alpha
          self.map.tileset.SetAlpha(orig_alpha*(float(self.alpha)/255.0))
          tileX=int(floor(self.camX/TILEWIDTH))
          tileY=int(floor(self.camY/TILEHEIGHT))
          offX=self.camX-(floor(tileX*TILEWIDTH))
          offY=self.camY-(floor(tileY*TILEHEIGHT))
          w=self.width
          h=self.height
          if offX > 0:
               w=w+1
          if offY > 0:
               h=h+1
          
          for x in range(w):
               for y in range(h):
                    tileNum=self.map.overlay[x+tileX][y+tileY]
                    if tileNum >= 0:
                         tileNum=self.map.tileList[ self.map.tileIndexList[self.map.overlay[x+tileX][y+tileY]] ].tile_id
                         rect.x=0
                         rect.y=0
                         rect.w=TILEWIDTH
                         rect.h=TILEHEIGHT
                              
                         if (x+tileX)*TILEWIDTH < self.camX:
                              rect.x=offX
                              rect.w=TILEWIDTH-offX
                         if (y+tileY)*TILEHEIGHT < self.camY:
                              rect.y=offY
                              rect.h=TILEHEIGHT-offY
                         if (x+tileX+1)*TILEWIDTH > self.camX+self.width*TILEWIDTH:
                              rect.w=offX
                         if (y+tileY+1)*TILEHEIGHT > self.camY+self.height*TILEHEIGHT:
                              rect.h=offY
                              
                         self.map.tileset.SetPosition( self.posX+(x*TILEWIDTH)-offX, self.posY+(y*TILEHEIGHT)-offY )
                         self.map.tileset.Draw(screen, tileNum, rect.x, rect.y, rect.w, rect.h)
                         
          self.map.tileset.SetAlpha(orig_alpha)
     """
          
     def FocusTo(self,id,once=False):
          if once == False:
               self.focus=id
          obj=self.room.GetObject(id)
          if obj != None:
               self.SetCamPosition(obj.posX-(self.width*TILEWIDTH/2)+(obj.width/2), obj.posY-(self.height*TILEHEIGHT/2)+(obj.height/2))
               self.BroadcastMessage(ViewMessage(VIEW_FOCUS,self))
          else:
               self.focus=-1
               self.BroadcastMessage(ViewMessage(VIEW_FOCUSLOST,self))
               
     def FocusToScroll(self,id,time=40):
          obj=self.room.GetObject(id)
          if obj != None:
               self.ScrollTo(obj.posX-(self.width*TILEWIDTH/2)+(obj.width/2), obj.posY-(self.height*TILEHEIGHT/2)+(obj.height/2),time)
        
     def ScrollAndFocus(self,id,time=40):
          obj=self.room.GetObject(id)
          self.focusAfterScroll=id
          if obj != None:
               self.ScrollTo(obj.posX-(self.width*TILEWIDTH/2)+(obj.width/2), obj.posY-(self.height*TILEHEIGHT/2)+(obj.height/2),time)
        
     def ScrollTo(self,sx,sy,time):
          self.scrollX=SetBound(sx,0,(self.map.width*TILEWIDTH)-self.width)
          self.scrollY=SetBound(sy,0,(self.map.height*TILEHEIGHT)-self.height)
          self.tscrolltime=time
          self.tscrollX=(self.scrollX-self.camX)/time
          self.tscrollY=(self.scrollY-self.camY)/time
          self.BroadcastMessage(ViewMessage(VIEW_SCROLLSTART,self))
          
     def FadeIn(self,time,end=255,start=0):
          self.fade=True
          self.fadeStart=start
          self.fadeEnd=end
          self.fadeInterval=-1*((start-end)/(time))
          self.fadeStep=0
          self.fadeTime=time
          
          self.SetAlpha(start)
          self.BroadcastMessage(ViewMessage(VIEW_FADESTART,self))
          
     def FadeOut(self,time,end=0,start=255):
          self.FadeIn(time,end,start)
          
          
          
     