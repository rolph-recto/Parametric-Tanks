from room import *

img=pygame.image.load( os.path.join(BASEDIR,"diamond.bmp") )
s=Sprite()
s.Create(img,"diamond",16,16)
s.SetColorKey(Color(0,255,0))
s.Save(os.path.join(BASEDIR,"diamond.spr"))

o=ObjectType("diamond")
o.SetSprite(s)
o.fall=False
o.collision=GHOST
o.controller="diamond"
o.data["score"]=1
o.Save(os.path.join(BASEDIR,"diamond.obj"))