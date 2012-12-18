#!/usr/bin/env python

import pygame
from pygame.locals import *

from guichan import *
from gui import Gui
from actionListener import ActionListener
from widget import Widget
from basicContainer import BasicContainer
from container import Container
from button import Button
from checkbox import Checkbox
from window import Window
from textField import TextField
from radioButton import RadioButton
from label import Label
from icon import Icon
from tabbedArea import TabbedArea
from tab import Tab
from listBox import ListBox
from listModel import ListModel
from slider import Slider
from imageButton import ImageButton
from textBox import TextBox
from scrollArea import ScrollArea
from progressBar import ProgressBar
from image import Image
from imageFont import ImageFont
from pygameInput import PygameInput
from pygameGraphics import PygameGraphics
from pygameGraphics import GuichanToPygameDirtyRect
from pygameImage import PygameImage
from pygameImageLoader import PygameImageLoader
from pygameFont import PygameFont

#import psyco
#psyco.log(); psyco.full()

import cProfile
import gc

class List_ListModel(ListModel):
    def __init__(self,list=[]):
        self.mList=list
        
    def getNumberOfElements(self):
        return len(self.mList)
    
    def getElementAt(self,i):
        return self.mList[i]
    
def action(action):
    print "Action event from "+action.getId()

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480),pygame.SWSURFACE)
    pygame.key.set_repeat(100, 100)
    '''TEST'''
    g=Gui()
    #g.enableDirtyRect()
    g.optimizeDraw()
    i=PygameInput()
    Image.mImageLoader=PygameImageLoader()
    gr=PygameGraphics()
    gr.setTarget(screen)
    f=ImageFont("C:\Python25\Projects\Guichan\consolefont.bmp")
    #f=ImageFont("consolefont.bmp")
    f.setColorkey( Color(255,0,255) )
    f.setGlyphSpacing(2)
    f2=PygameFont("C:\Python25\Projects\Guichan\LiberationMono-Regular.ttf",14,Color(0,0,0,255))
    #f2=PygameFont("C:\Python25\Projects\Guichan\Caracteres L1.ttf",13,Color(0,0,0,255))
    f2.setGlyphSpacing(1)
    Widget.setGlobalFont(f2)
    
    c=Container()
    c.setOpaque(False)
    c.setPosition(0,0)
    c.setSize(640,480)
    c.setBaseColor( Color(255,0,0,255) )
    
    a=ActionListener()
    a.action=action
    b, b2=Button("YEY!"), Button("WHa?")
    b.setPosition(0,50)
    b.setActionEventId("Button 1")
    b.addActionListener(a)
    b2.setPosition(100,100)
    b2.setActionEventId("Button 2")
    b2.addActionListener(a)
    b2.setBaseColor( Color(200,200,200) )
    b2.setCaption("ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()")
    w,w2=Window("Hey over here!"), Window("Trapped in a window!")
    wColor=w.getBaseColor()
    wColor.a=200
    w.setBaseColor(wColor)
    w.setTextColor(Color(255,0,255))
    xyz=Button("XYZ")
    xyz.setTextColor(Color(0,255,255))
    pb=ProgressBar(100.0)
    pb.setBaseColor( Color(255,255,0) )
    pb.setForegroundColor( Color(0,255,255) )
    pb.setSize(100, 20)
    pb.setPosition(300, 300)
    pb.setValue(50.0)
    c.add(w,0,100)
    c.add(b)
    c.add(b2)
    c.add(xyz,10,10)
    c.add(pb)
    
    check=Checkbox("Ye what? GET BACK HERE BOY!")
    check.setActionEventId("Checkbox")
    check.addActionListener(a)
    text=TextField("Hey Hey Hey Hey Hey Hey Hey Hey")
    text.setBackgroundColor( Color(255,255,255,255) )
    text.setMaxSize(150)
    text2=TextBox("Hey, HeyTrapped in a window!\nWhat's goin' onTrapped in a window!\ntodays???Trapped in a window!")
    text2.setTabSize(10)
    sc=ScrollArea(text2)
    sc.setSize(200,100)
    rBox=Container()
    r1=RadioButton("1984","Dystopia")
    r2=RadioButton("Fahrenheit 451","Dystopia")
    r3=RadioButton("Brave New World","Dystopia")
    rBox.add(r1,0,0)
    rBox.add(r2,0,r1.getY()+r1.getHeight())
    rBox.add(r3,0,r2.getY()+r2.getHeight())
    label=Label("WE AIN'T GOT IT")
    ico_image=Image.load("C:\Python25\Projects\Guichan\May.bmp")
    ico=Icon(ico_image)
    lb=ListBox( List_ListModel(["Bollocks!","Never!","Cuppa tea, mate?","Hello!","Goodbye!","OK Computer!","Oh Inverted World!","How To Disappear Completely!","Hold Still!","It Takes A Train To Cry!","A","B","C","D","E","F","G","H","I",]) )
    sc2=ScrollArea(lb)
    sc2.setSize(125,100)
    lb.setWidth(110)
    slider=Slider(0,100)
    slider.setOrientation(Slider.Orientation.VERTICAL)
    slider.setSize(15,100)
    slider.setActionEventId("Slider")
    #slider.addActionListener(a)
    ib=ImageButton(ico_image)
    ta=TabbedArea()
    c.add(w2)
    ta.addTab("Text",[ (text,0,0), (sc,0,50) ])
    ta.addTab("Check",check)
    ta.addTab("Radio",rBox)
    ta.addTab("List",[ (sc2,0,0) ])
    ta.addTab("Label",label)
    ta.addTab("Icon",[ (ico,0,0), (ib,100,0) ])
    ta.addTab("Slider",slider)
    ta.setSize(300,300)
    w2.add(ta,0,0)
    g.setGraphics(gr)
    w2.resizeToContent()
    w.setSize(300,300)
    g.setInput(i)
    g.setTop(c)
    clock=pygame.time.Clock()
    
    g.mDirtyRect.addRect( Rectangle(0,0,640,480) )
    done=False
    while done == False:
        clock.tick(0)

        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key == K_ESCAPE:
                    c.remove(b)
                    c.remove(b2)
                    done=True
                
                elif event.key == K_RETURN:
                    w=Window("It'a window!")
                    w.add(Checkbox("Kool thing"))
                    w.resizeToContent()
                    c.add(w, 10, 10)
                    
                elif event.key == K_LEFT:
                    pb.setValue( pb.getValue()-1.0 )
                elif event.key == K_RIGHT:
                    pb.setValue( pb.getValue()+1.0 )                
                    
            if event.type == ACTIVEEVENT:
                if event.gain == 1:
                    g.mDirtyRect.addRect( Rectangle(0,0,640,480) )
                    
            i.pushInput(event)
            g.logic()
            
        b2.setCaption( str( int(clock.get_fps()) ) )
        fRect=GuichanToPygameDirtyRect(g.mDirtyRect.getList())
        #for ix in fRect: screen.fill((255,0,0),ix)
        
        screen.fill((255,0,0))    
        g.draw()
        #pygame.display.update( GuichanToPygameDirtyRect(g.mDirtyRect.getList()) )
        pygame.display.update()
        
        g.mDirtyRect.clearList()
            
        
main()
gc.collect()

#cProfile.run("main()","main")
"""
import pstats
p = pstats.Stats('main')

p.sort_stats('cumulative').print_stats(20)
"""
