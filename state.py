#!/usr/bin/env python
from message import *
from message_class import *
#
class State(Listener):
     def __init__(self,name,eventDict={}):
          self.name=name
          #transition consists of:
          #the key is the message
          #the value is a 2-tuple as such: (action, transitionState)
          self.event=eventDict
          self.stop=True
          
     def OnMessage(self, message, args=()):
          if message in self.event:
               if message == "start":
                    self.stop=False
               if message == "stop":
                    self.stop=True
                    
               #run action function
               self.event[message][0](self, args)
               #return transition state
               return self.event[message][1]

class StateMachine(Dispatcher):
     def __init__(self):
          Dispatcher.__init__(self)
          self.stateList={}
          self.currentState=None
          self.startState=None
          
     def Start(self):
          self.SetState(self.startState)
     
     def AddState(self,name,transitionDict={}):
          if type(name) == type("abc"):
               state=State(name,transitionDict)
               self.stateList[name]=state
               
          else:
               self.stateList[name.name]=name
          
     def RemoveState(self,name):
          if name in self.stateList:
               if name == self.currentState:
                    self.OnMessage("stop")
                    
               del self.stateList[name]
     
     def SetState(self,newState):
          if newState in self.stateList:
               if self.currentState != None:
                    if self.stateList[self.currentState].stop == False:
                         self.stateList[self.currentState].OnMessage("stop")
                    
               self.currentState=newState
               self.OnMessage("start")
               
     def OnMessage(self,message,args=()):
          transition=self.stateList[self.currentState].OnMessage(message,args)
          self.BroadcastMessage(StateMessage(STATE_ONMESSAGE,self.stateList[self.currentState],self,message))
          if transition != None:
               self.SetState(transition)
          
     def Stop(self):
          self.OnMessage("stop")
          self.BroadcastMessage(StateMessage(STATE_STOP,self.stateList[self.currentState],self))
          
     def Update(self):
          self.OnMessage("update")
          self.BroadcastMessage(StateMessage(STATE_UPDATE,self.stateList[self.currentState],self))
          if self.stateList[self.currentState].stop:
              self.OnMessage("stop")