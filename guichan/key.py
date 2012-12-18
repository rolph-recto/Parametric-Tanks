#!/usr/bin/env python

from guichan import *

class Key:
    def __init__(self,val=0):
        if type(val) != type(0):
            self.mValue=ord(val)
        else:
            self.mValue=val
    
    def __str__(self):
        if self.mValue <= 255:
            return "Key [value="+chr(self.mValue)+", ASCII code="+str(self.mValue)+"]"
        else:
            return "Key [ASCII code="+str(self.mValue)+"]"
    
    def isCharacter(self):
        return (self.mValue >= 32 and self.mValue <= 126) or (self.mValue >= 162 and self.mValue <= 255) or (self.mValue == 9)
    
    def isNumber(self):
        return self.mValue >= 48 and self.mValue <= 57
    
    def isLetter(self):
        return ( ((self.mValue >= 65 and self.mValue <= 90) or (self.mValue >= 97 and self.mValue <= 122) or (self.mValue >= 192 and self.mValue <= 255)) and (self.mValue != 215) and (self.mValue != 247) )
    
    def getValue(self):
        return self.mValue
    
    def __eq__(self,other):
        if type(self) == type(other):
            return self.mValue == other.getValue()
        else:
            return self.mValue == other
        
    def __ne__(self,other):
        if type(self) == type(other):
            return self.mValue != other.getValue()
        else:
            return self.mValue != other
        
    SPACE              = 32
    TAB                = 9
    ENTER              = 10
    LEFT_ALT           = 1000
    RIGHT_ALT          = 1001
    LEFT_SHIFT         = 1002
    RIGHT_SHIFT        = 1003
    LEFT_CONTROL       = 1004
    RIGHT_CONTROL      = 1005
    LEFT_META          = 1006
    RIGHT_META         = 1007
    LEFT_SUPER         = 1008
    RIGHT_SUPER        = 1009
    INSERT             = 1010
    HOME               = 1011
    PAGE_UP            = 1012
    DELETE             = 1013
    END                = 1014
    PAGE_DOWN          = 1015
    ESCAPE             = 1016
    CAPS_LOCK          = 1017
    CAPSLOCK           = 1017
    BACKSPACE          = 1018
    F1                 = 1019
    F2                 = 1020
    F3                 = 1021
    F4                 = 1022
    F5                 = 1023
    F6                 = 1024
    F7                 = 1025
    F8                 = 1026
    F9                 = 1027
    F10                = 1028
    F11                = 1029
    F12                = 1030
    F13                = 1031
    F14                = 1032
    F15                = 1033
    PRINT_SCREEN       = 1034
    PRINTSCREEN        = 1034
    SCROLL_LOCK        = 1035
    SCROLLLOCK         = 1035
    PAUSE              = 1036
    NUM_LOCK           = 1037
    NUMLOCK            = 1037
    ALT_GR             = 1038
    LEFT               = 1039
    RIGHT              = 1040
    UP                 = 1041
    DOWN               = 1042


