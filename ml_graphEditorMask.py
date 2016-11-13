# 
#   -= ml_graphEditorMask.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 2, 2016-11-10
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_graphEditorMask.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_graphEditorMask
#     ml_graphEditorMask.ui()
# From MEL, this looks like:
#     python("import ml_graphEditorMask;ml_graphEditorMask.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly mask the visible curves in the graph editor.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Works best as hotkeys or marking menus for quick masking.
# Select Translate to isolate all the translate channels of the
# nodes you have selected. Select X to further isolate all translateX
# curves.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Channel Box] : Isolate curves based on channels highlighted in the channel box
# [Selected] : Isolate the selected curves
# [All] : Show all animation curves
# [Translate] : Isolate translation curves
# [Rotate] : Isolate rotation curves
# [Scale] : Isolate scale curves
# [X] : Isolate X axis curves
# [Y] : Isolate Y axis curves
# [Z] : Isolate Z axis curves
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'animationScripts'
__revision__ = 1


import maya.cmds as mc

try:
    import ml_utilities as utl
    utl.upToDateCheck(18)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    

def ui():
    '''
    User interface for graph editor mask
    '''

    with utl.MlUi('ml_graphEditorMask', 'Graph Editor Mask', width=400, height=120, info='''Quickly mask the curves visible in the graph editor.
''') as win:
        
        #check box to cull selection to what's visible.
        
        form = mc.formLayout()
        b11 = win.buttonWithPopup(label='Channel Box', command=channelBox, annotation='Isolate curves based on channels highlighted in the channel box')
        b12 = win.buttonWithPopup(label='Selected', command=selected, annotation='Isolate the selected curves')
        b13 = win.buttonWithPopup(label='All', command=showAll, annotation='Show all animation curves')
        b21 = win.buttonWithPopup(label='Translate', command=translate, annotation='Isolate translation curves')
        b22 = win.buttonWithPopup(label='Rotate', command=rotate, annotation='Isolate rotation curves')
        b23 = win.buttonWithPopup(label='Scale', command=scale, annotation='Isolate scale curves')
        b31 = win.buttonWithPopup(label='X', command=x, annotation='Isolate X axis curves')
        b32 = win.buttonWithPopup(label='Y', command=y, annotation='Isolate Y axis curves')
        b33 = win.buttonWithPopup(label='Z', command=z, annotation='Isolate Z axis curves')

        utl.formLayoutGrid(form, (
            (b11,b21,b31),
            (b12,b22,b32),
            (b13,b23,b33)
            ))


def clear(*args):
    '''Clears the graph editor of all curves'''
    mc.selectionConnection('graphEditor1FromOutliner', edit=True, clear=True)


def channelBox(*args):
    
    channels = utl.getSelectedChannels()
    if not channels:
        return
    
    sel = mc.ls(sl=True)
    clear()
    for each in sel:
        for c in channels:
            if mc.attributeQuery(c, node=each, exists=True):
                mc.selectionConnection('graphEditor1FromOutliner', edit=True, select=each+'.'+c)


def selected(*args):
    
    curves = mc.keyframe(query=True, selected=True, name=True)
    if not curves:
        return
    
    clear()
    for c in curves:
        plug = mc.listConnections(c, plugs=True, source=False, destination=True)
        mc.selectionConnection('graphEditor1FromOutliner', edit=True, select=plug[0])


def showAll(*args):
    
    sel = mc.ls(sl=True)
    if not sel:
        return
    
    for each in sel:
        attrs = mc.listAttr(each, keyable=True, unlocked=True)
        if attrs:
            for a in attrs:
                mc.selectionConnection('graphEditor1FromOutliner', edit=True, select=each+'.'+a)


def translate(*args): isolate('translate')
    
def rotate(*args): isolate('rotate')
    
def scale(*args): isolate('scale')
    
def x(*args): isolate('X')
    
def y(*args): isolate('Y')
    
def z(*args): isolate('Z')
    

def isolate(option):
    
    sel = mc.ls(sl=True)
    if not sel:
        return
    
    graphVis = mc.selectionConnection('graphEditor1FromOutliner', query=True, obj=True)
    
    channels = list()
    wildCard = str()
    alreadyIsolated = True
    
    if graphVis:
        for c in graphVis:
            if not '.' in c and mc.objExists(c):
                attrs = mc.listAttr(c, keyable=True, unlocked=True)
                if attrs:
                    channels.extend([c+'.'+a for a in attrs])
            else:
                attr = c.split('.')[-1]
                if attr.startswith(option):
                    channels.append(c)
                    if not wildCard:
                        wildCard = option+'*'
                elif attr.endswith(option):
                    channels.append(c)
                    if not wildCard:
                        wildCard = '*'+option
                elif attr == option:
                    channels.append(c)
                    if not wildCard:
                        wildCard = option
                else:
                    #found a curve that is outside our search parameters
                    alreadyIsolated = False
            
    if channels and alreadyIsolated:
    
        #if the option is already the only thing being displayed, then show everything that matches the option

        for obj in sel:
            attrs = mc.listAttr(obj, keyable=True, unlocked=True, string=wildCard)
            if attrs:
                channels.extend([obj+'.'+a for a in attrs])
                
    if not channels:
        for obj in sel:
            attrs = mc.listAttr(obj, keyable=True, unlocked=True)
            
            for a in attrs:
                if a==option or a.startswith(option) or a.endswith(option):
                    channels.append(obj+'.'+a)
    
    clear()
    for c in channels:
        mc.selectionConnection('graphEditor1FromOutliner', edit=True, select=c)


def markingMenu():
    '''
    Example of how a marking menu could be set up.
    '''
    
    menuKwargs = {'enable':True,
                  'subMenu':False,
                  'enableCommandRepeat':True,
                  'optionBox':False,
                  'boldFont':True}
        
    mc.menuItem(radialPosition='NW', label='Trans', command=translate, **menuKwargs)
    mc.menuItem(radialPosition='N', label='Rot', command=rotate, **menuKwargs)
    mc.menuItem(radialPosition='NE', label='Scale', command=scale, **menuKwargs)
    
    mc.menuItem(radialPosition='SW', label='X', command=x, **menuKwargs)
    mc.menuItem(radialPosition='S', label='Y', command=y, **menuKwargs)
    mc.menuItem(radialPosition='SE', label='Z', command=z, **menuKwargs)

    mc.menuItem(radialPosition='W', label='ChanBox', command=channelBox, **menuKwargs)
    mc.menuItem(radialPosition='E', label='Sel', command=selected, **menuKwargs)
    
    mc.menuItem(label='All', command=showAll, **menuKwargs)


if __name__ == '__main__':
    ui()    


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-05-31 : First publish.
#
# Revision 2: 2016-11-10 : Fix error when no channels are found.
