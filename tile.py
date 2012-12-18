#!/usr/bin/env python

from main import *

class TileTemplate:
     def init(self,name=""):
          self.name=name
          self.sprite=Null
          self.walkable=True
          self.cloud=False
          self.friction=0.0
          self.slope=False
          self.id=-1
          