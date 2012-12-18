#!/usr/bin/env python

from OpenGL.GL import *

import pygame
from pygame.locals import *

def power_of_two(input):
    value = 1

    while value < input :
        value *= 2;
        
    return value

def pygame_load_texture(tex):
    if type(tex) == type("abc"):
        surface=pygame.image.load(tex)
    else:
        surface=tex
        
    textureData = pygame.image.tostring(surface, "RGBA", 1)
 
    width = surface.get_width()
    height = surface.get_height()
 
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
        GL_UNSIGNED_BYTE, textureData)

    return texture
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480),pygame.OPENGL|pygame.DOUBLEBUF)
    pygame.key.set_repeat(100, 100)
    
    glViewport(0, 0, 640, 480)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    glMatrixMode (GL_PROJECTION)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    
    img=pygame.image.load("C:\Program Files\Python 2.5.1\Projects\Guichan\May.bmp")
    img_tex=pygame_load_texture(img)
    
    clock=pygame.time.Clock()
    done=False
    while done == False:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    done=True
            
            #i.pushInput(event)
            
        #b2.setCaption( str( int(clock.get_fps()) ) )
        #g.logic()
        #screen.fill((255,255,255))
        #g.draw()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(0, 640, 480, 0, -1, 1)
        #glMatrixMode(GL_MODELVIEW)
        #glPushMatrix()
        #glTranslatef(-1.5, 0.0, -6.0)

        # Draw a triangle
        glBindTexture(GL_TEXTURE_2D, img_tex)
        glBegin(GL_QUADS);
        glTexCoord2d(0.0, 0.0);glVertex2d(0.0, 0.0)
        glTexCoord2d(0.0, 1.0);glVertex2d(0.0, 1.0)
        glTexCoord2d(1.0, 1.0);glVertex2d(1.0, 1.0)
        glTexCoord2d(1.0, 0.0);glVertex2d(1.0, 0.0)
        glEnd()
        
    
        pygame.display.flip()
        clock.tick(60)
    

if __name__ == "__main__":
    main()
