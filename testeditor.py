#!/usr/bin/env python

from room import *
from pickle import *
from view import *
from guichan import *

SCREEN_WIDTH, SCREEN_HEIGHT=640, 672
screen = None
room = None
view=None
gui, input, grpahics, font, top=None, None, None, None, None
key=None
action=None
OnAction=None

def InitGUI():
     global gui, input, graphics, font, top, action
     gui=Gui()
     input=PygameInput()
     Image.mImageLoader=PygameImageLoader()
     graphics=PygameGraphics()
     graphics.setTarget(screen)
     font=ImageFont("consolefont.bmp")
     font.setColorkey( Color(255,0,255) )
     font.setGlyphSpacing(2)
     Widget.setGlobalFont(font)
     top=Container()
     top.setOpaque(False)
     top.setPosition(0,0)
     top.setSize(SCREEN_WIDTH,SCREEN_HEIGHT)
     top.setBaseColor( Color(255,0,0,255) )   
     gui.setInput(input)
     gui.setTop(top)
     gui.setGraphics(graphics)
     
     action=ActionListener()
     action.action=OnAction
     action.valueChanged=OnAction
     
     InitToolbar()

toolbar=None
xLabel, yLabel=None, None
xTileLabel, yTileLabel=None, None
def InitToolbar():
     global toolbar
     toolbar=TabbedArea()
     toolbar.setPosition(0, 480)
     toolbar.setSize(640,192)
     
     global xLabel, yLabel, xTileLabel, yTileLabel
     xLabel=Label("X: ")
     yLabel=Label("Y: ")
     xTileLabel=Label("X Tile: ")
     yTileLabel=Label("Y Tile: ")     
     
     global noticeWin, noticeText, noticeButton
     noticeWin=Window("Notice")
     noticeText=TextBox("This is a Notice")
     noticeText.adjustSize()
     noticeText.setOpaque(False)
     noticeText.setEditable(False)
     noticeButton=Button("OK")
     noticeButton.setActionEventId("NoticeOK")
     noticeButton.addActionListener(action)
     noticeButton.adjustSize()
     
     noticeWin.add(noticeText,0,10)
     noticeWin.add(noticeButton,65,30)
     noticeWin.setPadding(10)
     noticeWin.resizeToContent()
     noticeWin.setVisible(False)
     noticeWin.setMovable(False)
     
     top.add(noticeWin)
     top.add(toolbar)
     top.add(xLabel, 320, 485)
     top.add(yLabel, 390, 485)
     top.add(xTileLabel, 460, 485)
     top.add(yTileLabel, 550, 485)
     
     InitBrushTab()
     InitObjectTab()

class TileTemplateListModel(ListModel):
     def __init__(self):
          pass
        
     def getNumberOfElements(self):
          return len(room.map.tileList)
    
     def getElementAt(self,i):
          return room.map.tileList[i].name
          
class LayerListModel(ListModel):
     def __init__(self):
          pass
          
     def getNumberOfElements(self):
          return len(room.map.layerList)
    
     def getElementAt(self,i):
          return room.map.layerList[i].name
        
class ObjectTemplateListModel(ListModel):
     def __init__(self):
          pass
        
     def getNumberOfElements(self):
          return len(room.database[OBJTYPE])
    
     def getElementAt(self,i):
          return room.database[OBJTYPE].values()[i].name

class ObjectDataListModel(ListModel):
     def __init__(self):
          pass
     
     def getNumberOfElements(self):
          global obj
          o=room.GetObjectById(obj)
          if o != None:
               return len(o.data)
          
          else:
               return 0
    
     def getElementAt(self,i):
          global obj
          o=room.GetObjectById(obj)
          if o != None:
               return o.data.keys()[i]
          
          return ""
     
class ObjectDataListListener(SelectionListener):
     def __init__(self):
          pass
     
     def valueChanged(self,sourceEvent):
          global obj
          o=room.GetObjectById(obj)
          
          if o != None:
               v=o.data[ o.data.keys()[sourceEvent.getSource().getSelected()] ]
               objectVarValueText.setText( str(v) )
               if type(v) == type(123):
                    objectVarTypeInt.setSelected(True)
               elif type(v) == type(12.3):
                    objectVarTypeFloat.setSelected(True)
               elif type(v) == type("123"):
                    objectVarTypeStr.setSelected(True)
               else:
                    objectVarTypeList.setSelected(True)

brushMapLabel=None
brushMapText=None
brushMapSave=None
brushMapLoad=None
brushMapWidthLabel=None
brushMapWidthText=None
brushMapHeightLabel=None
brushMapHeightText=None
brushMapResize=None
brushMapFill=None
brushMapLayerList=None
brushMapLayerListScroll=None
brushMapLayerLabel=None
brushMapLayerBase=None
brushMapLayerVisible=None
def InitBrushTab():
     brush=[]
     
     global brushMapLabel
     brushMapLabel=Label("Map")
     
     global brushMapText
     brushMapText=TextField("Map file here")
     brushMapText.adjustSize()
     brushMapText.setWidth(140)
     
     global brushMapSave, brushMapLoad
     brushMapSave=Button("Save")
     brushMapSave.adjustSize()
     brushMapSave.setActionEventId("MapSave")
     brushMapSave.addActionListener(action)
     brushMapLoad=Button("Load")
     brushMapLoad.adjustSize()
     brushMapLoad.setActionEventId("MapLoad")
     brushMapLoad.addActionListener(action)
     
     global brushMapWidthLabel, brushMapWidthText
     brushMapWidthLabel=Label("Width")
     brushMapWidthText=TextField("1")
     brushMapWidthText.adjustSize()
     brushMapWidthText.setWidth(40)
     
     global brushMapHeightLabel, brushMapHeightText
     brushMapHeightLabel=Label("Height")
     brushMapHeightText=TextField("1")
     brushMapHeightText.adjustSize()
     brushMapHeightText.setWidth(40)
     
     brushMapWidthText.setText( str(room.map.width) )
     brushMapHeightText.setText( str(room.map.height) )
     
     global brushMapResize, brushMapFill
     brushMapResize=Button("Resize")
     brushMapResize.adjustSize()
     brushMapResize.setActionEventId("MapResize")
     brushMapResize.addActionListener(action)
     brushMapFill=Button("Fill")
     brushMapFill.adjustSize()
     brushMapFill.setActionEventId("MapFill")
     brushMapFill.addActionListener(action)
     
     global brushMapListScroll, brushMapList, brushMapListLabel
     brushMapListLabel=Label("Templates")
     brushMapList=ListBox(TileTemplateListModel())
     #brushMapList.setSelected(0)
     brushMapListScroll=ScrollArea(brushMapList)
     brushMapList.setWidth(125)
     brushMapListScroll.setSize(125+brushMapListScroll.getScrollbarWidth(),100)
     
     global brushMapLayerList, brushMapLayerListScroll, brushMapLayerLabel, brushMapLayerBase, brushMapLayerVisible
     brushMapLayerLabel=Label("Layers")
     brushMapLayerList=ListBox(LayerListModel())
     brushMapLayerList.setActionEventId("LayerList")
     brushMapLayerList.addSelectionListener(action)
     brushMapLayerListScroll=ScrollArea(brushMapLayerList)
     brushMapLayerList.setWidth(125)
     brushMapLayerListScroll.setSize(125+brushMapLayerListScroll.getScrollbarWidth(),100)
     brushMapLayerVisible=Checkbox("All Layers Visible")
     brushMapLayerVisible.setSelected(True)
     brushMapLayerVisible.setActionEventId("MapLayerVisible")
     brushMapLayerVisible.addActionListener(action)
     
     #global brushMapBase, brushMapOverlay
     #brushMapBase=RadioButton("Base","MapLayer")
     #brushMapOverlay=RadioButton("Overlay","MapLayer")
     #brushMapBase.setSelected(True)
     
     brush.append((brushMapLabel, 5, 5))
     brush.append((brushMapText, 5, 10+brushMapLabel.getHeight()))
     brush.append((brushMapSave, 5, 30+brushMapText.getHeight()))
     brush.append((brushMapLoad, 15+brushMapSave.getWidth(), 30+brushMapText.getHeight()))
     brush.append((brushMapWidthLabel, 5, 60+brushMapSave.getHeight()))
     brush.append((brushMapWidthText, 5, 85+brushMapWidthLabel.getHeight()))
     brush.append((brushMapHeightLabel, 15+brushMapWidthLabel.getWidth(),60+brushMapSave.getHeight()))
     brush.append((brushMapHeightText, 15+brushMapWidthLabel.getWidth(),85+brushMapHeightLabel.getHeight()))
     brush.append((brushMapResize, 5,105+brushMapHeightText.getHeight()))
     brush.append((brushMapFill, 15+brushMapResize.getWidth(),105+brushMapHeightText.getHeight()))
     brush.append((brushMapListLabel, 15+brushMapText.getWidth(), 5))
     brush.append((brushMapListScroll, 15+brushMapText.getWidth(), 10+brushMapLabel.getHeight()))
     #brush.append((brushMapBase, 15+brushMapText.getWidth(), 30+brushMapListScroll.getHeight()))
     #brush.append((brushMapOverlay, 15+brushMapText.getWidth(), 45+brushMapListScroll.getHeight()))
     brush.append((brushMapLayerLabel, 200+brushMapListScroll.getWidth(), 5))
     brush.append((brushMapLayerListScroll, 200+brushMapListScroll.getWidth(), 10+brushMapLayerLabel.getHeight()))
     brush.append((brushMapLayerVisible, 200+brushMapListScroll.getWidth(), 15+brushMapLayerLabel.getHeight()+brushMapLayerListScroll.getHeight()))
     
     toolbar.addTab("Brush", brush)

def InitObjectTab():
     object=[]
     
     global brushObjLabel, brushObjText
     brushObjLabel=Label("Object")
     brushObjText=TextField("Object file here")
     brushObjText.adjustSize()
     brushObjText.setWidth(140)
     
     global brushObjSave, brushObjLoad
     brushObjSave=Button("Save")
     brushObjSave.adjustSize()
     brushObjSave.setActionEventId("ObjSave")
     brushObjSave.addActionListener(action)
     brushObjLoad=Button("Load")
     brushObjLoad.adjustSize()
     brushObjLoad.setActionEventId("ObjLoad")
     brushObjLoad.addActionListener(action)
     
     global brushObjNameLabel, brushObjNameText
     brushObjNameLabel=Label("Name")
     brushObjNameText=TextField("Object name here")
     brushObjNameText.adjustSize()
     brushObjNameText.setWidth(140)
     
     global brushObjDuplicate, brushObjDelete
     brushObjDuplicate=Button("Set Name")
     brushObjDuplicate.adjustSize()
     brushObjDuplicate.setActionEventId("ObjName")
     brushObjDuplicate.addActionListener(action)
     brushObjDelete=Button("Clear")
     brushObjDelete.adjustSize()
     brushObjDelete.setActionEventId("ObjClear")
     brushObjDelete.addActionListener(action)
     
     global brushObjListScroll, brushObjList, brushObjListLabel
     brushObjListLabel=Label("Templates")
     brushObjList=ListBox(ObjectTemplateListModel())
     brushObjList.setSelected(0)
     brushObjListScroll=ScrollArea(brushObjList)
     brushObjList.setWidth(100)
     brushObjListScroll.setSize(100+brushObjListScroll.getScrollbarWidth(),100)
     
     global brushObjSnapGrid
     brushObjSnapGrid=Checkbox("Snap to Grid")
     
     global objectDictLabel, objectDictList, objectDictListScroll
     objectDictLabel=Label("Variables")
     objectDictList=ListBox(ObjectDataListModel())
     objectDictList.setSelected(0)
     objectDictListScroll=ScrollArea(objectDictList)
     objectDictList.setWidth(100)
     objectDictList.addSelectionListener(ObjectDataListListener())
     objectDictListScroll.setSize(100+objectDictListScroll.getScrollbarWidth(),100)
     
     global objectVarTypeLabel, objectVarTypeInt, objectVarTypeStr, objectVarTypeFloat, objectVarTypeList
     objectVarTypeLabel=Label("Type")
     objectVarTypeInt=RadioButton("Integer","ObjectVarType")
     objectVarTypeFloat=RadioButton("Floating Point","ObjectVarType")
     objectVarTypeStr=RadioButton("String","ObjectVarType")
     objectVarTypeList=RadioButton("List","ObjectVarType")
     
     global objectVarValueLabel, objectVarValueText, objectVarValueSet
     objectVarValueLabel=Label("Value")
     objectVarValueText=TextField("Value here")
     objectVarValueText.adjustSize()
     objectVarValueText.setWidth(140)
     objectVarValueSet=Button("Set Value")
     objectVarValueSet.adjustSize()
     objectVarValueSet.setActionEventId("ObjValue")
     objectVarValueSet.addActionListener(action)

     object.append((brushObjLabel, 315, 5))
     object.append((brushObjText, 315, 10+brushObjLabel.getHeight()))
     object.append((brushObjSave, 315, 30+brushObjText.getHeight()))
     object.append((brushObjLoad, 325+brushObjSave.getWidth(), 30+brushObjText.getHeight()))
     object.append((brushObjNameLabel, 315, 60+brushObjSave.getHeight()))
     object.append((brushObjNameText, 315, 85+brushObjNameLabel.getHeight()))
     object.append((brushObjDuplicate, 315,105+brushObjNameText.getHeight()))
     object.append((brushObjDelete, 325+brushObjDuplicate.getWidth(),105+brushObjNameText.getHeight()))
     object.append((brushObjListLabel, 325+brushObjText.getWidth(), 5))
     object.append((brushObjListScroll, 325+brushObjText.getWidth(), 10+brushObjLabel.getHeight()))
     object.append((brushObjSnapGrid, 325+brushObjText.getWidth(), 30+brushObjListScroll.getHeight()))
     
     object.append((objectDictLabel, 5, 5))
     object.append((objectDictListScroll, 5, 15+objectDictLabel.getHeight()))
     object.append((objectVarTypeLabel, 25+objectDictList.getWidth(), 5))
     object.append((objectVarTypeInt, 25+objectDictList.getWidth(), 15+objectVarTypeLabel.getHeight()))
     object.append((objectVarTypeFloat, 25+objectDictList.getWidth(), 30+objectVarTypeInt.getHeight()))
     object.append((objectVarTypeStr, 150+objectDictList.getWidth(), 15+objectVarTypeFloat.getHeight()))
     object.append((objectVarTypeList, 150+objectDictList.getWidth(), 30+objectVarTypeStr.getHeight()))
     object.append((objectVarValueLabel, 25+objectDictList.getWidth(), 60+objectVarTypeInt.getHeight()))
     object.append((objectVarValueText, 25+objectDictList.getWidth(), 75+objectVarTypeInt.getHeight()))
     object.append((objectVarValueSet, 25+objectDictList.getWidth(), 95+objectVarValueText.getHeight()))
     
     toolbar.addTab("Object", object)
     
     
def Notice(caption):
     global edit
     edit=False
     noticeText.setText(caption)
     noticeText.adjustSize()
     noticeWin.setWidth(noticeText.getWidth())
     noticeText.setPosition( (noticeWin.getWidth()/2)-(noticeText.getWidth()/2), 10 )
     noticeButton.setPosition( (noticeWin.getWidth()/2)-(noticeButton.getWidth()/2), 20+noticeText.getHeight() )
     noticeWin.resizeToContent()
     noticeWin.setPosition((SCREEN_WIDTH/2)-(noticeWin.getWidth()/2),(SCREEN_HEIGHT/2)-(noticeWin.getHeight()/2))
     noticeWin.setVisible(True)
     noticeButton.requestModalFocus()
     noticeButton.requestFocus()
     
def OnAction(action):
     id=action.mSource.mActionEventId
     if id == "NoticeOK":
          noticeButton.releaseModalFocus()
          noticeWin.setVisible(False)
          global edit
          edit=True
          
     elif id == "MapFill":
          global key
          fill=brushMapList.getSelected()
          if key[K_x]: fill=-1
          
          if brushMapLayerList.getSelected() >= 0:
               room.map.FillLayer(room.map.layerList[brushMapLayerList.getSelected()].name,fill)
          else:
               room.map.Fill(room.map.layerList[brushMapLayerList.getSelected()].name,fill)
          """
          if brushMapBase.getSelected():
               room.map.FillBase(fill)
          else:
               room.map.FillOverlay(fill)
          """
               
     elif id == "MapResize":
          width=int(brushMapWidthText.getText())
          height=int(brushMapHeightText.getText())
          
          if width < 1 or height < 1:
               Notice("Map dimensions invalid!")
               return
          
          if brushMapLayerList.getSelected() >= 0:
               room.map.layerList[brushMapLayerList.getSelected()].Resize(width,height,brushMapList.getSelected())
               view.ResetToMap(20, 15)
               brushMapWidthText.setText( str(room.map.layerList[brushMapLayerList.getSelected()].width) )
               brushMapHeightText.setText( str(room.map.layerList[brushMapLayerList.getSelected()].height) )
          else:
               room.map.Resize(width,height,brushMapList.getSelected())
               view.ResetToMap(20, 15)
               brushMapWidthText.setText( str(room.map.width) )
               brushMapHeightText.setText( str(room.map.height) )
          
     elif id == "MapSave":
          room.map.Save(os.path.join(BASEDIR,brushMapText.getText()))
          
     elif id == "MapLoad":
          if os.path.exists( os.path.join(BASEDIR,brushMapText.getText()) ):
               room.map.Load( os.path.join(BASEDIR,brushMapText.getText()) )
               brushMapWidthText.setText( str(room.map.width) )
               brushMapHeightText.setText( str(room.map.height) )
               for i in range(brushMapLayerList.mListModel.getNumberOfElements()):
                    if room.map.layerList[i].name == room.map.baseLayer.name:
                         brushMapLayerList.setSelected(i)
                         
               view.ResetToMap(20, 15)
               
          else:
               Notice("File doesn't exist!")
               
     elif id == "ObjSave":
          room.SaveObjects( os.path.join(BASEDIR,brushObjText.getText()) )
          
     elif id == "ObjLoad":
          if os.path.exists( os.path.join(BASEDIR,brushObjText.getText()) ):
               room.LoadObjects( os.path.join(BASEDIR,brushObjText.getText()) )
               global obj
               obj=-2
               
          else:
               Notice("File doesn't exist!")
               
     elif id == "ObjName":
          global obj
          o=room.GetObjectById(obj)
          if o != None:
               if brushObjNameText.getText() != "Object name here":
                    o.name=brushObjNameText.getText()
               else:
                    o.name=""
               
     elif id == "ObjClear":
          room.RemoveAllObjects()
          
     elif id == "ObjValue":
          o=room.GetObjectById(obj)
          
          if o != None and objectDictList.getSelected() > -1:
               if objectVarTypeInt.getSelected():
                    o.data[ o.data.keys()[objectDictList.getSelected()] ]=int(objectVarValueText.getText())
               elif objectVarTypeFloat.getSelected():
                    o.data[ o.data.keys()[objectDictList.getSelected()] ]=float(objectVarValueText.getText())
               elif objectVarTypeStr.getSelected():
                    o.data[ o.data.keys()[objectDictList.getSelected()] ]=objectVarValueText.getText()
               elif objectVarTypeList.getSelected():
                    o.data[ o.data.keys()[objectDictList.getSelected()] ]=eval(objectVarValueText.getText())
                    
     elif id == "MapLayerVisible":
          if brushMapLayerList.getSelected() == -1:
               brushMapLayerVisible.setSelected(~brushMapLayerVisible.isSelected())
               return None
               
          layername=room.map.layerList[brushMapLayerList.getSelected()].name
          if brushMapLayerVisible.isSelected():
               for layer in room.map.layerList:
                    layer.visible=True
          else:
               for layer in room.map.layerList:
                    if layer.name != layername:
                         layer.visible=False
                    else:
                         layer.visible=True
     elif id == "LayerList":
          brushMapWidthText.setText( str(room.map.layerList[brushMapLayerList.getSelected()].width) )
          brushMapHeightText.setText( str(room.map.layerList[brushMapLayerList.getSelected()].height) )
          layername=room.map.layerList[brushMapLayerList.getSelected()].name
          if brushMapLayerVisible.isSelected():
               for layer in room.map.layerList:
                    layer.visible=True
          else:
               for layer in room.map.layerList:
                    if layer.name != layername:
                         layer.visible=False
                    else:
                         layer.visible=True
     
                         
def OnSelection(selection):
     layername=room.map.layerList[brushMapLayerList.getSelected()].name
     if brushMapLayerVisible.isSelected():
          for layer in room.map.layerList:
               layer.visible=True
     else:
          for layer in room.map.layerList:
               if layer.name != layername:
                    layer.visible=False
               else:
                    layer.visible=True

clock=None
total, lastX, lastY=None, None, None
pause, done, edit, obj=None, None, None, None
def main():
     os.chdir(BASEDIR)
     pygame.init()
     #icon=pygame.image.load("icon.bmp")
     #icon.set_colorkey((0,0,0))
     #pygame.display.set_icon(icon)
     pygame.display.set_caption("Zero Editor", "ZEdit")
     global screen
     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
     
     global room
     #timg=pygame.image.load("tile.bmp")     
     room=Room()
     room.map=MapData()
     room.editor=True
     mappy=room.map
     
     room.database.LoadXML("resource.txt")
     room.SetTileTemplate("main")
     room.map.Load("MAP1x.TXT")
     
     global view
     view=RoomView(room,20,15)
     view.SetPosition(0,0)
     
     InitGUI()
     
     global clock, frame, total, lastX, lastY, total, pause, done, edit, key, obj
     clock = pygame.time.Clock()
     pygame.key.set_repeat(5, 100)
     inputMessage=InputMessage(None)
     frame, total, lastX, lastY=0, 0, -1, -1
     total=0
     pause=False
     done=False
     edit=True
     obj=-2
     key=pygame.key.get_pressed()
     while done == False:
          clock.tick(30)
          key=pygame.key.get_pressed()
          for event in pygame.event.get():
               if event.type == QUIT:
                    done=True
               elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done=True
                    if event.key == K_DELETE:
                         room.RemoveObject(obj)
                    if event.key == K_x:
                         brushMapList.setSelected(-1)
                         
               elif event.type == MOUSEBUTTONDOWN:
                    if edit:
                         if event.button == 1:
                              if key[K_s]:
                                   o=room.GetObjectByPos(view.camX+event.pos[0]-view.posX, view.camY+event.pos[1]-view.posY)
                                   if o != None:
                                        obj=o.id
                                        if o.name != "":
                                             brushObjNameText.setText(o.name)
                                        else:
                                             brushObjNameText.setText("Object name here")
                                   else:
                                        obj=-2
                                        brushObjNameText.setText("Object name here")
                              elif key[K_m]:
                                   o=room.GetObjectById(obj)
                                   if o != None:
                                        if brushObjSnapGrid.isSelected():
                                             o.posX=SetBound( int((view.camX+event.pos[0]-view.posX)/TILEWIDTH)*TILEWIDTH, 0, (room.map.width*TILEWIDTH)-o.width)
                                             o.posY=SetBound( int((view.camY+event.pos[1]-view.posY)/TILEHEIGHT)*TILEHEIGHT, 0, (room.map.height*TILEHEIGHT)-o.height)
                                        else:
                                             o.posX=SetBound(view.camX+event.pos[0]-view.posX, 0, (room.map.width*TILEWIDTH)-o.width)
                                             o.posY=SetBound(view.camY+event.pos[1]-view.posY, 0, (room.map.height*TILEHEIGHT)-o.height)
                              else:
                                   if event.pos[0] <= view.posX+(view.width*TILEWIDTH) and event.pos[1] <= view.posY+(view.height*TILEHEIGHT):
                                        layer=room.map.layerList[brushMapLayerList.getSelected()]
                                        camX=SetBound(int(view.camX*(float(layer.width)/float(room.map.baseLayer.width))**2.0),0,(layer.width-view.width)*TILEWIDTH)
                                        camY=SetBound(int(view.camY*(float(layer.height)/float(room.map.baseLayer.height))**2.0),0,(layer.height-view.height)*TILEHEIGHT)
                                        mappy.SetLayer(layer.name, int((camX+(event.pos[0]-view.posX))/TILEWIDTH), int((camY+(event.pos[1]-view.posY))/TILEHEIGHT), brushMapList.getSelected())                                       
                         elif event.button == 2:
                              lastX=event.pos[0]
                              lastY=event.pos[1]
                         elif event.button == 3:
                              if brushObjSnapGrid.isSelected():
                                   x=int((view.camX+(event.pos[0]-view.posX))/TILEWIDTH)*TILEWIDTH+(TILEWIDTH-room.database[OBJTYPE].values()[brushObjList.getSelected()].width)
                                   y=int((view.camY+(event.pos[1]-view.posY))/TILEHEIGHT)*TILEHEIGHT+(TILEHEIGHT-room.database[OBJTYPE].values()[brushObjList.getSelected()].height)
                                   room.AddObject(room.database[OBJTYPE].values()[brushObjList.getSelected()], x, y, brushObjNameText.getText())
                              else:
                                   room.AddObject(room.database[OBJTYPE].values()[brushObjList.getSelected()], view.camX+event.pos[0]-view.posX, view.camY+event.pos[1]-view.posY, brushObjNameText.getText())
                         
               elif event.type == MOUSEMOTION:
                    if edit:
                         if event.buttons[0] == 1:
                              if key[K_s]:
                                   o=room.GetObjectByPos(view.camX+event.pos[0]-view.posX, view.camY+event.pos[1]-view.posY)
                                   if o != None:
                                        obj=o.id
                                        brushObjNameText.setText(o.name)
                                   else:
                                        obj=-2
                                        brushObjNameText.setText("Object name here")
                              elif key[K_m]:
                                   o=room.GetObjectById(obj)
                                   if o != None:
                                        if brushObjSnapGrid.isSelected():
                                             o.posX=SetBound( int((view.camX+event.pos[0]-view.posX)/TILEWIDTH)*TILEWIDTH, 0, (room.map.width*TILEWIDTH)-o.width)
                                             o.posY=SetBound( int((view.camY+event.pos[1]-view.posY)/TILEHEIGHT)*TILEHEIGHT, 0, (room.map.height*TILEHEIGHT)-o.height)
                                        else:
                                             o.posX=SetBound(view.camX+event.pos[0]-view.posX, 0, (room.map.width*TILEWIDTH)-o.width)
                                             o.posY=SetBound(view.camY+event.pos[1]-view.posY, 0, (room.map.height*TILEHEIGHT)-o.height)
                              else:
                                   if event.pos[0] <= view.posX+(view.width*TILEWIDTH) and event.pos[1] <= view.posY+(view.height*TILEHEIGHT):
                                        layer=room.map.layerList[brushMapLayerList.getSelected()]
                                        camX=SetBound(int(view.camX*(float(layer.width)/float(room.map.baseLayer.width))**2.0),0,(layer.width-view.width)*TILEWIDTH)
                                        camY=SetBound(int(view.camY*(float(layer.height)/float(room.map.baseLayer.height))**2.0),0,(layer.height-view.height)*TILEHEIGHT)
                                        mappy.SetLayer(room.map.layerList[brushMapLayerList.getSelected()].name, int((camX+(event.pos[0]-view.posX))/TILEWIDTH), int((camY+(event.pos[1]-view.posY))/TILEHEIGHT), brushMapList.getSelected())
                         if event.buttons[1] == 1:
                              if lastX >= 0 and lastY >= 0:
                                   if key[K_m]:
                                        pass
                                   else:
                                        view.SetCamPosition(view.camX-(event.pos[0]-lastX), view.camY-(event.pos[1]-lastY))
                                   lastX=event.pos[0]
                                   lastY=event.pos[1]
                         """ #Not a good idea to brush objects while in motion
                         if event.buttons[2] == 1:
                              if brushObjSnapGrid.isSelected():
                                   room.AddObject(room.database[OBJTYPE].values()[brushObjList.getSelected()], int((view.camX+(event.pos[0]-view.posX))/TILEWIDTH)*TILEWIDTH, int((view.camY+(event.pos[1]-view.posY))/TILEHEIGHT)*TILEHEIGHT, brushObjNameText.getText())
                              else:
                                   room.AddObject(room.database[OBJTYPE].values()[brushObjList.getSelected()], view.camX+event.pos[0]-view.posX, view.camY+event.pos[1]-view.posY, brushObjNameText.getText())
                         """
                              
                    #update x and y labels
                    xLabel.setCaption("X: "+str(view.camX+(event.pos[0]-view.posX)))
                    yLabel.setCaption("Y: "+str(view.camY+(event.pos[1]-view.posY)))
                    xTileLabel.setCaption("X Tile: "+str(int((view.camX+(event.pos[0]-view.posX))/TILEWIDTH)))
                    yTileLabel.setCaption("Y Tile: "+str(int((view.camY+(event.pos[1]-view.posY))/TILEHEIGHT)))
                           
               elif event.type == MOUSEBUTTONUP:
                    lastX=-1
                    lastY=-1
               
               inputMessage.ChangeEvent(event)
               #room.BroadcastMessage(inputMessage)
               #room.UpdateControllers()
               input.pushInput(event)
               gui.logic()

          #Draw Everything
          #room.UpdateControllers()
          #room.Logic() #Don't want gravity!
          screen.fill((0,0,0))
          view.Draw(screen,obj)
          gui.draw()
          pygame.display.flip()
          total=total+clock.get_fps()
          frame=frame+1
          
     print "FPS:", total/frame
     
     pygame.mixer.quit()
          
          
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()