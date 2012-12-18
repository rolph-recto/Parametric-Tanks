config["TITLE"]="Parametric Tanks!"
config["ICON_TITLE"]="ZE3"
config["ICON"]="zero.bmp"
config["DISPLAY_FLAGS"]=0
config["SCREEN_WIDTH"]=800
config["SCREEN_HEIGHT"]=480
config["FONT_FILE"]="LiberationMono-Regular.ttf"
config["FONT_SIZE"]=12
config["FONT_COLOR"]=Color(255,255,255)
config["FONT_SPACING"]=2
config["VIEW_WIDTH"]=25
config["VIEW_HEIGHT"]=13
config["VIEW_POSX"]=0
config["VIEW_POSY"]=0
config["DATABASE"]="resource.txt"
config["TILE_TEMPLATE"]="main"
config["LEVELS"]=["one","two","three"]
config["KEYREPEAT_DELAY"]=100
config["KEYREPEAT_INTERVAL"]=20
config["PARTICLE_TEMPLATES"]=[]
config["PROJECTILE_SPEED"]=10.0
config["MAX_POWER"]=200
config["GRAVITY"]=4

diamond=Polygon([[0,-10], [-10,0], [0,10], [10,0]], 0, 0)
pt=ParticleTemplate("diamond",diamond)
pt.life=20
pt.gravity=1.0
pt.fall=False
pt.color=Color(0,128,255,255)
pt.decay=Color(0,-5,-10,0)
pt.fill=False
config["PARTICLE_TEMPLATES"].append(pt)
     
pt5=ParticleTemplate("diamond2",diamond)
pt5.life=20
pt5.gravity=1.0
pt5.fall=False
pt5.color=Color(255,0,0,255)
pt5.decay=Color(5,-15,0,0)
pt5.fill=False
config["PARTICLE_TEMPLATES"].append(pt5)

circle=Circle(0,0,4)
pt2=ParticleTemplate("circle",circle)
pt2.life=20
pt2.gravity=1.0
pt2.fall=False
pt2.color=Color(255,230,230,255)
pt2.decay=Color(0,30,50,0)
pt2.fill=True
config["PARTICLE_TEMPLATES"].append(pt2)
          
circle=Circle(0,0,10)
pt3=ParticleTemplate("circle2",circle)
pt3.life=45
pt3.gravity=1.0
pt3.fall=False
pt3.color=Color(0,255,255,255)
pt3.decay=Color(0,10,20,0)
pt3.fill=False
config["PARTICLE_TEMPLATES"].append(pt3)
          
circle=Circle(0,0,8)
pt4=ParticleTemplate("circle3",circle)
pt4.life=45
pt4.gravity=1.0
pt4.fall=True
pt4.color=Color(255,0,0,255)
pt4.decay=Color(0,10,20,0)
pt4.fill=False
config["PARTICLE_TEMPLATES"].append(pt4)

circle=Circle(0,0,20)
pt6=ParticleTemplate("circle4",circle)
pt6.life=60
pt6.gravity=1.0
pt6.fall=False
pt6.color=Color(255,255,255,255)
pt6.decay=Color(10,10,10,0)
pt6.fill=False
config["PARTICLE_TEMPLATES"].append(pt6)

circle=Circle(0,0,16)
pt7=ParticleTemplate("circle5",circle)
pt7.life=45
pt7.gravity=1.0
pt7.fall=False
pt7.color=Color(250,0,0,255)
pt7.decay=Color(0,0,0,0)
pt7.fill=False
config["PARTICLE_TEMPLATES"].append(pt7)

circle=Circle(0,0,8)
pt8=ParticleTemplate("circle6",circle)
pt8.life=45
pt8.gravity=1.0
pt8.fall=False
pt8.color=Color(250,150,0,255)
pt8.decay=Color(0,5,0,0)
pt8.fill=True
config["PARTICLE_TEMPLATES"].append(pt8)