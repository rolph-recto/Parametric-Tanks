from main import *
from controller import *

class PackageController(PersonController):
     def __init__(self,args):
          PersonController.__init__(self,args)
          
     def Update(self,args):
          pass
          
     def OnObjectCollision(self,message):
          if message.collision_type != COLLISION_WALL:
               if message.obj2.type.name == "cannonball":
                    ctrl=self.room.GetControllerByObj(message.obj2)
                    if ctrl.owner == 1:
                         self.room.GetControllerByObj(self.room.GetObjectByName("player")).Score(50)
                    else:
                         self.room.GetControllerByObj(self.room.GetObjectByName("player2")).Score(50)
                         
                    self.object.remove=True

Controller=PackageController