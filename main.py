#!/usr/bin/env python

import sys, os
import pygame
import imp
from math import *
from pickle import *
from zlib import *
from StringIO import *
from pygame.locals import *
from array import *
import xml.dom.minidom

from utilities import *
from sprite import *
from tileset import *

#Global variables
TILEWIDTH=32

TILEHEIGHT=32
NORTH, SOUTH, EAST, WEST = 0, 1, 2, 3
UP, DOWN, LEFT, RIGHT, JUMP= 0, 1, 2, 3, 4
UP_RIGHT = 5
UP_LEFT = 6
DOWN_RIGHT = 7
DOWN_LEFT = 8
JUMP_RIGHT = 9
JUMP_LEFT = 10

BASEDIR=os.path.dirname(__file__)
while os.path.basename(BASEDIR).find(".") > -1:
    BASEDIR=os.path.dirname(BASEDIR)
    
BASEFILE=__file__
RESOURCEDIR=os.path.join(BASEDIR, "resource")
LEVELDIR=os.path.join(BASEDIR, "levels")
CURRENTLEVELDIR=""

frame=0
total=0
config={}
gravity=8