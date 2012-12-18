#!/usr/bin/env python

import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image
from pyglet.gl import *
import pyglet.graphics

window = pyglet.window.Window()
may=pyglet.image.load("C:\Program Files\Python 2.5.1\Projects\Guichan\May.bmp")
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print 'The "A" key was pressed.'
    elif symbol == key.LEFT:
        print 'The left arrow key was pressed.'
    elif symbol == key.ENTER:
        print 'The enter key was pressed.'

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print 'The left mouse button was pressed at '+str(x)+','+str(y)

@window.event
def on_draw():
    window.clear()
    glColor4ub(255,255,255,255)
    may.blit(0,450)
    pyglet.graphics.draw(2,GL_LINES, ( ('v2i', (0, window.get_size()[1],    30, 35)) ), ('c4B', (255, 0, 255, 20, 0, 255, 0, 20)) )

pyglet.app.run()
