# -= ml_graphEditorMask.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 2
#   / / / / / / /  2018-02-17
#  /_/ /_/ /_/_/  _________
#               /_________/
# 
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copyright 2018 Morgan Loomis
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#     ___________________
# - -/__ Installation __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_graphEditorMask.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_graphEditorMask
#     ml_graphEditorMask.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly mask the visible curves in the graph editor.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Works best as hotkeys or marking menus for quick masking. Select Translate to
# isolate all the translate channels of the nodes you have selected. Select X to
# further isolate all translateX curves.
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
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
# [null] : Isolate Z axis curves
# [TRS] : Isolate Z axis curves
# [Custom] : Isolate Z axis curves
# 
#     ___________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
#     https://raw.githubusercontent.com/morganloomis/ml_tools/master/ml_utilities.py
# 
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -

__author__ = 'Morgan Loomis'
__license__ = 'MIT'
__revision__ = 2
__category__ = 'animation'

import sys
import maya.cmds as mc
import maya.mel as mm

try:
    import ml_utilities as utl
    utl.upToDateCheck(32)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/tool/ml_utilities/',absolute=True)

ATTR_FILTER_NAME = 'ml_graphEditorMask_attrFilter'
OBJ_FILTER_NAME = 'ml_graphEditorMask_objFilter'

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

        #b41 = win.buttonWithPopup(label='null', command=z, annotation='Isolate Z axis curves')
        #b42 = win.buttonWithPopup(label='TRS', command=z, annotation='Isolate Z axis curves')
        #b43 = win.buttonWithPopup(label='Custom', command=z, annotation='Isolate Z axis curves')

        utl.formLayoutGrid(form, (
            (b11,b21,b31),
            (b12,b22,b32),
            (b13,b23,b33)
            ))


def getGraphEditorOutliner():
    graphEditor = mc.getPanel(scriptType='graphEditor')
    if graphEditor:
        return mc.animCurveEditor(graphEditor[0]+'GraphEd', query=True, outliner=True)
    return None


def channelBox(*args):

    shortNames = utl.getSelectedChannels()
    if not shortNames:
        return
    sel = mc.ls(sl=True)
    channels = [mc.attributeQuery(x, longName=True, node=sel[-1]) for x in shortNames]
    filterChannels(channels)


def selected(*args):

    curves = mc.keyframe(query=True, selected=True, name=True)
    if not curves:
        return

    try:
        mc.delete(ATTR_FILTER_NAME)
    except:pass
    try:
        mc.delete(OBJ_FILTER_NAME)
    except:pass

    filters = list()
    for c in curves:
        plug = mc.listConnections(c, plugs=True, source=False, destination=True)[0]
        print plug
        filters.append(mc.itemFilter(byName=plug, classification='user'))

    print filters
    selectedFilter = mc.itemFilter(union=filters)
    #mc.delete(filters)
    print selectedFilter
    mc.outlinerEditor('graphEditor1OutlineEd', edit=True, attrFilter=selectedFilter)


def showAll(*args):

    try:
        mc.delete(ATTR_FILTER_NAME)
    except:pass

    for ge in mc.getPanel(scriptType='graphEditor'):
        mm.eval('filterUIClearFilter  {};'.format(mc.animCurveEditor(ge+'GraphEd', query=True, outliner=True)))


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
                    channels.extend(attrs)
            else:
                attr = c.split('.')[-1]
                if attr.startswith(option):
                    channels.append(attr)
                    if not wildCard:
                        wildCard = option+'*'
                elif attr.endswith(option):
                    channels.append(attr)
                    if not wildCard:
                        wildCard = '*'+option
                elif attr == option:
                    channels.append(attr)
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
                channels.extend(attrs)

    if not channels:
        for obj in sel:
            attrs = mc.listAttr(obj, keyable=True, unlocked=True)
            if attrs:
                channels = [a for a in attrs if a==option or a.startswith(option) or a.endswith(option)]

    filterChannels(channels)


def filterChannels(channels):

    try:
        mc.delete(ATTR_FILTER_NAME)
    except:pass
    try:
        mc.delete(OBJ_FILTER_NAME)
    except:pass
    channels = list(set(channels))
    channelFilter = mc.itemFilterAttr(ATTR_FILTER_NAME, byNameString=channels, classification='user')

    mc.outlinerEditor('graphEditor1OutlineEd', edit=True, attrFilter=channelFilter)


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
# Revision 2: 2018-02-17 : Updating license to MIT.