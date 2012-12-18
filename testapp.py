#!/usr/bin/env python

from room import *
from pickle import *
from guichan import *
from guichan.container import *
from guichan.button import *
from pygame import mixer

from view import *

key=None
pause=False
notice=True

class ObjectListener(Listener):
     def __init__(self, room):
          self.room=room
          self.max_points=0
          self.Reload()
          
     def Reload(self):
          self.max_points=0
          for i in self.room.objList:
               if i.name == "player":
                    i.AddSubscriber(self,MSG_ALL)
               if i.type.name == "door":
                    i.AddSubscriber(self,OBJECT)
               if i.type.name == "key":
                    i.AddSubscriber(self,OBJECT)
               if i.type.name == "diamond":
                    self.max_points=self.max_points+1
          
          
     def OnPlayerHit(self,message):
          Notify("Player hit! HP left: "+str(message.obj.data["currentHP"]))
          self.room.AddAlarm(self,150,1)
          
     def OnPlayerDied(self,message):
          Notify("Player died!")
          self.room.AddAlarm(self,150,1)
          
     def OnPlayerScored(self,message):
          if message.obj.data["score"] >= self.max_points:
               Notify("Got all the diamonds!")
               self.room.AddAlarm(self,150,2)
          else:     
               Notify("Got diamond, "+str(self.max_points-message.obj.data["score"])+" left! Player score: "+str(message.obj.data["score"]))
               self.room.AddAlarm(self,150,1)
          
     def OnObjectLocked(self,message):
          Notify("Door locked!")
          self.room.AddAlarm(self,150,1)
          
     def OnObjectOpened(self,message):
          o=self.room.GetObjectByName("player")
          Notify("Door unlocked! Keys left: "+str(o.data["keys"]))
          self.room.AddAlarm(self,150,1)
          
     def OnObjectCollision(self,message):
          if message.obj.type.name == "key":
               o=self.room.GetObjectByName("player")
               Notify("Got key! Have "+str(o.data["keys"])+" now.")
               self.room.AddAlarm(self,150,1)
          
     def OnAlarm(self,message):
          if message.data == 1:
               Notify("")
          if message.data == 2:
               NextLevel()
          
def LoadLevel(level):
     global levels, currentLevel
     if level < len(levels):
          currentLevel=level
          CURRENTLEVELDIR=os.path.join(LEVELDIR, levels[currentLevel])
          execfile(os.path.join(CURRENTLEVELDIR,"level.py"))
          v.ResetToMap(16, 11)
          SetPause(True)
          if notice:
               noticeWin.setVisible(True)
          
def NextLevel():
     global levels, currentLevel
     currentLevel=currentLevel+1
     if currentLevel >= len(levels):
          currentLevel=len(levels)-1
          
     LoadLevel(currentLevel)
          
def PreviousLevel():
     global levels, currentLevel
     currentLevel=currentLevel-1
     if currentLevel < 0:
          currentLevel=0
          
     LoadLevel(currentLevel)

def Notify(caption):
     global notifyLabel
     notifyLabel.setCaption(caption)
     notifyLabel.setPosition(256-(notifyLabel.getWidth()/2), 384)
     
def NoticeText(text):
     global noticeText
     noticeText.setText(text)
     
def OnAction(action):
     id=action.getId()
     if id == "NoticeOK":
          SetPause(False)
          noticeWin.setVisible(False)
          
def IsPaused():
     global pause
     return pause

def SetPause(pauses):
     global pause
     pause=pauses
     
def mainFunc():
     os.chdir(BASEDIR)
     pygame.init()
     pygame.display.set_caption("Nibor Dooh in King Arthur's Castle", "Nibor")
     global screen
     screen = pygame.display.set_mode((512, 416))
     
     pygame.mixer.init()
     
     global room
     room=Room()
     room.map=MapData(100,100)
     global mappy
     mappy=room.map
     mappy.LoadTemplates("templates.tmp")
     
     room.database.LoadXML("resource.txt")
     
     global v
     v=RoomView(room,16,11)
     v.SetPosition(0,32)
     focus=None
     
     clock = pygame.time.Clock()
     pygame.key.set_repeat(1, 1)
     inputMessage=InputMessage(None)
     #Main Loop
     total=0
     lastX=-1
     lastY=-1

     g=gui.Gui()
     i=pygameInput.PygameInput()
     image.Image.mImageLoader=pygameImageLoader.PygameImageLoader()
     gr=pygameGraphics.PygameGraphics()
     gr.setTarget(screen)
     f=imageFont.ImageFont("consolefont.bmp")
     f.setColorkey( Color(255,0,255) )
     f.setGlyphSpacing(2)
     f2=imageFont.ImageFont("consolefont2.bmp")
     f2.setColorkey( Color(255,0,255) )
     f2.setGlyphSpacing(2)
     widget.Widget.setGlobalFont(f)
     c=Container()
     c.setOpaque(False)
     c.setPosition(0,0)
     c.setSize(640,480)
     c.setBaseColor( Color(255,0,0,255) )   
     g.setInput(i)
     g.setTop(c)
     g.setGraphics(gr)
     
     global action
     action=ActionListener()
     action.action=OnAction
     
     global notifyLabel
     notifyLabel=Label("")
     notifyLabel.setFont(f2)
     notifyLabel.setPosition(256-(notifyLabel.getWidth()/2), 384)
     c.add(notifyLabel)
     
     global noticeWin, noticeText, noticeScroll, noticeButton
     noticeWin=Window("")
     noticeText=TextBox("This is a Notice")
     noticeText.adjustSize()
     noticeText.setOpaque(False)
     noticeText.setEditable(False)
     noticeScroll=ScrollArea(noticeText)
     noticeScroll.setSize(250, 288)
     noticeScroll.setOpaque(False)
     noticeButton=Button("OK")
     noticeButton.setBaseColor(Color(219,219,219))
     noticeButton.setActionEventId("NoticeOK")
     noticeButton.addActionListener(action)
     noticeButton.adjustSize()
     
     noticeWin.add(noticeScroll,0,0)
     noticeWin.add(noticeButton,0,20+noticeScroll.getHeight())
     noticeWin.setPadding(10)
     noticeWin.resizeToContent()
     noticeButton.setPosition(112,300)
     noticeWin.setPosition(256-(noticeWin.getWidth()/2), 32)
     noticeWin.setMovable(False)
     noticeWin.setVisible(True)
     c.add(noticeWin)
     noticeWin.setBaseColor(Color(219,219,219))
     noticeWin.setForegroundColor(Color(219,219,219))
     noticeWin.setBackgroundColor(Color(219,219,219))
     noticeWin.setSelectionColor(Color(219,219,219))
     
     #levels
     global levels, currentLevel
     levels=["one","two","three","four","five","end"]
     currentLevel=0
     global CURRENTLEVELDIR
     
     global oListen
     oListen=ObjectListener(room)
     LoadLevel(currentLevel)
     
     global pause, done, key
     done=False
     key=pygame.key.get_pressed()
     while done == False:
          clock.tick(30)
          key=pygame.key.get_pressed()
          for event in pygame.event.get():
               if event.type == QUIT:
                    done=True
               elif event.type == KEYDOWN:
                    if event.key == K_F1:
                         PreviousLevel()
                    elif event.key == K_F2:
                         LoadLevel(currentLevel)
                    elif event.key == K_F3:
                         NextLevel()                         
                    """
                    if event.key == K_F1:
                         mappy.Save("MAP1.TXT")
                    if event.key == K_z:
                        mappy.Resize(mappy.width-1, mappy.height, 0)
                        v.ResetToMap()
                    if event.key == K_x:
                        mappy.Resize(mappy.width+1, mappy.height, 0)
                        v.ResetToMap()
                    if event.key == K_c:
                        mappy.Resize(mappy.width, mappy.height-1, 0)
                        v.ResetToMap()
                    if event.key == K_v:
                        mappy.Resize(mappy.width, mappy.height+1, 0)     
                        v.ResetToMap()     
                    if event.key == K_m:
                         if focus == None:
                              focus=room.GetObject(bob)
                         else:
                              focus=None
                    
                    if event.key == K_w:
                        v.SetCamPosition(v.camX,v.camY-10)
                    if event.key == K_s:
                        v.SetCamPosition(v.camX,v.camY+10)
                    if event.key == K_a:
                        v.SetCamPosition(v.camX-10,v.camY)
                    if event.key == K_d:
                        v.SetCamPosition(v.camX+10,v.camY)
                    if event.key == K_q:
                        v.SetAlpha(v.alpha-10)
                    if event.key == K_e:
                        v.SetAlpha(v.alpha+10)
                        
                    if event.key == K_F1:
                         if pause:
                              pygame.mixer.music.unpause()
                              pause=False
                         else:
                              pygame.mixer.music.pause()
                              pause=True
                    """    
                    if event.key == K_ESCAPE:
                        done=True
                        
               elif event.type == MOUSEBUTTONDOWN:
                    """
                    if event.button == 1:
                         if event.pos[0] <= v.posX+(v.width*TILEWIDTH) and event.pos[1] <= v.posY+(v.height*TILEHEIGHT):
                              mappy.SetBase( int((v.camX+(event.pos[0]-v.posX))/TILEWIDTH), int((v.camY+(event.pos[1]-v.posY))/TILEHEIGHT), 1)
                    if event.button == 3:
                         if event.pos[0] <= v.posX+(v.width*TILEWIDTH) and event.pos[1] <= v.posY+(v.height*TILEHEIGHT):
                              mappy.SetBase( int((v.camX+(event.pos[0]-v.posX))/TILEWIDTH), int((v.camY+(event.pos[1]-v.posY))/TILEHEIGHT), 0)
                    elif event.button == 2:
                         lastX=event.pos[0]
                         lastY=event.pos[1]
                    """
                         
               elif event.type == MOUSEMOTION:
                    """
                    if event.buttons[0] == 1:
                         if event.pos[0] <= v.posX+(v.width*TILEWIDTH) and event.pos[1] <= v.posY+(v.height*TILEHEIGHT):
                              mappy.SetBase( int((v.camX+(event.pos[0]-v.posX))/TILEWIDTH), int((v.camY+(event.pos[1]-v.posY))/TILEHEIGHT), 1)
                    if event.buttons[2] == 1:
                         if event.pos[0] <= v.posX+(v.width*TILEWIDTH) and event.pos[1] <= v.posY+(v.height*TILEHEIGHT):
                              mappy.SetBase( int((v.camX+(event.pos[0]-v.posX))/TILEWIDTH), int((v.camY+(event.pos[1]-v.posY))/TILEHEIGHT), 0)                      
                    if event.buttons[1] == 1:
                         if lastX >= 0 and lastY >= 0:
                              v.SetCamPosition(v.camX-(event.pos[0]-lastX), v.camY-(event.pos[1]-lastY))
                              lastX=event.pos[0]
                              lastY=event.pos[1]
                    """
                           
               elif event.type == MOUSEBUTTONUP:
                    lastX=-1
                    lastY=-1
               
               inputMessage.ChangeEvent(event)
               i.pushInput(event)
               g.logic()
               if IsPaused() == False:
                    room.BroadcastMessage(inputMessage)

          #Draw Everything
          if IsPaused() == False:
               room.UpdateControllers()
               room.UpdateAlarms()
               room.Logic()
               
          screen.fill((0,0,0), (0, 384, 512, 32))
          global focus
          v.FocusTo(focus)
          v.Draw(screen)
          g.draw()
          pygame.display.flip()
          total=total+clock.get_fps()
          main.frame=main.frame+1
          
     print "FPS:", total/main.frame
     
     pygame.mixer.quit()
          
          
#this calls the 'main' function when this script is executed
if __name__ == '__main__': mainFunc()
