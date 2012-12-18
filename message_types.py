#!/usr/bin/env python

from utilities import *

MAX_MESSAGE_TYPE = 128

def MSG_RANGE(start,end,size=MAX_MESSAGE_TYPE):
    b=Bitset()
    b.Resize(size)
    b.Reset()
    if start>-1 and end>start:
          i=0
          while i<=end-start and start+i<b.Size():
               b[start+i]=1
               i=i+1
    return b

def MSG(a,size=MAX_MESSAGE_TYPE):
    b=Bitset()
    b.Resize(size)
    b.Reset()
    if a>-1 and a<MAX_MESSAGE_TYPE:
        b[a]=1
    return b

#messages and message ranges
MSG_NONE                  = -1
MSG_ALL                   = MSG_RANGE(0,MAX_MESSAGE_TYPE)
		
#message hooks/callback function names
MSG_DEFAULT_CALLBACK = "OnMessage"
MSG_HOOK=[]
#set default callback function to "OnMessage"
for i in range(MAX_MESSAGE_TYPE):
    MSG_HOOK.append(MSG_DEFAULT_CALLBACK)




