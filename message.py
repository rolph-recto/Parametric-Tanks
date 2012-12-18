#!/usr/bin/env python

from main import *
from message_types import *

class Message:
    "Base class for all Message objects"
    def __init__(self,type=0):
        self.type=type
        
    def Compare(self,msg):
        return self.__class__ == msg.__class__
        
class Subscription:
    "Used when Listeners subscribe to Dispatchers"
    def __init__(self,subscriber,filter=MSG_NONE):
        self.subscriber=subscriber
        #if filter is just one message
        if type(filter)==type(0):
            self.filter=MSG(filter)
        #else, we assume that it is a range
        else:
            self.filter=filter
            
class Dispatcher:
    "Dispatches messages to Listeners"
    def __init__(self):
        self.subscribers=[]
    
    def AddSubscriber(self,subscriber,filter=None):
        for i in self.subscribers:
            if i.subscriber==subscriber:
                return None
    
        s=None
        
        if filter != None:
            s=Subscription(subscriber,filter)
            
        elif "MSG_FILTER" in dir(subscriber.__class__):
            s=Subscription(subscriber,subscriber.__class__.MSG_FILTER)
            
        else:
            s=Subscription(subscriber,MSG_ALL)
            
        self.subscribers.append(s)

    def RemoveSubscriber(self,subscriber):
        for i in self.subscribers[:]:
            if i.subscriber==subscriber:
                self.subscriber.remove(i)
                
    def RemoveAllSubscribers(self):
        while len(self.subscribers)>0:
            self.subscribers.pop()

    def EditSubscription(self,subscriber,filter):
        for i in self.subscribers[:]:
            if i.subscriber==subscriber:
                i.filter=filter
                
    def IsSubscribed(self,subscriber,filter=MSG_NONE):
         for i in self.subscribers[:]:
            if i.subscriber==subscriber:
                if filter==MSG_NONE:
                    return True
                else:
                    return ( (i.filter&filter)==True )
                
    def SendMessage(self,receiver,message):
        if MSG_HOOK[message.type] in dir(receiver):
            getattr(receiver,MSG_HOOK[message.type])(message)
                
        elif MSG_DEFAULT_CALLBACK in dir(receiver):
            getattr(receiver,MSG_DEFAULT_CALLBACK)(message)        
    
    def BroadcastMessage(self,m):
        for i in self.subscribers[:]:
            if i.filter.Test(m.type):
                self.SendMessage(i.subscriber,m)

                
                
class Listener:
    "Base class for objects that listen to events."
    MSG_FILTER=MSG_ALL
    def __init__(self,f=None):
        self.func=1
        if f != None:
            self.func=f
    
    def OnMessage(self,m):
        if self.func != 1:
          self.func(m)
        else:
            pass
    
    def SetProcessFunc(self,f):
        self.func=f
