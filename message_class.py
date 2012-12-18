#!/usr/bin/env python

import main
from message import *

#event messages
#InputMessage class
INPUT_START               = 0
INPUT_END                 = INPUT_START+4
INPUT                     = MSG_RANGE(INPUT_START,INPUT_END)

INPUT_KEY                 = MSG_RANGE(INPUT_START,INPUT_START+1)
INPUT_KEYDOWN             = INPUT_START+0
INPUT_KEYUP               = INPUT_START+1

INPUT_MOUSE               = MSG_RANGE(INPUT_START+2,INPUT_START+4)
INPUT_MOUSEBUTTONDOWN     = INPUT_START+2
INPUT_MOUSEBUTTONUP       = INPUT_START+3
INPUT_MOUSEMOTION         = INPUT_START+4

#ObjectMessage class
OBJECT_START              = INPUT_END+1
OBJECT_END                = OBJECT_START+9
OBJECT                    = MSG_RANGE(OBJECT_START,OBJECT_END)

OBJECT_CREATED            = OBJECT_START+0
OBJECT_DESTROYED          = OBJECT_START+1
OBJECT_MOVED              = OBJECT_START+2
OBJECT_JUMPED             = OBJECT_START+3
OBJECT_FELL               = OBJECT_START+4
OBJECT_LANDED             = OBJECT_START+5
OBJECT_COLLISION          = OBJECT_START+6
OBJECT_ACTION             = OBJECT_START+7
OBJECT_OPENED             = OBJECT_START+8
OBJECT_LOCKED             = OBJECT_START+9

#PlayerMessage class
PLAYER_START              = OBJECT_END+1
PLAYER_END                = PLAYER_START+2
PLAYER                    = MSG_RANGE(PLAYER_START,PLAYER_END)

PLAYER_HIT                = PLAYER_START+0
PLAYER_DIED               = PLAYER_START+1
PLAYER_SCORED             = PLAYER_START+2

#ControllerMessage class
CONTROLLER_START          = PLAYER_END+1
CONTROLLER_END            = CONTROLLER_START+1
CONTROLLER                = MSG_RANGE(CONTROLLER_START,CONTROLLER_END)

CONTROLLER_CREATED        = CONTROLLER_START+0
CONTROLLER_DESTROYED      = CONTROLLER_START+1

#AlarmMessage class
ALARM_START               = CONTROLLER_END+1
ALARM_END                 = ALARM_START

ALARM                     = ALARM_START+0

#StateMessage class
STATE_START               = ALARM_END+1
STATE_END                 = STATE_START+3
STATE                     = MSG_RANGE(STATE_START,STATE_END)

STATE_INITIALIZE          = STATE_START+0
STATE_UPDATE              = STATE_START+1
STATE_ONMESSAGE           = STATE_START+2
STATE_STOP                = STATE_START+3

#ViewMessage class
VIEW_START                = STATE_END+1
VIEW_END                  = VIEW_START+6
VIEW                      = MSG_RANGE(VIEW_START,VIEW_END)

VIEW_RESIZE               = VIEW_START+0
VIEW_FOCUS                = VIEW_START+1
VIEW_FOCUSLOST            = VIEW_START+2
VIEW_SCROLLSTART          = VIEW_START+3
VIEW_SCROLLEND            = VIEW_START+4
VIEW_FADESTART            = VIEW_START+5
VIEW_FADEEND              = VIEW_START+6
VIEW_DRAW                 = VIEW_START+7

#message hooks/callback function names
MSG_HOOK[INPUT_KEYDOWN]                  = "OnKeyDown"
MSG_HOOK[INPUT_KEYUP]                    = "OnKeyUp"

MSG_HOOK[INPUT_MOUSEBUTTONDOWN]          = "OnMouseButtonDown"
MSG_HOOK[INPUT_MOUSEBUTTONUP]            = "OnMouseButtonUp"
MSG_HOOK[INPUT_MOUSEMOTION]              = "OnMouseMotion"

MSG_HOOK[OBJECT_CREATED]                 = "OnObjectCreate"
MSG_HOOK[OBJECT_DESTROYED]               = "OnObjectDestroy"
MSG_HOOK[OBJECT_MOVED]                   = "OnObjectMove"
MSG_HOOK[OBJECT_JUMPED]                  = "OnObjectJump"
MSG_HOOK[OBJECT_FELL]                    = "OnObjectFall"
MSG_HOOK[OBJECT_LANDED]                  = "OnObjectLand"
MSG_HOOK[OBJECT_COLLISION]               = "OnObjectCollision"
MSG_HOOK[OBJECT_ACTION]                  = "OnObjectAction"
MSG_HOOK[OBJECT_OPENED]                  = "OnObjectOpened"
MSG_HOOK[OBJECT_LOCKED]                  = "OnObjectLocked"

MSG_HOOK[PLAYER_HIT]                     = "OnPlayerHit"
MSG_HOOK[PLAYER_DIED]                    = "OnPlayerDied"
MSG_HOOK[PLAYER_SCORED]                  = "OnPlayerScored"

MSG_HOOK[CONTROLLER_CREATED]             = "OnControllerCreation"
MSG_HOOK[CONTROLLER_DESTROYED]           = "OnControllerDestruction"

MSG_HOOK[ALARM]                          = "OnAlarm"

MSG_HOOK[STATE_INITIALIZE]               = "OnStateInitialization"
MSG_HOOK[STATE_UPDATE]                   = "OnStateUpdate"
MSG_HOOK[STATE_ONMESSAGE]                = "OnStateMessage"
MSG_HOOK[STATE_STOP]                     = "OnStateStop"

MSG_HOOK[VIEW_RESIZE]                    = "OnViewResize"
MSG_HOOK[VIEW_FOCUS]                     = "OnViewFocus"
MSG_HOOK[VIEW_FOCUSLOST]                 = "OnViewFocusLost"
MSG_HOOK[VIEW_SCROLLSTART]               = "OnViewScrollStart"
MSG_HOOK[VIEW_SCROLLEND]                 = "OnViewScrollEnd"
MSG_HOOK[VIEW_FADESTART]                 = "OnFadeStart"
MSG_HOOK[VIEW_FADEEND]                   = "OnFadeEnd"
MSG_HOOK[VIEW_DRAW]                      = "OnViewDraw"

#Message classes
#INPUT_KEYDOWN
#INPUT_KEYUP
#INPUT_MOUSEBUTTONDOWN
#INPUT_MOUSEBUTTONUP
#INPUT_MOUSEMOTION
class InputMessage(Message):
     def __init__(self,event):
          self.ChangeEvent(event)
          
     def ChangeEvent(self,event):
          self.event=event
          if event != None:
               if event.type == KEYDOWN:
                    self.type=INPUT_KEYDOWN
               elif event.type == KEYUP:
                    self.type=INPUT_KEYUP
               elif event.type == MOUSEBUTTONDOWN:
                    self.type=INPUT_MOUSEBUTTONDOWN
               elif event.type == MOUSEBUTTONUP:
                    self.type=INPUT_MOUSEBUTTONUP          
               elif event.type == MOUSEMOTION:
                    self.type=INPUT_MOUSEMOTION
               else:
                    self.type=MSG_NONE

          else:
               self.type=MSG_NONE


#OBJECT_CREATED
#OBJECT_DESTROYED
#OBJECT_MOVED
#OBJECT_JUMPED
#OBJECT_FELL
#OBJECT_LANDED
#OBJECT_COLLISION
#OBJECT_ACTION

#Collision types
COLLISION_THUD   = 0 #solid object v. solid object
COLLISION_PASS   = 1 #ghost object v. ghost object
COLLISION_IMPACT = 2 #solid object v. ghost object
COLLISION_WALL   = 3 #object hits wall

class ObjectMessage(Message):
     def __init__(self,obj,type,args=()):
          self.type=type
          self.obj=obj
          self.args=args
          
          if self.type == OBJECT_COLLISION:
               self.obj2=args[0]
               self.collision_type=args[1]
          elif self.type == OBJECT_ACTION:
               if len(args) > 0:
                    self.action_obj=args[0]
          
     def Compare(self,msg):
          return self.obj == msg.obj

#PLAYER_HIT
#PLAYER_DIED
#PLAYER_SCORED
class PlayerMessage(Message):
     def __init__(self,obj,type,args=()):
          self.type=type
          self.obj=obj
          
     def Compare(self,msg):
          return self.obj == msg.obj

#CONTROLLER_CREATED
#CONTROLLER_DESTROYED
class ControllerMessage(Message):
     def __init__(self,controller,type):
          self.type=type
          self.controller=controller
          
     def Compare(self,msg):
          return self.controller == msg.controller
     
#Alarm
class AlarmMessage(Message):
     def __init__(self,listener,time,data,loop=-1):
          self.type=ALARM
          self.listener=listener
          self.startFrame=main.frame
          self.time=time
          self.iterations=0
          self.loop=loop
          self.data=data
          
#STATE_START
#STATE_UPDATE
#STATE_ONMESSAGE
#STATE_STOP
class StateMessage(Message):
     def __init__(self,type,state,sm=None,message=""):
          self.type=type
          self.state=state
          self.stateMachine=sm
          self.message=message
          
class ViewMessage(Message):
     def __init__(self,type,view):
          self.type=type
          self.view=view
          
          