#!/usr/bin/env python

from room import *
from map import *
from pickle import *
import pygame.gfxdraw
from guichan import *

#import psyco
#psyco.profile()

from state import *
from view import *
from particle import *

import profile
import pstats
from objType import *

s=None
screen = None
room = None
v=None
key=None
clock, inputMessage=None, None
pause, done = False, False
player, player2=None, None
turn=1
shot=False
updateRect=[]
scrolling=False
cutscene=False
victory=False
cutsceneList=[]
cutsceneIndex=-1

#GUI
gui, input, graphics, font, top, action = None, None, None, None, None, None
notifyLabel=None
healthBar=None
angleLabel=None
powerLabel=None
powerSlider=None
normalRadio=None
fireballRadio=None
terraRadio=None
dynamiteRadio=None
spreadRadio=None
spreadfireRadio=None
moveRadio=None
pointLabel=None
victoryLabel=None
moveLabel=None

cs1, cs2=[], []

class InitState(State):
     def __init__(self):
          State.__init__(self,"init",InitState.EventTable)
          
     def Start(self, args=()):
          os.chdir(BASEDIR)
          execfile("config.py")
     
          pygame.init()
          global screen
          screen = pygame.display.set_mode((config["SCREEN_WIDTH"], config["SCREEN_HEIGHT"]), config["DISPLAY_FLAGS"])
          pygame.display.set_caption(config["TITLE"],config["ICON_TITLE"])
          icon=pygame.image.load(config["ICON"])
          pygame.display.set_icon(icon)
          pygame.mixer.init()
          pygame.key.set_repeat(config["KEYREPEAT_DELAY"], config["KEYREPEAT_INTERVAL"])
          
          #pygame.mixer.music.load("TMCPalaceOfWinds.mid")
          #pygame.mixer.music.play()
          
          global room
          room=Room()
          room.database.LoadXML(config["DATABASE"])
          room.SetTileTemplate(config["TILE_TEMPLATE"])
          
          particle=room.particle
          
          for i in config["PARTICLE_TEMPLATES"]:
               particle.AddTemplate(i)
          
          global clock, inputMessage
          clock = pygame.time.Clock()
          inputMessage=InputMessage(None)
     
          self.InitGUI()
          
     def InitGUI(self):
          global gui, input, graphics, font, top, action
          gui=Gui()
          input=PygameInput()
          Image.mImageLoader=PygameImageLoader()
          graphics=PygameGraphics()
          graphics.setTarget(screen)
          font=PygameFont(config["FONT_FILE"],config["FONT_SIZE"],config["FONT_COLOR"])
          font.setGlyphSpacing(config["FONT_SIZE"])
          Widget.setGlobalFont(font)
          top=Container()
          top.setOpaque(False)
          top.setPosition(0,0)
          top.setSize(config["SCREEN_WIDTH"],config["SCREEN_HEIGHT"])
          gui.setInput(input)
          gui.setTop(top)
          gui.setGraphics(graphics)
          
          action=ActionListener()
          action.action=OnAction
          action.valueChanged=OnAction
          
          global healthBar
          healthBar=ProgressBar(10.0,5.0)
          healthBar.setWidth(100)
          healthBar.setHeight(10)
          healthBar.setBaseColor(Color(255,0,0))
          healthBar.setForegroundColor(Color(0,255,0))
          healthBar.setVisible(False)
          top.add(healthBar,20,config["SCREEN_HEIGHT"]-24)
          
          global angleLabel
          angleLabel=Label("Angle: 0")
          angleLabel.setVisible(False)
          angleLabel.setTextColor(Color(255,255,255))
          top.add(angleLabel,20,config["SCREEN_HEIGHT"]-48)
          
          global powerLabel, powerSlider
          powerLabel=Label("Power: 0")
          powerLabel.setVisible(False)
          powerLabel.setTextColor(Color(255,255,255))
          top.add(powerLabel,140,config["SCREEN_HEIGHT"]-48)
          
          powerSlider=Slider(0,config["MAX_POWER"])
          powerSlider.setWidth(200)
          powerSlider.setHeight(10)
          powerSlider.setActionEventId("power")
          powerSlider.addActionListener(action)
          powerSlider.setMarkerLength(5)
          powerSlider.setStepLength(5)
          powerSlider.setVisible(False)
          top.add(powerSlider,140,config["SCREEN_HEIGHT"]-24)
          
          global pointLabel
          pointLabel=Label("Points: 100")
          pointLabel.setVisible(False)
          pointLabel.setTextColor(Color(255,255,255))
          top.add(pointLabel,218,config["SCREEN_HEIGHT"]-48)
          
          global moveLabel
          moveLabel=Label("M: 100")
          moveLabel.setVisible(False)
          moveLabel.setTextColor(Color(255,255,255))
          top.add(moveLabel,300,config["SCREEN_HEIGHT"]-48)
          
          global normalRadio,fireballRadio,terraRadio,dynamiteRadio,spreadRadio,spreadfireRadio,moveRadio
          normalRadio=RadioButton("(0)Normal: --","weapon",True)
          normalRadio.setVisible(False)
          
          fireballRadio=RadioButton("(1)Fireball: 0","weapon",False)
          fireballRadio.setVisible(False)
          
          terraRadio=RadioButton("(2)Terra: 0","weapon",False)
          terraRadio.setVisible(False)
          
          dynamiteRadio=RadioButton("(3)Dynamite: 0","weapon",False)
          dynamiteRadio.setVisible(False)
          
          spreadRadio=RadioButton("(4)Spreadshot: 0","weapon",False)
          spreadRadio.setVisible(False)
          
          spreadfireRadio=RadioButton("(5)Spreadfire: 0","weapon",False)
          spreadfireRadio.setVisible(False)
          
          moveRadio=RadioButton("(6)M","weapon",False)
          moveRadio.setVisible(False)
          
          top.add(normalRadio,360,config["SCREEN_HEIGHT"]-48)
          top.add(fireballRadio,360,config["SCREEN_HEIGHT"]-24)
          top.add(terraRadio,480,config["SCREEN_HEIGHT"]-48)
          top.add(dynamiteRadio,480,config["SCREEN_HEIGHT"]-24)
          top.add(spreadRadio,600,config["SCREEN_HEIGHT"]-48)
          top.add(spreadfireRadio,600,config["SCREEN_HEIGHT"]-24)
          top.add(moveRadio,740,config["SCREEN_HEIGHT"]-48)
          
          global victoryLabel
          victoryLabel=Label("")
          victoryLabel.setTextColor(Color(255,255,255))
          top.add(victoryLabel,(config["SCREEN_WIDTH"]/2)-(victoryLabel.getWidth()/2),(config["SCREEN_HEIGHT"]/2)-(victoryLabel.getHeight()/2))
          
     def Stop(self, args=()):
          pass
          
     EventTable={ 'start': (Start, "splash"),
                  'stop': (Stop, None) }
                  
def OnAction(action):
     id=action.getId()
     global turn
     if id == "power":
          if turn==1:
               player.data["power"]=int(powerSlider.getValue())
               powerLabel.setCaption("Power: "+str(player.data["power"]))
          else:
               player2.data["power"]=int(powerSlider.getValue())
               powerLabel.setCaption("Power: "+str(player2.data["power"]))

def Notify(caption):
     global notifyLabel
     notifyLabel.setCaption(caption)
     notifyLabel.setPosition((config["SCREEN_WIDTH"]/2)-(notifyLabel.getWidth()/2), config["VIEW_POSY"]+(config["VIEW_HEIGHT"]*TILEHEIGHT)+5)

def ChangeTurn(args=()):
     global turn, shot
     obj=None
     if turn == 1:
          turn=2
          obj=room.GetObjectById(player2.id)
          if v.focus == player.id:
               v.FocusTo(player2.id) 
     else:
          turn=1
          obj=room.GetObjectById(player.id)
          if v.focus == player2.id:
               v.FocusTo(player.id)
     
     healthBar.setMax(obj.data["max_hp"])
     healthBar.setValue(obj.data["current_hp"])
     powerLabel.setCaption("Power: "+str(obj.data["power"]))
     powerSlider.setValue(obj.data["power"])
     fireballRadio.setCaption("(1)Fireball: "+str(obj.data["fireball"]))
     terraRadio.setCaption("(2)Terra: "+str(obj.data["terra"]))
     dynamiteRadio.setCaption("(3)Dynamite: "+str(obj.data["dynamite"]))
     spreadRadio.setCaption("(4)Spreadshot: "+str(obj.data["spreadshot"]))
     spreadfireRadio.setCaption("(5)Spreadfire: "+str(obj.data["spreadfire"]))
     pointLabel.setCaption("Points: "+str(obj.data["score"]))
     moveLabel.setCaption("M: "+str(obj.data["move"]))
               
     shot=False          
     
notifyAlarm=-1
class ObjectListener(Listener):
     def __init__(self, room):
          Listener.__init__(self)
          self.room=room
          self.max_points=0
          if self.room != None:
               self.Reload()
          
     def Reload(self):
          self.max_points=0
          for i in self.room.objList:
               if i.type.name == "player1" or i.type.name=="player2":
                    i.AddSubscriber(self,MSG_ALL)
     
     def OnPlayerScored(self,message):
          global turn
          if turn==1:
               pointLabel.setCaption("Points: "+str(player.data["score"]))
          else:
               pointLabel.setCaption("Points: "+str(player2.data["score"]))
     
     def OnPlayerDied(self,message):
          global victory
          victory=True
          if message.obj.type.name=="player1":
               victoryLabel.setCaption("RED WINS")
               victoryLabel.setPosition((config["SCREEN_WIDTH"]/2)-(victoryLabel.getWidth()/2),(config["SCREEN_HEIGHT"]/2)-(victoryLabel.getHeight()/2))
          else:
               victoryLabel.setCaption("YELLOW WINS")
               victoryLabel.setPosition((config["SCREEN_WIDTH"]/2)-(victoryLabel.getWidth()/2),(config["SCREEN_HEIGHT"]/2)-(victoryLabel.getHeight()/2))   
     
     def FollowProjectile(self,p):
          p.AddSubscriber(self,OBJECT_DESTROYED)
          
     def OnObjectDestroy(self,message):
          if message.obj.type.name=="cannonball":
               global turn, cs1, cs2
               if turn==1:
                    LoadCutscene(cs1)
               else:
                    LoadCutscene(cs2)
          
     def OnAlarm(self,message):
          if message.data == 4:
               NextCutscene()
          
def ScrollTo(args):
     global scrolling
     v.FocusToScroll(args[0],args[1])
     scrolling=True
     
def ScrollEnd(m):
     global scrolling
     if scrolling:
          NextCutscene()
          scrolling=False
     
def Wait(frames):
     room.AddAlarm(s.stateList["room"].oListen,frames,4)
          
def LoadCutscene(cslist):
     global cutsceneList, cutsceneIndex
     cutsceneList=cslist
     cutsceneIndex=0
     
     InitCutscene()
     PlayCutscene()
          
def InitCutscene():
     global cutscene
     if cutscene: return None
     cutscene=True
     
def PlayCutscene():
     global cutscene, cutsceneList, cutsceneIndex
     if cutscene:
          #call cutscene func with args
          cutsceneList[cutsceneIndex][0](cutsceneList[cutsceneIndex][1])
          #don't wait for NextCutscene event
          if cutsceneList[cutsceneIndex][2] == 0:
               NextCutscene()

def NextCutscene():
     global cutscene, cutsceneList, cutsceneIndex
     if cutscene:
          cutsceneIndex+=1
          if cutsceneIndex >= len(cutsceneList):
               StopCutscene()
          else:
               PlayCutscene()
     
def StopCutscene():
     global cutscene, cutsceneList, cutsceneIndex
     cutscene=False
     cutsceneList=[]
     cutsceneIndex=-1
          
class RoomState(State):
     def __init__(self):
          global room
          State.__init__(self,"room",RoomState.EventTable)
          self.level=0
          self.oListen=ObjectListener(room)

     def OnViewFadeEnd(self,message):
          pass
          
     def Start(self, args=()):
          self.status=0
          global CURRENTLEVELDIR
          CURRENTLEVELDIR=os.path.join(LEVELDIR,config["LEVELS"][self.level])
          
          room.RemoveAll()
          room.map.Load(os.path.join(CURRENTLEVELDIR,"map.txt"))
          room.LoadObjects(os.path.join(CURRENTLEVELDIR,"object.txt"))
          
          global v, turn, shot
          if v == None:
               v=RoomView(room,config["VIEW_WIDTH"],config["VIEW_HEIGHT"])
               v.SetPosition(config["VIEW_POSX"],config["VIEW_POSY"])
          else:
               v.ResetToMap()
               
          turn=1
          shot=False
     
          global player, player2
          player=room.GetObjectByName("player")
          player2=room.GetObjectByName("player2")
          v.FocusTo(room.GetObjectIdByName("player"))
          
          l=Listener(ScrollEnd)
          v.AddSubscriber(l,VIEW_SCROLLEND)
          
          ctrl2=room.GetControllerByObj(player2)
          ctrl2.LEFT=K_a
          ctrl2.RIGHT=K_d
          ctrl2.UP=K_w
          ctrl2.DOWN=K_s
          ctrl2.JUMP=K_z
          
          #put player at bottom
          room.MoveObjectIndex(player.id,len(room.objList))
          
          self.oListen.room=room
          self.oListen.Reload()
          
          global cs1, cs2
          cs1, cs2=[],[]
          cs1.append( (Wait, 30, 1) )
          cs1.append( (ScrollTo, (room.GetObjectByName("player2").id, 40), 1) )
          cs1.append( (v.FocusTo, (room.GetObjectByName("player2").id), 0) )
          cs1.append( (ChangeTurn, None, 0) )
          
          cs2.append( (Wait, 30, 1) )
          cs2.append( (ScrollTo, (room.GetObjectByName("player").id, 40), 1) )
          cs2.append( (v.FocusTo, (room.GetObjectByName("player").id), 0) )
          cs2.append( (ChangeTurn, None, 0) )
          
          healthBar.setVisible(True)
          healthBar.setMax(player.data["max_hp"])
          healthBar.setValue(player.data["current_hp"])
          
          angleLabel.setVisible(True)
          angleLabel.setCaption("Angle: "+str(player.data["angle"]))
          
          powerLabel.setVisible(True)
          powerLabel.setCaption("Power: "+str(player.data["power"]))
          
          powerSlider.setVisible(True)
          powerSlider.setValue(player.data["power"])
          
          pointLabel.setVisible(True)
          pointLabel.setCaption("Points: "+str(player.data["score"]))
          
          moveLabel.setVisible(True)
          moveLabel.setCaption("M: "+str(player.data["move"]))
          
          normalRadio.setVisible(True)
          
          fireballRadio.setVisible(True)
          fireballRadio.setCaption("(1)Fireball: "+str(player.data["fireball"]))
          
          terraRadio.setVisible(True)
          terraRadio.setCaption("(2)Terra: "+str(player.data["terra"]))
          
          dynamiteRadio.setVisible(True)
          dynamiteRadio.setCaption("(3)Dynamite: "+str(player.data["dynamite"]))
          
          spreadRadio.setVisible(True)
          spreadRadio.setCaption("(4)Spreadshot: "+str(player.data["spreadshot"]))
          
          spreadfireRadio.setVisible(True)
          spreadfireRadio.setCaption("(5)Spreadfire: "+str(player.data["spreadfire"]))
          
          moveRadio.setVisible(True)
          
          victoryLabel.setCaption("")
          
          global victory
          victory=False
          player.disabled=True
          player2.disabled=True
          
     def NextLevel(self, args=()):
          l=self.level
          self.level=SetBound(self.level+1,0,len(config["LEVELS"])-1)
          global CURRENTLEVELDIR, room
          CURRENTLEVELDIR=os.path.join(LEVELDIR,config["LEVELS"][self.level])
          
          if l != self.level:
               s.OnMessage("reloadlevel")
          
     def PrevLevel(self, args=()):
          l=self.level
          self.level=SetBound(self.level-1,0,len(config["LEVELS"])-1)
          global CURRENTLEVELDIR
          CURRENTLEVELDIR=os.path.join(LEVELDIR,config["LEVELS"][self.level])
          
          if l != self.level:
               s.OnMessage("reloadlevel")
          
     def ReloadLevel(self, args=()):
          pass
          
     def Update(self, args=()):
          global done, pause, player, player2, turn
          particle=room.particle
          clock.tick(30)
          room.key=pygame.key.get_pressed()
          room.mouse=pygame.mouse.get_pressed()
          for event in pygame.event.get():
               if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    done=True
               if event.type==KEYDOWN and event.key == K_F1:
                    self.PrevLevel()
               if event.type==KEYDOWN and event.key == K_F2:
                    s.OnMessage("reloadlevel")
               if event.type==KEYDOWN and event.key == K_F3:
                    self.NextLevel()
               if victory == False:
                    if event.type == MOUSEMOTION:
                         if event.buttons[2]:
                              if turn == 1:
                                   obj=player
                              else:
                                   obj=player2
                         
                              a=(event.pos[0]-v.posX+v.camX)-(obj.posX+(obj.width/2))
                              b=obj.posY-(event.pos[1]-v.posY+v.camY)
                              angle=0
                              if b >= 0:
                                   #find unit vector (||v||cos(t)i, ||v||sin(t)j), solve for theta
                                   magnitude=math.sqrt((a**2)+(b**2))
                                   unitcos=float(a)/float(magnitude)
                                   angle=int(math.degrees(math.acos(unitcos)))
                              else:
                                   if a>=0:
                                        angle=0
                                   else:
                                        angle=180
                              
                              obj.data["angle"]=angle
                         
                    elif event.type == MOUSEBUTTONDOWN:
                         if event.button==3:
                              if turn == 1:
                                   obj=player
                              else:
                                   obj=player2
                         
                              a=(event.pos[0]-v.posX+v.camX)-(obj.posX+(obj.width/2))
                              b=obj.posY-(event.pos[1]-v.posY+v.camY)
                              angle=0
                              if b >= 0:
                                   #find unit vector (||v||cos(t)i, ||v||sin(t)j), solve for theta
                                   magnitude=math.sqrt((a**2)+(b**2))
                                   unitcos=float(a)/float(magnitude)
                                   angle=int(math.degrees(math.acos(unitcos)))
                              else:
                                   if a>=0:
                                        angle=0
                                   else:
                                        angle=180
                              
                              obj.data["angle"]=angle

                    elif event.type == KEYDOWN:
                         if event.key == K_1:
                              obj=player if turn ==1 else player2
                              if obj.data["score"] >= 10:
                                   obj.data["score"]-=10
                                   obj.data["fireball"]+=1
                                   fireballRadio.setCaption("(1)Fireball: "+str(obj.data["fireball"]))
                                   pointLabel.setCaption("Points: "+str(obj.data["score"]))
                         
                         if event.key == K_2:
                              obj=player if turn ==1 else player2
                              if obj.data["score"] >= 15:
                                   obj.data["score"]-=15
                                   obj.data["terra"]+=1
                                   terraRadio.setCaption("(2)Terra: "+str(obj.data["terra"]))
                                   pointLabel.setCaption("Points: "+str(obj.data["score"]))
                              
                         if event.key == K_3:
                              obj=player if turn ==1 else player2
                              if obj.data["score"] >= 15:
                                   obj.data["score"]-=15
                                   obj.data["dynamite"]+=1
                                   dynamiteRadio.setCaption("(3)Dynamite: "+str(obj.data["dynamite"]))
                                   pointLabel.setCaption("Points: "+str(obj.data["score"]))
                                   
                         if event.key == K_4:
                              obj=player if turn ==1 else player2
                              if obj.data["score"] >= 20:
                                   obj.data["score"]-=20
                                   obj.data["spreadshot"]+=1
                                   spreadRadio.setCaption("(4)Spreadshot: "+str(obj.data["spreadshot"]))
                                   pointLabel.setCaption("Points: "+str(obj.data["score"]))
                              
                         if event.key == K_5:
                              obj=player if turn ==1 else player2
                              if obj.data["score"] >= 25:
                                   obj.data["score"]-=25
                                   obj.data["spreadfire"]+=1
                                   spreadfireRadio.setCaption("(5)Spreadfire: "+str(obj.data["spreadfire"]))
                                   pointLabel.setCaption("Points: "+str(obj.data["score"]))
                                   
                         if event.key == K_6:
                              obj=player if turn ==1 else player2
                              if obj.data["score"] >= 25:
                                   obj.data["score"]-=25
                                   obj.data["move"]+=200
                                   moveLabel.setCaption("M: "+str(obj.data["move"]))
                                   pointLabel.setCaption("Points: "+str(obj.data["score"]))
                                   
                         if event.key == K_p:
                              if pause == False:
                                   pause=True
                         
                              if v.focus != -1:
                                   v.FocusTo(-1)
                              
                              pos=pygame.mouse.get_pos()
                              if pos[0] <= v.posX+(v.width*TILEWIDTH) and pos[1] <= v.posY+(v.height*TILEHEIGHT):
                                   v.ScrollTo(v.camX+(pos[0]-v.posX)-(v.width*TILEWIDTH/2), v.camY+(pos[1]-v.posY)-(v.height*TILEHEIGHT/2), 20)
                                   room.particle.AddParticle("circle4",v.camX+(pos[0]-v.posX),v.camY+(pos[1]-v.posY),0,0,3.0,-0.05)
                         
                         strafejump=False
                         if event.key == K_LEFT:
                              obj=player if turn==1 else player2
                              if obj.data["move"]>=1 and room.key[K_SPACE]==False:
                                   obj.data["move"]-=1
                                   obj.disabled=False
                                   obj.GenerateAction(LEFT)
                                   obj.disabled=True
                                   moveLabel.setCaption("M: "+str(obj.data["move"]))
                              if room.key[K_SPACE]:
                                   strafejump=True
                                   
                         elif event.key == K_RIGHT:
                              obj=player if turn==1 else player2
                              if obj.data["move"]>=1 and room.key[K_SPACE]==False:
                                   obj.data["move"]-=1
                                   obj.disabled=False
                                   obj.GenerateAction(RIGHT)
                                   obj.disabled=True
                                   moveLabel.setCaption("M: "+str(obj.data["move"]))
                              if room.key[K_SPACE]:
                                   strafejump=True
                                   
                         elif room.key[K_SPACE]:
                              strafejump=True
                                   
                         if event.key == K_SPACE or strafejump:
                              obj=player if turn==1 else player2
                              if obj.data["move"]>=1:
                                   obj.data["move"]-=1
                                   room.particle.AddParticle("circle",obj.posX+(obj.width/2),obj.posY+(obj.height),0,0,3.0,0.0)
                                   obj.disabled=False
                                   if room.key[K_LEFT]:
                                        obj.GenerateAction(JUMP_LEFT)
                                   elif room.key[K_RIGHT]:
                                        obj.GenerateAction(JUMP_RIGHT)
                                   else:
                                        obj.GenerateAction(JUMP)
                                   obj.disabled=True
                                   moveLabel.setCaption("M: "+str(obj.data["move"]))
                    
                         global shot          
                         if event.key == K_RETURN and shot==False:
                              pos=pygame.mouse.get_pos()
                              #get relative position from object as a vector
                              if turn == 1: 
                                   obj=room.GetObjectByName("player")
                              elif turn == 2:
                                   obj=room.GetObjectByName("player2")
                              
                              #determine weapon.
                              cid=-1
                              if normalRadio.getSelected():
                                   cid=room.AddObject("cannonball",(obj.posX+(obj.width/2)),obj.posY-32,"",(obj.data["power"],obj.data["angle"],1,turn))
                              elif fireballRadio.getSelected():
                                   if obj.data["fireball"] >= 1:
                                        obj.data["fireball"]-=1
                                        fireballRadio.setCaption("(1)Fireball: "+str(obj.data["fireball"]))
                                        cid=room.AddObject("cannonball",(obj.posX+(obj.width/2)),obj.posY-32,"",(obj.data["power"],obj.data["angle"],2,turn))
                              elif terraRadio.getSelected():
                                   if obj.data["terra"] >= 1:
                                        obj.data["terra"]-=1
                                        terraRadio.setCaption("(2)Terra: "+str(obj.data["terra"]))
                                        cid=room.AddObject("cannonball",(obj.posX+(obj.width/2)),obj.posY-32,"",(obj.data["power"],obj.data["angle"],3,turn))
                              elif dynamiteRadio.getSelected():
                                   if obj.data["dynamite"] >= 1:
                                        obj.data["dynamite"]-=1
                                        dynamiteRadio.setCaption("(3)Dynamite: "+str(obj.data["dynamite"]))
                                        cid=room.AddObject("cannonball",(obj.posX+(obj.width/2)),obj.posY-32,"",(obj.data["power"],obj.data["angle"],4,turn))
                              elif spreadRadio.getSelected():
                                   if obj.data["spreadshot"] >= 1:
                                        obj.data["spreadshot"]-=1
                                        spreadRadio.setCaption("(4)Spreadshot: "+str(obj.data["spreadshot"]))
                                        cid=room.AddObject("cannonball",(obj.posX+(obj.width/2)),obj.posY-32,"",(obj.data["power"],obj.data["angle"],1,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))-24,obj.posY-32,"",(obj.data["power"],obj.data["angle"]+5,1,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))+24,obj.posY-32,"",(obj.data["power"],obj.data["angle"]-5,1,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))-48,obj.posY-32,"",(obj.data["power"],obj.data["angle"]+10,1,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))+48,obj.posY-32,"",(obj.data["power"],obj.data["angle"]-10,1,turn))
                              elif spreadfireRadio.getSelected():
                                   if obj.data["spreadfire"] >= 1:
                                        obj.data["spreadfire"]-=1
                                        spreadfireRadio.setCaption("(5)Spreadfire: "+str(obj.data["spreadfire"]))
                                        cid=room.AddObject("cannonball",(obj.posX+(obj.width/2)),obj.posY-32,"",(obj.data["power"],obj.data["angle"],2,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))-24,obj.posY-32,"",(obj.data["power"],obj.data["angle"]+5,2,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))+24,obj.posY-32,"",(obj.data["power"],obj.data["angle"]-5,2,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))-48,obj.posY-32,"",(obj.data["power"],obj.data["angle"]+10,2,turn))
                                        room.AddObject("cannonball",(obj.posX+(obj.width/2))+48,obj.posY-32,"",(obj.data["power"],obj.data["angle"]-10,2,turn))
                              if cid >= 0:
                                   v.FocusTo(cid)
                                   self.oListen.FollowProjectile(room.GetObjectById(cid))
                                   shot=True
                        
                    elif event.type == KEYUP:
                         if event.key == K_p:
                              pause=False
                         
                              if turn == 1:
                                   v.ScrollAndFocus(player.id)
                              else:
                                   v.ScrollAndFocus(player2.id)
               
               inputMessage.ChangeEvent(event)
               room.BroadcastMessage(inputMessage)
               input.pushInput(event)
               gui.logic()

          #Draw Everything
          if ~pause:
               room.UpdateControllers()
               room.Logic()

          screen.fill((0,0,0))
          v.Draw(screen)
          objturret=None
          if turn == 1:
               objturret=player
          else:
               objturret=player2
          
          #draw turret angle
          if objturret != None:
               x1=v.posX+(objturret.posX+(objturret.width/2)-v.camX)
               y1=v.posY+(objturret.posY-v.camY-16)
               x2=x1+(64*cos[objturret.data["angle"]])
               y2=y1-(64*sin[objturret.data["angle"]])
               
               screen.set_clip((v.posX,v.posY,v.width*TILEWIDTH,v.height*TILEHEIGHT))
               pygame.gfxdraw.line(screen, x1, y1, x2, y2, (255,255,255,255))
               screen.set_clip(None)
               
          #update angle label
          angleLabel.setCaption("Angle: "+str(objturret.data["angle"]))
               
          gui.draw()
          pygame.display.flip()
          main.total+=clock.get_fps()
          main.frame+=1
          
     def Stop(self, args=()):
          room.RemoveAll()
          StopCutscene()
     
     EventTable={ 'start': (Start, None),
                  'update': (Update, None),
                  'stop': (Stop, "splash"),
                  'reloadlevel': (ReloadLevel, "room") }
                  
class SplashState(State):
     def __init__(self):
          State.__init__(self,"splash",SplashState.EventTable)
          self.label=None
          
     def Start(self, args=()):
          if self.label == None:
               self.label=Label("Press space to begin Parametric Tanks!")
               self.label.setTextColor(Color(255,255,255))
               
          top.add(self.label, 100, 100)
          
     def Update(self, args=()):
          global done, pause
          clock.tick(30)
          room.key=pygame.key.get_pressed()
          room.mouse=pygame.mouse.get_pressed()
          for event in pygame.event.get():
               if event.type == QUIT:
                    done=True
               elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                         self.stop=True
                         
               input.pushInput(event)
               gui.logic()
          
          screen.fill((0,0,0))
          gui.draw()
          pygame.display.flip()
                         
     def Stop(self, args=()):
          top.remove(self.label)
          
     EventTable={ 'start': (Start, None),
                  'update': (Update, None),
                  'stop': (Stop, "room") }
     
def mainFunc():
     global s
     s=StateMachine()
     s.AddState(InitState())
     s.AddState(SplashState())
     s.AddState(RoomState())
     s.startState="init"
     s.Start()
     
     while done == False:
          s.Update()
     s.Stop()
          
          
#this calls the 'main' function when this script is executed
#if __name__ == '__main__': profile.run("mainFunc()","profile.txt")
#s=pstats.Stats(BASEDIR+"\profile.txt")
#s.sort_stats("cumulative")
#s.print_stats()
if __name__ == '__main__': mainFunc()
os.chdir(BASEDIR)
"""
m=MapData()
m.tileset.Create("tile3.bmp","main",32,32)
m.tileset.SetColorKey(Color(255,0,255))
m.CreateTileTemplate("SPACE",0,True,False,False,False,-1.0)
m.CreateTileTemplate("LAND_MIDDLE",1,False,False,False,False,1.0)
m.CreateTileTemplate("LAND_SLOPELEFT",2,False,False,False,False,1.0)
m.CreateTileTemplate("LAND_SLOPERIGHT",3,False,False,False,False,1.0)
m.SaveTemplates("templates.tmp")
spr=Sprite()
spr.CreateFromFile("tank1.bmp","tank1",64,32)
spr.SetColorKey(Color(255,0,255))
o=ObjectType("player1")
o.SetSprite(spr)
o.controller="player"
o.maxVelX=4.0
o.maxVelY=4.0
o.accelX=0.5
o.accelY=0.5
o.jumpStart=4.0
o.jumpHeight=128.0
o.fall=True
o.collision=GHOST
o.group=PLAYER
o.data["max_hp"]=10
o.data["current_hp"]=10
o.data["points"]=0
o.data["normal"]=5
o.data["fireball"]=1
o.data["seeker"]=0
o.Save("player1.obj")
"""