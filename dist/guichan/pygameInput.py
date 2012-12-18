#!/usr/bin/env python

import pygame
from pygame.locals import *

from exception import *
from input import Input
from key import Key
from keyInput import KeyInput
from mouseInput import MouseInput

class PygameInput(Input):
    def __init__(self):
        self.mMouseInWindow=True
        self.mMouseDown=False
        self.mKeyInputQueue=[]
        self.mMouseInputQueue=[]
        self.mLastUnicode=None
        
    def isKeyQueueEmpty(self):
        return len(self.mKeyInputQueue) == 0
    
    def dequeueKeyInput(self):
        if len(self.mKeyInputQueue) == 0:
            raise GCN_EXCEPTION("Key input queue is empty.")
        else:
            keyInput=self.mKeyInputQueue.pop(0)
            return keyInput
        
    def isMouseQueueEmpty(self):
        return len(self.mMouseInputQueue) == 0
    
    def dequeueMouseInput(self):
        if len(self.mMouseInputQueue) == 0:
            raise GCN_EXCEPTION("Mouse input queue is empty.")
        else:
            mouseInput=self.mMouseInputQueue.pop(0)
            return mouseInput
        
    def pushInput(self,event):
        keyInput=KeyInput(0,0)
        mouseInput=MouseInput()
        if event.type == KEYDOWN or event.type == KEYUP:
            value = self.convertPygameEventToGuichanKeyValue(event)
            if value < 0:
                if event.type == KEYDOWN:
                    self.mLastUnicode=event.unicode
                if len(self.mLastUnicode) > 0:
                    value = ord(self.mLastUnicode)
                
            keyInput.setKey(Key(value))
            keyInput.setShiftPressed(event.mod & KMOD_SHIFT)
            keyInput.setControlPressed(event.mod & KMOD_CTRL)
            keyInput.setAltPressed(event.mod & KMOD_ALT)
            keyInput.setMetaPressed(event.mod & KMOD_META)
                
            if event.type == KEYDOWN:
                keyInput.setType(KeyInput.PRESSED)
            else:
                keyInput.setType(KeyInput.RELEASED)
                
            self.mKeyInputQueue.append(keyInput)
                
        elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            mouseInput.setX(event.pos[0])
            mouseInput.setY(event.pos[1])
            mouseInput.setButton(self.convertMouseButton(event.button))
            mouseInput.setTimeStamp(pygame.time.get_ticks())
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 5:
                    mouseInput.setType(MouseInput.WHEEL_MOVED_DOWN)
                elif event.button == 4:
                    mouseInput.setType(MouseInput.WHEEL_MOVED_UP)
                else:
                    mouseInput.setType(MouseInput.PRESSED)
                self.mMouseDown = True
            else:
                mouseInput.setType(MouseInput.RELEASED)
                self.mMouseDown = False
                
            self.mMouseInputQueue.append(mouseInput)
            
        elif event.type == MOUSEMOTION:
            mouseInput.setX(event.pos[0])
            mouseInput.setY(event.pos[1])
            mouseInput.setButton(MouseInput.EMPTY)
            mouseInput.setTimeStamp(pygame.time.get_ticks())
            mouseInput.setType(MouseInput.MOVED)
            self.mMouseInputQueue.append(mouseInput)
            
        elif event.type == ACTIVEEVENT:
            if event.state&1 and event.gain == False:
                self.mMouseInWindow=False
                
                if self.mMouseDown == False:
                    mouseInput.setX(-1)
                    mouseInput.setY(-1)
                    mouseInput.setButton(MouseInput.EMPTY)
                    mouseInput.setTimeStamp(pygame.time.get_ticks())
                    mouseInput.setType(MouseInput.MOVED)
                    self.mMouseInputQueue.append(mouseInput)
            
            elif event.state&1 and event.gain == True:
                self.mMouseInWindow=True
                
    
    def convertMouseButton(self,button):
        if button == 1:
            return MouseInput.LEFT
        
        elif button == 2:
            return MouseInput.MIDDLE
        
        elif button == 3:
            return MouseInput.RIGHT
        
        else:
            return button
        
    def convertPygameEventToGuichanKeyValue(self,event):
        value=-1
        if event.key == K_TAB:
            value=Key.TAB
            
        elif event.key == K_LALT:
            value=Key.LEFT_ALT
            
        elif event.key == K_RALT:
            value=Key.RIGHT_ALT
             
        elif event.key == K_LSHIFT:
            value=Key.LEFT_SHIFT
            
        elif event.key == K_RSHIFT:
            value=Key.RIGHT_SHIFT
            
        elif event.key == K_LCTRL:
            value=Key.LEFT_CONTROL
            
        elif event.key == K_RCTRL:
            value=Key.RIGHT_CONTROL
            
        elif event.key == K_BACKSPACE:
            value=Key.BACKSPACE
            
        elif event.key == K_PAUSE:
            value=Key.PAUSE
            
        elif event.key == K_SPACE:
            if event.type == KEYUP or event.unicode == ' ':
                value=Key.SPACE
            
        elif event.key == K_ESCAPE:
            value=Key.ESCAPE
            
        elif event.key == K_DELETE:
            value=Key.DELETE
            
        elif event.key == K_INSERT:
            value=Key.INSERT
            
        elif event.key == K_HOME:
            value=Key.HOME
            
        elif event.key == K_END:
            value=Key.END
            
        elif event.key == K_PAGEUP:
            value=Key.PAGE_UP
            
        elif event.key == K_PRINT:
            value=Key.PRINT_SCREEN
            
        elif event.key == K_PAGEDOWN:
            value=Key.PAGE_DOWN
            
        elif event.key == K_F1:
            value=Key.F1
            
        elif event.key == K_F2:
            value=Key.F2
            
        elif event.key == K_F3:
            value=Key.F3
            
        elif event.key == K_F4:
            value=Key.F4
            
        elif event.key == K_F5:
            value=Key.F5
            
        elif event.key == K_F6:
            value=Key.F6
            
        elif event.key == K_F7:
            value=Key.F7
            
        elif event.key == K_F8:
            value=Key.F8
            
        elif event.key == K_F9:
            value=Key.F9
            
        elif event.key == K_F10:
            value=Key.F10
            
        elif event.key == K_F11:
            value=Key.F11
            
        elif event.key == K_F12:
            value=Key.F12
            
        elif event.key == K_F13:
            value=Key.F13
            
        elif event.key == K_F14:
            value=Key.F14
            
        elif event.key == K_F15:
            value=Key.F15
            
        elif event.key == K_NUMLOCK:
            value=Key.NUM_LOCK
            
        elif event.key == K_CAPSLOCK:
            value=Key.CAPS_LOCK
            
        elif event.key == K_SCROLLOCK:
            value=Key.SCROLL_LOCK
            
        elif event.key == K_RMETA:
            value=Key.RIGHT_META
            
        elif event.key == K_LMETA:
            value=Key.LEFT_META
            
        elif event.key == K_LSUPER:
            value=Key.LEFT_SUPER
            
        elif event.key == K_RSUPER:
            value=Key.RIGHT_SUPER
            
        elif event.key == K_MODE:
            value=Key.MODE
            
        elif event.key == K_UP:
            value=Key.UP
            
        elif event.key == K_DOWN:
            value=Key.DOWN
            
        elif event.key == K_LEFT:
            value=Key.LEFT
            
        elif event.key == K_RIGHT:
            value=Key.RIGHT
            
        elif event.key == K_RETURN:
            value=Key.ENTER
            
        elif event.key == K_KP_ENTER:
            value=Key.ENTER
            
            
        if event.mod&KMOD_NUM == False:
            if event.key == K_KP0:
                value=Key.INSERT
                
            if event.key == K_KP1:
                value=Key.END
                
            if event.key == K_KP2:
                value=Key.DOWN
                
            if event.key == K_KP3:
                value=Key.PAGE_DOWN
                
            if event.key == K_KP4:
                value=Key.LEFT
                
            if event.key == K_KP5:
                value=0
                
            if event.key == K_KP6:
                value=Key.RIGHT
                
            if event.key == K_KP7:
                value=Key.HOME
                
            if event.key == K_KP8:
                value=Key.UP
                
            if event.key == K_KP9:
                value=Key.PAGE_UP
                
        return value
                
            

                