#!/usr/bin/env python

import inspect
from inspect import currentframe

class Exception:
    def __init__(self,msg,file,line):
        self.mMessage=msg
        self.mFilename=file
        self.mLine=line
        
    def __str__(self):
        return "Exception at "+str(self.mFilename)+" line "+str(self.mLine)+": "+self.mMessage
        
    def getMessage(self):
        return self.mMessage
    
    def getFilename(self):
        return self.mFilename

    def getLine(self):
        return self.mLine

def GCN_EXCEPTION(msg):
    return Exception(msg,inspect.stack()[1][1:3][0],inspect.stack()[1][1:3][1])