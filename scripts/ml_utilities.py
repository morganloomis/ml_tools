# -= ml_utilities.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 36
#   / / / / / / /  2019-03-07
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_utilities.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_utilities
#     ml_utilities._showHelpCommand()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# A collection of support functions that are required by several of the tools in
# this library. The individual tools will tell you if this script is required.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# ml_utilities isn't a stand alone tool, and so it isn't meant to be used
# directly. However, you can certainly call these functions if they seem useful in
# your own scripts.
# 
# 
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -

__author__ = 'Morgan Loomis'
__license__ = 'MIT'
__revision__ = 36

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya
import maya.api.OpenMaya as om
from functools import partial
import shutil, os, re, sys, math

#declare some variables
WEBSITE_URL = 'http://morganloomis.com'
TOOL_URL = WEBSITE_URL+'/tool/'
ICON_URL = WEBSITE_URL+'/icons/'
GITHUB_ROOT_URL = 'https://raw.githubusercontent.com/morganloomis/ml_tools/master/scripts/'

#try to add to the iconpath if there is an icons folder in this directory
THIS_DIR = os.path.dirname(__file__)
ICON_PATH = os.path.join(THIS_DIR,'icons').replace('\\','/')
if os.path.isdir(ICON_PATH) and ICON_PATH not in os.environ['XBMLANGPATH']:
    os.environ['XBMLANGPATH'] = os.pathsep.join((os.environ['XBMLANGPATH'],ICON_PATH))

MAYA_VERSION = mm.eval('getApplicationVersionAsFloat')

def _showHelpCommand(url):
    '''
    This just returns the maya command for launching a web page, since that gets called a few times
    '''
    return 'import maya.cmds;maya.cmds.showHelp("'+url+'",absolute=True)'


def main():
    '''
    This just launches the online help and serves as a placeholder for the default function for this script.
    '''
    mc.showHelp(TOOL_URL+'ml_utilities/', absolute=True)


def upToDateCheck(revision, prompt=True):
    '''
    This is a check that can be run by scripts that import ml_utilities to make sure they
    have the correct version.
    '''

    if not '__revision__' in locals():
        return

    if revision > __revision__:
        if prompt and mc.optionVar(query='ml_utilities_revision') < revision:
            result = mc.confirmDialog( title='Module Out of Date',
                                       message='Your version of ml_utilities may be out of date for this tool. Without the latest file you may encounter errors.',
                                       button=['Download Latest Revision','Ignore', "Don't Ask Again"],
                                       defaultButton='Download Latest Revision', cancelButton='Ignore', dismissString='Ignore' )

            if result == 'Download Latest Revision':
                mc.showHelp(GITHUB_ROOT_URL+'ml_utilities.py', absolute=True)
            elif result == "Don't Ask Again":
                mc.optionVar(intValue=('ml_utilities_revision', revision))
        return False
    return True


def castToTime(time):
    '''
    Maya's keyframe commands are finnicky about how lists of times or indicies are formatted.
    '''
    if isinstance(time, (list, tuple)):
        return [(x,) for x in time]
    return (time,)


def constrain(source, destination, translate=True, rotate=True, scale=False, maintainOffset=False):
    '''
    Constrain two objects, even if they have some locked attributes.
    '''

    transAttr = None
    rotAttr = None
    scaleAttr = None

    if translate:
        transAttr = mc.listAttr(destination, keyable=True, unlocked=True, string='translate*')
    if rotate:
        rotAttr = mc.listAttr(destination, keyable=True, unlocked=True, string='rotate*')
    if scale:
        scaleAttr = mc.listAttr(destination, keyable=True, unlocked=True, string='scale*')

    rotSkip = list()
    transSkip = list()

    for axis in ['x','y','z']:
        if transAttr and not 'translate'+axis.upper() in transAttr:
            transSkip.append(axis)
        if rotAttr and not 'rotate'+axis.upper() in rotAttr:
            rotSkip.append(axis)

    if not transSkip:
        transSkip = 'none'
    if not rotSkip:
        rotSkip = 'none'

    constraints = list()
    if rotAttr and transAttr and rotSkip == 'none' and transSkip == 'none':
        constraints.append(mc.parentConstraint(source, destination, maintainOffset=maintainOffset))
    else:
        if transAttr:
            constraints.append(mc.pointConstraint(source, destination, skip=transSkip, maintainOffset=maintainOffset))
        if rotAttr:
            constraints.append(mc.orientConstraint(source, destination, skip=rotSkip, maintainOffset=maintainOffset))

    return constraints


def createAnimLayer(nodes=None, name=None, namePrefix='', override=True):
    '''
    Create an animation layer, add nodes, and select it.
    '''

    #if there's no layer name, generate one
    if not name:
        if namePrefix:
            namePrefix+='_'
        if nodes:
            shortNodes = mc.ls(nodes, shortNames=True)
            shortNodes = [x.rpartition(':')[-1] for x in shortNodes]
            #if there's just one node, use it's name minus the namespace
            if len(shortNodes) == 1:
                name = namePrefix+shortNodes[0]
            else:
                #try to find the longest common substring
                commonString = longestCommonSubstring(shortNodes)
                if commonString:
                    name = commonString
                elif ':' in nodes[0]:
                    #otherwise use the namespace if it has one
                    name = nodes[0].rpartition(':')[-1]
        if not name:
            if not namePrefix:
                namePrefix = 'ml_'
            name = namePrefix+'animLayer'

    layer = mc.animLayer(name, override=override)

    #add the nodes to the layer
    if nodes:
        sel = mc.ls(sl=True)
        mc.select(nodes)
        mc.animLayer(layer, edit=True, addSelectedObjects=True)
        if sel:
            mc.select(sel)
        else:
            mc.select(clear=True)

    #select the layer
    selectAnimLayer(layer)
    return layer


def selectAnimLayer(animLayer=None):
    '''
    Select only the specified animation layer
    '''
    #deselect all layers
    for each in mc.ls(type='animLayer'):
        mc.animLayer(each, edit=True, selected=False, preferred=False)
    if animLayer:
        mc.animLayer(animLayer, edit=True, selected=True, preferred=True)


def getSelectedAnimLayers():
    '''
    Return the names of the layers which are selected
    '''
    layers = list()
    for each in mc.ls(type='animLayer'):
        if mc.animLayer(each, query=True, selected=True):
            layers.append(each)
    return layers


def createHotkey(command, name, description='', python=True):
    '''
    Open up the hotkey editor to create a hotkey from the specified command
    '''

    if MAYA_VERSION > 2015:
        print("Creating hotkeys currently doesn't work in the new hotkey editor.")
        print("Here's the command, you'll have to make the hotkey yourself (sorry):")
        print(command)
        OpenMaya.MGlobal.displayWarning("Couldn't create hotkey, please see script editor for details...")
        return

    mm.eval('hotkeyEditor')
    mc.textScrollList('HotkeyEditorCategoryTextScrollList', edit=True, selectItem='User')
    mm.eval('hotkeyEditorCategoryTextScrollListSelect')
    mm.eval('hotkeyEditorCreateCommand')

    mc.textField('HotkeyEditorNameField', edit=True, text=name)
    mc.textField('HotkeyEditorDescriptionField', edit=True, text=description)

    if python:
        if MAYA_VERSION < 2013:
            command = 'python("'+command+'");'
        else: #2013 or above
            mc.radioButtonGrp('HotkeyEditorLanguageRadioGrp', edit=True, select=2)

    mc.scrollField('HotkeyEditorCommandField', edit=True, text=command)


def createShelfButton(command, label='', name=None, description='',
                      image=None, #the default image is a circle
                      labelColor=(1, 0.5, 0),
                      labelBackgroundColor=(0, 0, 0, 0.5),
                      backgroundColor=None
                      ):
    '''
    Create a shelf button for the command on the current shelf
    '''
    #some good default icons:
    #menuIconConstraints - !
    #render_useBackground - circle
    #render_volumeShader - black dot
    #menuIconShow - eye

    gShelfTopLevel = mm.eval('$temp=$gShelfTopLevel')
    if not mc.tabLayout(gShelfTopLevel, exists=True):
        OpenMaya.MGlobal.displayWarning('Shelf not visible.')
        return

    if not name:
        name = label

    if not image:
        image = getIcon(name)
    if not image:
        image = 'render_useBackground'

    shelfTab = mc.shelfTabLayout(gShelfTopLevel, query=True, selectTab=True)
    shelfTab = gShelfTopLevel+'|'+shelfTab

    #add additional args depending on what version of maya we're in
    kwargs = {}
    if MAYA_VERSION >= 2009:
        kwargs['commandRepeatable'] = True
    if MAYA_VERSION >= 2011:
        kwargs['overlayLabelColor'] = labelColor
        kwargs['overlayLabelBackColor'] = labelBackgroundColor
        if backgroundColor:
            kwargs['enableBackground'] = bool(backgroundColor)
            kwargs['backgroundColor'] = backgroundColor

    return mc.shelfButton(parent=shelfTab, label=name, command=command,
                          imageOverlayLabel=label, image=image, annotation=description,
                          width=32, height=32, align='center', **kwargs)


def deselectChannels():
    '''
    Deselect selected channels in the channelBox
    by clearing selection and then re-selecting
    '''

    if not getSelectedChannels():
        return
    sel = mc.ls(sl=True)
    mc.select(clear=True)
    mc.evalDeferred(partial(mc.select,sel))


def formLayoutGrid(form, controls, offset=1):
    '''
    Controls should be a list of lists, and this will arrange them in a grid
    '''

    kwargs = {'edit':True, 'attachPosition':[]}
    rowInc = 100/len(controls)
    colInc = 100/len(controls[0])
    position = {'left':0,'right':100,'top':0,'bottom':100}

    for r,row in enumerate(controls):
        position['top'] = r*rowInc
        position['bottom'] = (r+1)*rowInc
        for c,ctrl in enumerate(row):
            position['left'] = c*colInc
            position['right'] = (c+1)*colInc
            for k in list(position.keys()):
                kwargs['attachPosition'].append((ctrl, k, offset, position[k]))

    mc.formLayout(form, **kwargs)


def frameRange(start=None, end=None):
    '''
    Returns the frame range based on the highlighted timeslider,
    or otherwise the playback range.
    '''

    if not start and not end:
        gPlayBackSlider = mm.eval('$temp=$gPlayBackSlider')
        if mc.timeControl(gPlayBackSlider, query=True, rangeVisible=True):
            frameRange = mc.timeControl(gPlayBackSlider, query=True, rangeArray=True)
            start = frameRange[0]
            end = frameRange[1]-1
        else:
            start = mc.playbackOptions(query=True, min=True)
            end = mc.playbackOptions(query=True, max=True)

    return start,end


def getChannelFromAnimCurve(curve, plugs=True):
    '''
    Finding the channel associated with a curve has gotten really complicated since animation layers.
    This is a recursive function which walks connections from a curve until an animated channel is found.
    '''


    #we need to save the attribute for later.
    attr = ''
    if '.' in curve:
        curve, attr = curve.split('.')

    nodeType = mc.nodeType(curve)
    if nodeType.startswith('animCurveT') or nodeType.startswith('animBlendNode'):
        source = mc.listConnections(curve+'.output', source=False, plugs=plugs)
        if not source and nodeType=='animBlendNodeAdditiveRotation':
            #if we haven't found a connection from .output, then it may be a node that uses outputX, outputY, etc.
            #get the proper attribute by using the last letter of the input attribute, which should be X, Y, etc.
            #if we're not returning plugs, then we wont have an attr suffix to use, so just use X.
            attrSuffix = 'X'
            if plugs:
                attrSuffix = attr[-1]

            source = mc.listConnections(curve+'.output'+attrSuffix, source=False, plugs=plugs)
        if source:
            nodeType = mc.nodeType(source[0])
            if nodeType.startswith('animCurveT') or nodeType.startswith('animBlendNode'):
                return getChannelFromAnimCurve(source[0], plugs=plugs)
            return source[0]


def getCurrentCamera():
    '''
    Returns the camera that you're currently looking through.
    If the current highlighted panel isn't a modelPanel,
    '''

    panel = mc.getPanel(withFocus=True)

    if mc.getPanel(typeOf=panel) != 'modelPanel':
        #just get the first visible model panel we find, hopefully the correct one.
        for p in mc.getPanel(visiblePanels=True):
            if mc.getPanel(typeOf=p) == 'modelPanel':
                panel = p
                mc.setFocus(panel)
                break

    if mc.getPanel(typeOf=panel) != 'modelPanel':
        OpenMaya.MGlobal.displayWarning('Please highlight a camera viewport.')
        return False

    camShape = mc.modelEditor(panel, query=True, camera=True)
    if not camShape:
        return False

    camNodeType = mc.nodeType(camShape)
    if mc.nodeType(camShape) == 'transform':
        return camShape
    elif mc.nodeType(camShape) in ['camera','stereoRigCamera']:
        return mc.listRelatives(camShape, parent=True, path=True)[0]


def getFrameRate():
    '''
    Return a float of the current frame rate.
    '''
    currentUnit = mc.currentUnit(query=True, time=True)
    if currentUnit == 'film':
        return 24
    if currentUnit == 'show':
        return 48
    if currentUnit == 'pal':
        return 25
    if currentUnit == 'ntsc':
        return 30
    if currentUnit == 'palf':
        return 50
    if currentUnit == 'ntscf':
        return 60
    if 'fps' in currentUnit:
        return float(currentUnit.replace('fps',''))

    return 1


def getFrameRateInSeconds():

    return 1.0/getFrameRate()


def getDistanceInMeters():

    unit = mc.currentUnit(query=True, linear=True)

    if unit == 'mm':
        return 1000
    elif unit == 'cm':
        return 100
    elif unit == 'km':
        return 0.001
    elif unit == 'in':
        return 39.3701
    elif unit == 'ft':
        return 3.28084
    elif unit == 'yd':
        return 1.09361
    elif unit == 'mi':
        return 0.000621371

    return 1


def getHoldTangentType():
    '''
    Returns the best in and out tangent type for creating a hold with the current tangent settings.
    '''
    try:
        tangentType = mc.keyTangent(query=True, g=True, ott=True)[0]
    except:
        return 'auto','auto'
    if tangentType=='linear':
        return 'linear','linear'
    if tangentType=='step':
        return 'linear','step'
    if tangentType == 'plateau' or tangentType == 'spline' or MAYA_VERSION < 2012:
        return 'plateau','plateau'
    return 'auto','auto'


def getIcon(name):
    '''
    Check if an icon name exists, and return with proper extension.
    Otherwise return standard warning icon.
    '''

    ext = '.png'
    if MAYA_VERSION < 2011:
        ext = '.xpm'

    if not name.endswith('.png') and not name.endswith('.xpm'):
        name+=ext

    for each in os.environ['XBMLANGPATH'].split(os.pathsep):
        #on some linux systems each path ends with %B, for some reason
        iconPath = os.path.abspath(each.replace('%B',''))
        iconPath = os.path.join(iconPath,name)
        if os.path.exists(iconPath):
            return name

    return None


def getIconPath():
    '''
    Find the icon path
    '''

    appDir = os.environ['MAYA_APP_DIR']
    for each in os.environ['XBMLANGPATH'].split(os.pathsep):
        #on some linux systems each path ends with %B, for some reason
        iconPath = each.replace('%B','')
        if iconPath.startswith(appDir):
            iconPath = os.path.abspath(iconPath)
            if os.path.exists(iconPath):
                return iconPath


def getModelPanel():
    '''Return the active or first visible model panel.'''
    
    panel = mc.getPanel(withFocus=True)

    if mc.getPanel(typeOf=panel) != 'modelPanel':
        #just get the first visible model panel we find, hopefully the correct one.
        panels = getModelPanels()
        if panels:
            panel = panels[0]
            mc.setFocus(panel)
    
    if mc.getPanel(typeOf=panel) != 'modelPanel':
        OpenMaya.MGlobal.displayWarning('Please highlight a camera viewport.')
        return None
    return panel
    
    
def getModelPanels():
    '''Return all the model panels visible so you can operate on them.'''
    panels = []
    for p in mc.getPanel(visiblePanels=True):
        if mc.getPanel(typeOf=p) == 'modelPanel':
            panels.append(p)
    return panels


def getNamespace(node):
    '''Returns the namespace of a node with simple string parsing.'''

    if not ':' in node:
        return ''
    return node.rsplit('|',1)[-1].rsplit(':',1)[0] + ':'


def getNucleusHistory(node):
    
    history = mc.listHistory(node, levels=0)
    if history:
        dynamics = mc.ls(history, type='hairSystem')
        if dynamics:
            nucleus = mc.listConnections(dynamics[0]+'.startFrame', source=True, destination=False, type='nucleus')
            if nucleus:
                return nucleus[0]
    return None


def getRoots(nodes):

    objs = mc.ls(nodes, long=True)
    tops = []
    namespaces = []
    parent = None
    for obj in objs:
        namespace = getNamespace(obj)
        if namespace in namespaces:
            #we've already done this one
            continue
        parent = mc.listRelatives(obj, parent=True, pa=True)
        top = obj
        if not namespace:
            while parent:
                top = parent[0]
                parent = mc.listRelatives(top, parent=True, pa=True)
            
            tops.append(top)
        
        else:
            namespaces.append(namespace)
            while parent and parent[0].rsplit('|',1)[-1].startswith(namespace):
                top = parent[0]
                parent = mc.listRelatives(top, parent=True, pa=True)
            
            tops.append(top)
    return tops


def getSelectedChannels():
    '''
    Return channels that are selected in the channelbox
    '''

    if not mc.ls(sl=True):
        return
    gChannelBoxName = mm.eval('$temp=$gChannelBoxName')
    sma = mc.channelBox(gChannelBoxName, query=True, sma=True)
    ssa = mc.channelBox(gChannelBoxName, query=True, ssa=True)
    sha = mc.channelBox(gChannelBoxName, query=True, sha=True)

    channels = list()
    if sma:
        channels.extend(sma)
    if ssa:
        channels.extend(ssa)
    if sha:
        channels.extend(sha)

    return channels


def getSkinCluster(mesh):
    '''
    Return the first skinCluster affecting this mesh.
    '''

    if mc.nodeType(mesh) in ('mesh','nurbsSurface','nurbsCurve'):
        shapes = [mesh]
    else:
        shapes = mc.listRelatives(mesh, shapes=True, path=True)

    for shape in shapes:
        history = mc.listHistory(shape, groupLevels=True, pruneDagObjects=True)
        if not history:
            continue
        skins = mc.ls(history, type='skinCluster')
        if skins:
            return skins[0]
    return None


def listAnimCurves(objOrAttrs):
    '''
    This lists connections to all types of animNodes
    '''

    animNodes = list()

    tl = mc.listConnections(objOrAttr, s=True, d=False, type='animCurveTL')
    ta = mc.listConnections(objOrAttr, s=True, d=False, type='animCurveTA')
    tu = mc.listConnections(objOrAttr, s=True, d=False, type='animCurveTU')

    if tl:
        animNodes.extend(tl)
    if ta:
        animNodes.extend(ta)
    if tu:
        animNodes.extend(tu)

    return animNodes


def longestCommonSubstring(data):
    '''
    Returns the longest string that is present in the list of strings.
    '''
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr):
                    find = data[0][i:i+j]
                    if len(data) < 1 and len(find) < 1:
                        continue
                    found = True
                    for k in range(len(data)):
                        if find not in data[k]:
                            found = False
                    if found:
                        substr = data[0][i:i+j]
    return substr


def sameNode(a, b):
    a = mc.ls(a, long=True)
    b = mc.ls(b, long=True)
    if not a or not b:
        return False
    return a == b


def matchBake(source=None, destination=None, bakeOnOnes=False, maintainOffset=False, preserveTangentWeight=True, translate=True, rotate=True, start=None, end=None):

    if not source and not destination:
        sel = mc.ls(sl=True)
        if len(sel) != 2:
            OpenMaya.MGlobal.displayWarning('Select exactly 2 objects')
            return
        source = [sel[0]]
        destination = [sel[1]]

    #save for reset:
    resetTime = mc.currentTime(query=True)

    #frame range
    if start == None or end == None:
        start, end = frameRange()

    attributes = list()
    if translate:
        attributes.extend(['translateX','translateY','translateZ'])
    if rotate:
        attributes.extend(['rotateX','rotateY','rotateZ'])

    if not attributes:
        OpenMaya.MGlobal.displayWarning('No attributes to bake!')
        return

    duplicates = {}
    keytimes = {}
    constraint = list()
    itt = {}
    ott = {}
    weighted = {}
    itw = {}
    otw = {}
    #initialize allKeyTimes with start and end frames, since they may not be keyed
    allKeyTimes = [start,end]
    for s,d in zip(source,destination):

        #duplicate the destination
        dup = mc.duplicate(d, name='temp#', parentOnly=True)[0]
        for a in attributes:
            mc.setAttr(dup+'.'+a, lock=False, keyable=True)

        constraint.append(mc.parentConstraint(s, dup, maintainOffset=maintainOffset))

        #cut keys on destination
        mc.cutKey(d, attribute=attributes, time=(start,end))

        #set up our data dictionaries
        duplicates[d] = dup
        keytimes[d] = {}
        itt[d] = {}
        ott[d] = {}
        weighted[d] = {}
        itw[d] = {}
        otw[d] = {}

        #if we're baking on ones, we don't need keytimes
        if not bakeOnOnes:
            for a in attributes:
                currKeytimes = mc.keyframe(s, attribute=a, time=(start,end), query=True, timeChange=True)
                if not currKeytimes:
                    continue

                keytimes[d][a] = currKeytimes
                allKeyTimes.extend(currKeytimes)

                #errors in maya 2016.5?
                try:
                    itt[d][a] = mc.keyTangent(s, attribute=a, time=(start,end), query=True, inTangentType=True)
                    ott[d][a] = mc.keyTangent(s, attribute=a, time=(start,end), query=True, outTangentType=True)
                except RuntimeError as err:
                    itt[d][a] = ['auto'] * len(currKeytimes)
                    ott[d][a] = ['auto'] * len(currKeytimes)

                if preserveTangentWeight and mc.keyTangent(s, attribute=a, query=True, weightedTangents=True)[0]:
                    weighted[d][a] = True
                    itw[d][a] = mc.keyTangent(s, attribute=a, time=(start,end), query=True, inWeight=True)
                    otw[d][a] = mc.keyTangent(s, attribute=a, time=(start,end), query=True, outWeight=True)

                #change fixed tangents to spline, because we can't set fixed tangents
                for i, each in enumerate(itt[d][a]):
                    if each == 'fixed':
                        itt[d][a][i] = 'spline'

                for i, each in enumerate(ott[d][a]):
                    if each == 'fixed':
                        ott[d][a][i] = 'spline'

                #add the start and end frames and tangents if they're not keyed
                if not start in keytimes[d][a]:
                    keytimes[d][a].insert(0,start)
                    itt[d][a].insert(0,'spline')
                    ott[d][a].insert(0,'spline')
                    if a in weighted[d]:
                        itw[d][a].insert(0, 1.0)
                        otw[d][a].insert(0, 1.0)
                if not end in keytimes[d][a]:
                    keytimes[d][a].append(end)
                    itt[d][a].append('spline')
                    ott[d][a].append('spline')
                    if a in weighted[d]:
                        itw[d][a].append(1.0)
                        otw[d][a].append(1.0)

                #reverse these, because we want to pop but start from the beginning
                itt[d][a].reverse()
                ott[d][a].reverse()
                if a in weighted[d]:
                    itw[d][a].reverse()
                    otw[d][a].reverse()


    if bakeOnOnes:
        allKeyTimes = list(range(int(start), int(end)+1))
    else:
        allKeyTimes = list(set(allKeyTimes))
        allKeyTimes.sort()

    with UndoChunk():
        #if 
        with IsolateViews():
            for frame in allKeyTimes:
                #cycle through all the frames
                mc.currentTime(frame, edit=True)
                for d in destination:
                    weightedSet = False
                    for a in attributes:
                        try:
                            v = mc.getAttr(duplicates[d]+'.'+a)
                            if bakeOnOnes:
                                mc.setKeyframe(d, attribute=a, time=frame,
                                               value=v,
                                               itt='spline',
                                               ott='spline')
                                mc.setAttr(d+'.'+a, v)
                            elif a in keytimes[d] and frame in keytimes[d][a]:
                                #tangent types line up with keytimes
                                mc.setKeyframe(d, attribute=a, time=frame,
                                               value=v,
                                               itt=itt[d][a].pop(),
                                               ott=ott[d][a].pop()
                                               )
                                mc.setAttr(d+'.'+a, v)

                        except:
                            pass

            #this was breaking the tangents inside the other loop, so run it after.
            if not bakeOnOnes and preserveTangentWeight:
                for d in destination:
                    for a in attributes:
                        if a in weighted[d]:
                            mc.keyTangent(d, attribute=a, edit=True, weightedTangents=True)
                            for frame in keytimes[d][a]:
                                mc.keyTangent(d, attribute=a, time=(frame,), edit=True, absolute=True, inWeight=itw[d][a].pop(), outWeight=otw[d][a].pop())

        #reset time and selection
        mc.currentTime(resetTime, edit=True)
        mc.select(destination, replace=True)

    mc.delete(list(duplicates.values()))
    if rotate:
        mc.filterCurve(mc.listConnections(destination,type='animCurve'))
    if bakeOnOnes:
        mc.keyTangent(destination, attribute=attributes, itt='spline', ott='spline')

def message(msg, position='midCenterTop'):
    
    OpenMaya.MGlobal.displayWarning(msg)
    fadeTime = min(len(msg)*100, 2000)
    mc.inViewMessage( amg=msg, pos=position, fade=True, fadeStayTime=fadeTime, dragKill=True)

def warning(msg):
    message(msg)
    OpenMaya.MGlobal.displayWarning(msg)

def error(msg):
    message(msg)
    OpenMaya.MGlobal.displayError(msg)

def minimizeRotationCurves(obj):
    '''
    Sets rotation animation to the value closest to zero.
    '''

    rotateCurves = mc.keyframe(obj, attribute=('rotateX','rotateY', 'rotateZ'), query=True, name=True)

    if not rotateCurves or len(rotateCurves) < 3:
        return

    keyTimes = mc.keyframe(rotateCurves, query=True, timeChange=True)
    tempFrame = sorted(keyTimes)[0] - 1

    #set a temp frame
    mc.setKeyframe(rotateCurves, time=(tempFrame,), value=0)

    #euler filter
    mc.filterCurve(rotateCurves)

    #delete temp key
    mc.cutKey(rotateCurves, time=(tempFrame,))


def renderShelfIcon(name='tmp', width=32, height=32):
    '''
    This renders a shelf-sized icon and hopefully places it in your icon directory
    '''
    imageName=name

    #getCamera
    cam = getCurrentCamera()

    #save these values for resetting
    currentRenderer = mc.getAttr('defaultRenderGlobals.currentRenderer')
    imageFormat = mc.getAttr('defaultRenderGlobals.imageFormat')

    mc.setAttr('defaultRenderGlobals.currentRenderer', 'mayaSoftware', type='string')

    imageFormat = 50 #XPM
    if MAYA_VERSION >= 2011:
        imageFormat = 32 #PNG

    mc.setAttr('defaultRenderGlobals.imageFormat', imageFormat)
    mc.setAttr('defaultRenderGlobals.imfkey', 'xpm', type='string')
    #here's the imageName
    mc.setAttr('defaultRenderGlobals.imageFilePrefix', imageName, type='string')

    mc.setAttr(cam+'.backgroundColor', 0.8,0.8,0.8, type='double3')
    #need to reset this afterward

    image = mc.render(cam, xresolution=width, yresolution=height)
    base = os.path.basename(image)

    #here we attempt to move the rendered icon to a more generalized icon location
    newPath = getIconPath()
    if newPath:
        newPath = os.path.join(newPath, base)
        shutil.move(image, newPath)
        image = newPath

    #reset
    mc.setAttr('defaultRenderGlobals.currentRenderer', currentRenderer, type='string')
    mc.setAttr('defaultRenderGlobals.imageFormat', imageFormat)

    return image


def setAnimValue(plug, value, tangentType=None):
    '''
    Sets key if the channel is keyed, otherwise setAttr
    '''

    if mc.keyframe(plug, query=True, name=True):
        mc.setKeyframe(plug, value=value)
        if tangentType:
            time = mc.currentTime(query=True)
            itt = tangentType
            ott = tangentType
            if tangentType == 'step':
                itt = 'linear'
            mc.keyTangent(plug, time=(time,), edit=True, itt=itt, ott=ott)

    mc.setAttr(plug, value)


class Dragger(object):

    def __init__(self,
                 name = 'mlDraggerContext',
                 title = 'Dragger',
                 defaultValue=0,
                 minValue=None,
                 maxValue=None,
                 multiplier=0.01,
                 cursor='hand'
                 ):

        self.multiplier = multiplier
        self.defaultValue = defaultValue
        self.minValue = minValue
        self.maxValue = maxValue
        #self.cycleCheck = mc.cycleCheck(query=True, evaluation=True)

        self.draggerContext = name
        if not mc.draggerContext(self.draggerContext, exists=True):
            self.draggerContext = mc.draggerContext(self.draggerContext)

        mc.draggerContext(self.draggerContext, edit=True,
                          pressCommand=self.press,
                          dragCommand=self.drag,
                          releaseCommand=self.release,
                          cursor=cursor,
                          drawString=title,
                          undoMode='all'
                          )


    def press(self, *args):
        '''
        Be careful overwriting the press method in child classes, because of the undoInfo openChunk
        '''

        self.anchorPoint = mc.draggerContext(self.draggerContext, query=True, anchorPoint=True)
        self.button = mc.draggerContext(self.draggerContext, query=True, button=True)

        # This turns off the undo queue until we're done dragging, so we can undo it.
        mc.undoInfo(openChunk=True)


    def drag(self, *args):
        '''
        This is what is actually run during the drag, updating the coordinates and calling the
        placeholder drag functions depending on which button is pressed.
        '''

        self.dragPoint = mc.draggerContext(self.draggerContext, query=True, dragPoint=True)

        #if this doesn't work, try getmodifier
        self.modifier = mc.draggerContext(self.draggerContext, query=True, modifier=True)

        self.x = ((self.dragPoint[0] - self.anchorPoint[0]) * self.multiplier) + self.defaultValue
        self.y = ((self.dragPoint[1] - self.anchorPoint[1]) * self.multiplier) + self.defaultValue

        if self.minValue is not None and self.x < self.minValue:
            self.x = self.minValue
        if self.maxValue is not None and self.x > self.maxValue:
            self.x = self.maxValue

        #dragString
        if self.modifier == 'control':
            if self.button == 1:
                self.dragControlLeft(*args)
            elif self.button == 2:
                self.dragControlMiddle(*args)
        elif self.modifier == 'shift':
            if self.button == 1:
                self.dragShiftLeft(*args)
            elif self.button == 2:
                self.dragShiftMiddle(*args)
        else:
            if self.button == 1:
                self.dragLeft()
            elif self.button == 2:
                self.dragMiddle()

        mc.refresh()

    def release(self, *args):
        '''
        Be careful overwriting the release method in child classes. Not closing the undo chunk leaves maya in a sorry state.
        '''
        # close undo chunk and turn cycle check back on
        mc.undoInfo(closeChunk=True)
        #mc.cycleCheck(evaluation=self.cycleCheck)
        mm.eval('SelectTool')

    def drawString(self, message):
        '''
        Creates a string message at the position of the pointer.
        '''
        mc.draggerContext(self.draggerContext, edit=True, drawString=message)

    def dragLeft(self,*args):
        '''Placeholder for potential commands. This is meant to be overridden by a child class.'''
        pass

    def dragMiddle(self,*args):
        '''Placeholder for potential commands. This is meant to be overridden by a child class.'''
        pass

    def dragControlLeft(self,*args):
        '''Placeholder for potential commands. This is meant to be overridden by a child class.'''
        pass

    def dragControlMiddle(self,*args):
        '''Placeholder for potential commands. This is meant to be overridden by a child class.'''
        pass

    def dragShiftLeft(self,*args):
        '''Placeholder for potential commands. This is meant to be overridden by a child class.'''
        pass

    def dragShiftMiddle(self,*args):
        '''Placeholder for potential commands. This is meant to be overridden by a child class.'''
        pass

    #no drag right, because that is monopolized by the right click menu
    #no alt drag, because that is used for the camera

    def setTool(self):
        mc.setToolTo(self.draggerContext)


class IsolateViews():
    '''
    Isolates selection with nothing selected for all viewports
    This speeds up any process that causes the viewport to refresh,
    such as baking or changing time.
    '''

    def __enter__(self):

        if MAYA_VERSION >= 2016.5:
            if not mc.ogs(query=True, pause=True):
                mc.ogs(pause=True)
        else:
            self.sel = mc.ls(sl=True)
            self.modelPanels = mc.getPanel(type='modelPanel')

            #unfortunately there's no good way to know what's been isolated, so in this case if a view is isolated, skip it.
            self.skip = []
            for each in self.modelPanels:
                if mc.isolateSelect(each, query=True, state=True):
                    self.skip.append(each)

            self.isolate(True)

            mc.select(clear=True)

        self.resetAutoKey = mc.autoKeyframe(query=True, state=True)
        mc.autoKeyframe(state=False)


    def __exit__(self, *args):

        #reset settings
        mc.autoKeyframe(state=self.resetAutoKey)

        if MAYA_VERSION >= 2016.5:
            if mc.ogs(query=True, pause=True):
                mc.ogs(pause=True)
        else:
            if self.sel:
                mc.select(self.sel)

            self.isolate(False)


    def isolate(self, state):

        mc.select(clear=True)
        for each in self.modelPanels:
            if not each in self.skip:
                mc.isolateSelect(each, state=state)


class KeySelection(object):
    '''

    '''

    def __init__(self, *args):

        #if args are passed in, this has been called from and out of date script. Warn and fail.
        if args:
            print('')
            print("Because of an update to ml_utilities, the tool you're trying to run is deprecated and needs to be updated as well.")
            print("Please visit http://morganloomis.com/tools and download the latest version of this tool.")
            OpenMaya.MGlobal.displayError('Tool out of date. See script editor for details.')
            return

        self.shortestTime = getFrameRate()/6000.0

        #node variables
        self.nodeSelection = mc.ls(sl=True)
        self._nodes = list()
        self._curves = list()
        self._channels = list()

        #time variables
        self.currentTime = mc.currentTime(query=True)
        self._time = None
        self._timeRangeStart = None
        self._timeRangeEnd = None

        #keyframe command variables
        self.selected = False

        #other housekeeping
        self._curvesCulled = False


    @property
    def curves(self):
        '''
        The keySelections's animation curve list.
        '''

        # if self._curves is False or None, then it has been initialized and curves haven't been found.
        if self._curves == []:

            #find anim curves connected to channels or nodes
            for each in (self._channels, self._nodes):
                if not each:
                    continue
                # this will only return time based keyframes, not driven keys
                self._curves = mc.keyframe(each, time=(':',), query=True, name=True)

                if self._curves:
                    self._curvesCulled = False
                    break
            if not self._curves:
                self._curves = False

        # need to remove curves which are unkeyable
        # supposedly referenced keys are keyable in 2013, I'll need to test that and update
        if self._curves and not self._curvesCulled:
            remove = list()
            for c in self._curves:
                if mc.referenceQuery(c, isNodeReferenced=True):
                    remove.append(c)
                else:
                    plug = mc.listConnections('.'.join((c,'output')), source=False, plugs=True)
                    if plug:
                        if not mc.getAttr(plug, keyable=True) and not mc.getAttr(plug, settable=True):
                            remove.append(c)
            if remove:
                for r in remove:
                    self._curves.remove(r)
            self._curvesCulled = True

        return self._curves


    @property
    def channels(self):
        '''
        The keySelection's channels list.
        '''

        if not self._channels:

            if self._curves:
                for c in self._curves:
                    self._channels.append(getChannelFromAnimCurve(c))
            elif self._nodes:
                for obj in self._nodes:
                    keyable = mc.listAttr(obj, keyable=True, unlocked=True, hasData=True, settable=True)
                    if keyable:
                        for attr in keyable:
                            self._channels.append('.'.join((obj, attr)))

        return self._channels

    @property
    def nodes(self):
        '''
        The keySelection's node list.
        '''

        if not self._nodes:

            if self._curves:
                self._nodes = list()
                for c in self._curves:
                    n = getChannelFromAnimCurve(c, plugs=False)
                    if not n in self._nodes:
                        self._nodes.append(n)
            elif self._channels:
                for each in self._channels:
                    n = each.split('.')[0]
                    if not n in self._nodes:
                        self._nodes.append(n)

        return self._nodes

    @property
    def args(self):
        '''
        This will return channels, curves or nodes in instances where we don't care which.
        It wont waste time converting from one to the other.
        '''
        if self._channels:
            return self._channels
        if self._curves:
            return self._curves
        if self._nodes:
            return self._nodes
        return None


    @property
    def time(self):
        '''
        The keySelection's time, formatted for maya's various keyframe command arguments.
        '''
        if self._time:
            if isinstance(self._time, list):
                return tuple(self._time)
            elif isinstance(self._time, float) or isinstance(self._time, int):
                return (self._time,)
            return self._time
        elif self._timeRangeStart and self._timeRangeEnd:
            return (self._timeRangeStart,self._timeRangeEnd)
        elif self._timeRangeStart:
            return (str(self._timeRangeStart)+':',)
        elif self._timeRangeEnd:
            return (':'+str(self._timeRangeEnd),)
        elif self.selected:
            #if keys are selected, get their times
            timeList = self.keyframe(query=True, timeChange=True)
            return tuple(set(timeList))
        return (':',)


    @property
    def times(self):
        '''
        This returns an expanded list of times, which is synced with the curve list.
        '''
        timeList = list()
        theTime = self.time
        for c in self.curves:
            curveTime = tuple(mc.keyframe(c, time=(theTime,), query=True, timeChange=True))
            if len(curveTime) == 1:
                curveTime = (curveTime[0],)
            timeList.append(curveTime)
        return timeList

    @property
    def values(self):
        valueList = list()
        for c in self.curves:
            curveValues = mc.keyframe(c, query=True, valueChange=True)
            if len(curveValues) == 1:
                curveValues = (curveValues[0],)
            valueList.append(curveValues)
        return valueList


    @property
    def initialized(self):
        '''
        Basically just tells if the object has been sucessfully initialized.
        '''
        return bool(self.args)


    def selectedObjects(self):
        '''
        Initializes the keySelection object with selected objects.
        Returns True if successful.
        '''

        if not self.nodeSelection:
            return False

        self._nodes = self.nodeSelection
        return True


    def selectedChannels(self):
        '''
        Initializes the keySelection object with selected channels.
        Returns True if successful.
        '''

        chanBoxChan = getSelectedChannels()

        if not chanBoxChan:
            return False

        #channels may be on shapes, include shapes in the list
        nodes = self.nodeSelection
        shapes = mc.listRelatives(self.nodeSelection, shapes=True, path=True)
        if shapes:
            nodes.extend(shapes)
            nodes = list(set(nodes))

        for obj in nodes:
            for attr in chanBoxChan:
                if mc.attributeQuery(attr, node=obj, exists=True):
                    self._channels.append('.'.join((obj,attr)))

        if not self._channels:
            return False

        return True


    def selectedLayers(self, includeLayerWeight=True):
        '''
        This affects keys on all layers that the node belongs to.
        If includeLayerWeight, the keys on the layer's weight attribute will be affected also.
        '''
        layers = getSelectedAnimLayers()
        curves = list()
        for layer in layers:
            layerCurves = mc.animLayer(layer, query=True, animCurves=True)
            if layerCurves:
                curves.extend(layerCurves)
            if includeLayerWeight:
                weightCurve = mc.keyframe(layer+'.weight', query=True, name=True)
                if weightCurve:
                    curves.append(weightCurve[0])
        self._curves = curves
        #we only want to use curves, since nodes or channels wont accurately represent all layers
        self._nodes = None
        self._channels = None


    def visibleInGraphEditor(self):
        '''
        Initializes the keySelection object with curves visibile in graph editor.
        Returns True if successful.
        '''


        if not 'graphEditor1' in mc.getPanel(visiblePanels=True):
            return False

        graphVis = mc.selectionConnection('graphEditor1FromOutliner', query=True, obj=True)

        if not graphVis:
            return False

        for each in graphVis:
            try:
                self._curves.extend(mc.keyframe(each, query=True, name=True))
            except Exception:
                pass


        if not self._curves:
            return False

        return True


    def selectedKeys(self):
        '''
        Initializes the keySelection object with selected keyframes.
        Returns True if successful.
        '''

        selectedCurves = mc.keyframe(query=True, name=True, selected=True)

        if not selectedCurves:
            return False
        self._curves = selectedCurves
        self.selected = True
        return True


    def keyedChannels(self, includeShapes=False):
        '''
        Initializes the keySelection object with keyed channels.
        Returns True if successful.
        '''

        if not self.nodeSelection:
            return False

        self._nodes = self.nodeSelection
        if includeShapes:
            shapes = mc.listRelatives(self.nodeSelection, shapes=True, path=True)
            if shapes:
                self._nodes.extend(shapes)

        #since self.curves is a property, it is actually finding curves from self._nodes
        if not self.curves:
            #if we don't find curves, reset nodes and fail
            self._nodes = None
            return False

        #reset self._nodes, otherwise they'll take priority over curves.
        self._nodes = None

        return True


    def keyedInHierarchy(self, includeRoot=True):
        '''
        Initializes the keySelection object with all the animation curves in the hierarchy.
        Returns True if successful.
        '''

        if not self.nodeSelection:
            return False

        tops = getRoots(self.nodeSelection)

        if not tops:
            #if we haven't been sucessful, we're done
            return False

        nodes = mc.listRelatives(tops, pa=True, type='transform', ad=True)
        if not nodes:
            nodes = list()

        if includeRoot:
            nodes.extend(tops)

        if not nodes:
            return False

        #now that we've determined the hierarchy, lets find keyed nodes
        #for node in nodes:
        # this will only return time based keyframes, not driven keys
        self._curves = mc.keyframe(nodes, time=(':',), query=True, name=True)

        #nodes or channels can be acessed by the node or channel property
        if not self._curves:
            return False

        return True


    def scene(self):
        '''
        Initializes the keySelection object with all animation curves in the scene.
        Returns True if successful.
        '''

        tl = mc.ls(type='animCurveTL')
        ta = mc.ls(type='animCurveTA')
        tu = mc.ls(type='animCurveTU')

        if tl:
            self._curves.extend(tl)
        if ta:
            self._curves.extend(ta)
        if tu:
            self._curves.extend(tu)

        if not self._curves:
            return False

        return True


    def selectedFrameRange(self):
        '''
        Sets the keySelection time to the selected frame range, returns false if frame range not selected.
        '''

        gPlayBackSlider = mm.eval('$temp=$gPlayBackSlider')
        if mc.timeControl(gPlayBackSlider, query=True, rangeVisible=True):
            self._timeRangeStart, self._timeRangeEnd = mc.timeControl(gPlayBackSlider, query=True, rangeArray=True)
            return True
        return False


    def frameRange(self):
        '''
        Sets the keySelection time to the selected frame range, or the current frame range.
        '''
        #this is selected range in the time slider
        self._timeRangeStart, self._timeRangeEnd = frameRange()


    def toEnd(self, includeCurrent=False):
        '''
        Sets the keySelection time to the range from the current frame to the last frame.
        Option to include the current frame.
        '''

        t = self.currentTime
        if not includeCurrent:
            t+=self.shortestTime
        self._timeRangeStart = t


    def fromBeginning(self, includeCurrent=False):
        '''
        Sets the keySelection time to the range from the first frame to the current frame.
        Option to include the current frame.
        '''

        t = self.currentTime
        if not includeCurrent:
            t-=self.shortestTime
        self._timeRangeEnd = t


    def keyRange(self):
        '''
        Sets the keySelection time range to the range of keys in the keySelection.
        '''

        keyTimes = self.getSortedKeyTimes()

        if not keyTimes or keyTimes[0] == keyTimes[-1]:
            return

        self._timeRangeStart = keyTimes[0]
        self._timeRangeEnd = keyTimes[-1]


    def currentFrame(self):
        '''
        Sets the keySelection time to the current frame.
        '''
        self._time = self.currentTime


    def previousKey(self):
        '''
        Sets the keySelection time to the previous key from the current frame.
        '''
        self._time = self.findKeyframe(which='previous')


    def nextKey(self):
        '''
        Sets the keySelection time to the next key from the current frame.
        '''
        self._time = self.findKeyframe(which='next')


    def setKeyframe(self, deleteSubFrames=False, **kwargs):
        '''
        Wrapper for the setKeyframe command. Curve and time arguments will be provided based on
        how this object was intitialized, otherwise usage is the same as maya's setKeyframe command.
        Option to delete sub-frames after keying.
        '''

        if not 'time' in kwargs:
            #still not sure about how I want to do this, but we need a discrete time.
            #if time is a string set to current time
            if isinstance(self.time, tuple) and (isinstance(self.time[0], str) or len(self.time)>1):
                kwargs['time'] = mc.currentTime(query=True)
            else:
                kwargs['time'] = self.time

        if 'insert' in kwargs and kwargs['insert'] == True:
            #setKeyframe fails if insert option is used but there's no keyframes on the channels.
            #key any curves with insert, then key everything again without it

            if self.curves:
                mc.setKeyframe(self.curves, **kwargs)
            kwargs['insert'] = False

        #want to try setting keys on nodes first, since certain setKeyframe arguments wont work
        #as expected with channels
        if self._nodes:
            mc.setKeyframe(self.nodes, **kwargs)
            self._curves = mc.keyframe(self.nodes, query=True, name=True)
        else:
            mc.setKeyframe(self.channels, **kwargs)
            self._curves = mc.keyframe(self.channels, query=True, name=True)

        #there's a new selection of curves, so reset the member variables
        self._channels = list()
        self._nodes = list()
        self._time = kwargs['time']

        if deleteSubFrames:
            #remove nearby sub-frames
            #this breaks at higher frame ranges because maya doesn't keep enough digits
            #this value is also different for different frame rates
            if self.currentTime % 1 == 0 and -9999 < self.currentTime < 9999:
                #the distance that keys can be is independent of frame rate, so we have to convert based on the frame rate.
                tol = self.shortestTime
                self.cutKey(time=(self.currentTime+tol, self.currentTime+0.5))
                self.cutKey(time=(self.currentTime-0.5, self.currentTime-tol))


    def keyframe(self,**kwargs):
        '''
        Wrapper for the keyframe command. Curve and time arguments will be provided based on
        how this object was intitialized, otherwise usage is the same as maya's keyframe command.
        '''
        if self.selected:
            #it's important that selection test first, becuase it's called by the time property
            kwargs['sl'] = True
        elif not 'time' in kwargs:
            kwargs['time'] = self.time

        return mc.keyframe(self.curves, **kwargs)


    def cutKey(self, includeSubFrames=False, **kwargs):
        '''
        Wrapper for the cutKey command. Curve and time arguments will be provided based on
        how this object was intitialized, otherwise usage is the same as maya's cutKey command.
        Option to delete sub-frames.
        '''

        if not 'includeUpperBound' in kwargs:
            kwargs['includeUpperBound'] = False

        if self.selected:
            mc.cutKey(sl=True, **kwargs)
            return

        if not 'time' in kwargs:
            if includeSubFrames:
                kwargs['time'] = (round(self.time[0])-0.5, round(self.time[-1])+0.5)
            else:
                kwargs['time'] = self.time
        mc.cutKey(self.curves, **kwargs)


    def copyKey(self, **kwargs):
        '''

        '''

        if not 'includeUpperBound' in kwargs:
            kwargs['includeUpperBound'] = False

        if self.selected:
            mc.copyKey(sl=True, **kwargs)
            return

        if not 'time' in kwargs:
            kwargs['time'] = self.time

        mc.copyKey(self.args, **kwargs)


    def pasteKey(self, option='replaceCompletely', **kwargs):
        '''

        '''
        mc.pasteKey(self.args, option=option, **kwargs)


    def selectKey(self,**kwargs):
        '''
        Wrapper for maya's selectKey command.
        '''

        if not 'time' in kwargs:
            kwargs['time'] = self.time
        mc.selectKey(self.curves, **kwargs)


    def moveKey(self, frames):
        '''
        A wrapper for keyframe -edit -timeChange
        '''

        if not frames:
            return

        self.keyframe(edit=True, relative=True, timeChange=frames)


    def scaleKey(self, timePivot=0, **kwargs):
        '''
        Wrapper for maya's scaleKey command.
        '''

        if not 'time' in kwargs:
            kwargs['time'] = self.time

        if timePivot == 'current':
            timePivot = self.currentTime

        mc.scaleKey(self.curves, timePivot=timePivot, **kwargs)


    def tangentType(self, **kwargs):
        '''
        Wrapper for maya's tangentType command.
        '''
        if not 'time' in kwargs:
            kwargs['time'] = self.time
        mc.tangentType(self.curves, **kwargs)


    def keyTangent(self, **kwargs):
        '''
        Wrapper for maya's keyTangent command.
        '''
        if not 'time' in kwargs:
            kwargs['time'] = self.time
        mc.keyTangent(self.curves, **kwargs)


    def findKeyframe(self, which='next', loop=False, roundFrame=False, **kwargs):
        '''
        This is similar to maya's findKeyframe, but operates on the keySelection and has options
        for rounding and looping.
        '''

        if which not in ('next','previous','first','last'):
            return

        if not roundFrame:
            if not loop or which == 'first' or which == 'last':
                #if there's not special options, just use default maya command for speed
                return mc.findKeyframe(self.args, which=which, **kwargs)

        keyTimes = self.getSortedKeyTimes()

        #if we don't find any, we're done
        if not keyTimes:
            return

        tolerence = 0.0
        if roundFrame:
            tolerence = 0.5

        if which == 'previous':
            findTime = keyTimes[-1]
            for x in reversed(keyTimes):
                if self.currentTime - x > tolerence:
                    findTime=x
                    break
        elif which == 'next':
            findTime = keyTimes[0]
            for x in keyTimes:
                if x - self.currentTime > tolerence:
                    findTime=x
                    break
        elif which == 'first':
            findTime = keyTimes[0]
        elif which == 'last':
            findTime = keyTimes[-1]

        if roundFrame:
            #round to nearest frame, if that option is selected
            findTime = round(findTime)

        return findTime


    def getSortedKeyTimes(self):
        '''
        Returns a list of the key times in order without duplicates.
        '''

        keyTimes = self.keyframe(query=True, timeChange=True)
        if not keyTimes:
            return
        return sorted(list(set(keyTimes)))



class MlUi(object):
    '''
    Window template for consistency
    '''

    def __init__(self, name, title, width=400, height=200, info='', menu=True, module=None):

        self.name = name
        self.title = title
        self.width = width
        self.height = height
        self.info = info
        self.menu = menu

        self.module = module
        if not module or module == '__main__':
            self.module = self.name

        #look for icon
        self.icon = getIcon(name)


    def __enter__(self):
        self.buildWindow()
        return self

    def __exit__(self, *args):
        self.finish()

    def buildWindow(self):
        '''
        Initialize the UI
        '''

        if mc.window(self.name, exists=True):
            mc.deleteUI(self.name)

        mc.window(self.name, title='ml :: '+self.title, iconName=self.title, width=self.width, height=self.height, menuBar=self.menu)


        if self.menu:
            self.createMenu()

        self.form = mc.formLayout()
        self.column = mc.columnLayout(adj=True)


        mc.rowLayout( numberOfColumns=2, columnWidth2=(34, self.width-34), adjustableColumn=2,
                      columnAlign2=('right','left'),
                      columnAttach=[(1, 'both', 0), (2, 'both', 8)] )

        #if we can find an icon, use that, otherwise do the text version
        if self.icon:
            mc.iconTextStaticLabel(style='iconOnly', image1=self.icon)
        else:
            mc.text(label=' _ _ |\n| | | |')

        if not self.menu:
            mc.popupMenu(button=1)
            mc.menuItem(label='Help', command=(_showHelpCommand(TOOL_URL+self.name+'/')))

        mc.text(label=self.info)
        mc.setParent('..')
        mc.separator(height=8, style='single', horizontal=True)


    def finish(self):
        '''
        Finalize the UI
        '''

        mc.setParent(self.form)

        frame = mc.frameLayout(labelVisible=False)
        mc.helpLine()

        mc.formLayout( self.form, edit=True,
                       attachForm=((self.column, 'top', 0), (self.column, 'left', 0),
                                   (self.column, 'right', 0), (frame, 'left', 0),
                                   (frame, 'bottom', 0), (frame, 'right', 0)),
                       attachNone=((self.column, 'bottom'), (frame, 'top')) )

        mc.showWindow(self.name)
        mc.window(self.name, edit=True, width=self.width, height=self.height)


    def createMenu(self, *args):
        '''
        Create the main menu for the UI
        '''

        #generate shelf label by removing ml_
        shelfLabel = self.name.replace('ml_','')
        module = self.module
        if not module:
            module = self.name

        #if icon exists, use that
        argString = ''
        if not self.icon:
            argString = ', label="'+shelfLabel+'"'

        mc.menu(label='Tools')
        mc.menuItem(label='Add to shelf',
                    command='import ml_utilities;ml_utilities.createShelfButton("import '+module+';'+module+'.ui()", name="'+self.name+'", description="Open the UI for '+self.name+'."'+argString+')')
        if not self.icon:
            mc.menuItem(label='Get Icon',
                        command=(_showHelpCommand(ICON_URL+self.name+'.png')))
        mc.menuItem(label='Get More Tools!',
                    command=(_showHelpCommand(WEBSITE_URL+'/tools/')))
        mc.setParent( '..', menu=True )

        mc.menu(label='Help')
        mc.menuItem(label='About', command=self.about)
        mc.menuItem(label='Documentation', command=(_showHelpCommand(TOOL_URL+self.name+'/')))
        mc.menuItem(label='Python Command Documentation', command=(_showHelpCommand(TOOL_URL+'#\%5B\%5B'+self.name+'\%20Python\%20Documentation\%5D\%5D')))
        mc.menuItem(label='Submit a Bug or Request', command=(_showHelpCommand(WEBSITE_URL+'/about/')))

        mc.setParent( '..', menu=True )


    def about(self, *args):
        '''
        This pops up a window which shows the revision number of the current script.
        '''

        text='by Morgan Loomis\n\n'
        try:
            __import__(self.module)
            module = sys.modules[self.module]
            text = text+'Revision: '+str(module.__revision__)+'\n'
        except Exception:
            pass
        try:
            text = text+'ml_utilities Rev: '+str(__revision__)+'\n'
        except Exception:
            pass

        mc.confirmDialog(title=self.name, message=text, button='Close')


    def buttonWithPopup(self, label=None, command=None, annotation='', shelfLabel='', shelfIcon='render_useBackground', readUI_toArgs={}):
        '''
        Create a button and attach a popup menu to a control with options to create a shelf button or a hotkey.
        The argCommand should return a kwargs dictionary that can be used as args for the main command.
        '''

        if self.icon:
            shelfIcon = self.icon

        if annotation and not annotation.endswith('.'):
            annotation+='.'

        button = mc.button(label=label, command=command, annotation=annotation+' Or right click for more options.')

        mc.popupMenu()
        self.shelfMenuItem(command=command, annotation=annotation, shelfLabel=shelfLabel, shelfIcon=shelfIcon)
        self.hotkeyMenuItem(command=command, annotation=annotation)
        return button


    def shelfMenuItem(self, command=None, annotation='', shelfLabel='', shelfIcon='menuIconConstraints', menuLabel='Create Shelf Button'):
        '''
        This creates a menuItem that can be attached to a control to create a shelf menu with the given command
        '''
        pythonCommand = 'import '+self.name+';'+self.name+'.'+command.__name__+'()'

        mc.menuItem(label=menuLabel,
                    command='import ml_utilities;ml_utilities.createShelfButton(\"'+pythonCommand+'\", \"'+shelfLabel+'\", \"'+self.name+'\", description=\"'+annotation+'\", image=\"'+shelfIcon+'\")',
                    enableCommandRepeat=True,
                    image=shelfIcon)


    def hotkeyMenuItem(self, command=None, annotation='', menuLabel='Create Hotkey'):
        '''
        This creates a menuItem that can be attached to a control to create a hotkey with the given command
        '''
        melCommand = 'import '+self.name+';'+self.name+'.'+command.__name__+'()'
        mc.menuItem(label=menuLabel,
                    command='import ml_utilities;ml_utilities.createHotkey(\"'+melCommand+'\", \"'+self.name+'\", description=\"'+annotation+'\")',
                    enableCommandRepeat=True,
                    image='commandButton')


    def selectionField(self, label='', annotation='', channel=False, text=''):
        '''
        Create a field with a button that adds the selection to the field.
        '''
        field = mc.textFieldButtonGrp(label=label, text=text,
                                      buttonLabel='Set Selected')
        mc.textFieldButtonGrp(field, edit=True, buttonCommand=partial(self._populateSelectionField, channel, field))
        return field


    def _populateSelectionField(self, channel, field, *args):

        selectedChannels = None
        if channel:
            selectedChannels = getSelectedChannels()
            if not selectedChannels:
                raise RuntimeError('Please select an attribute in the channelBox.')
            if len(selectedChannels) > 1:
                raise RuntimeError('Please select only one attribute.')

        sel = mc.ls(sl=True)
        if not sel:
            raise RuntimeError('Please select a node.')
        if len(sel) > 1:
            raise RuntimeError('Please select only one node.')

        selection = sel[0]
        if selectedChannels:
            selection = selection+'.'+selectedChannels[0]

        mc.textFieldButtonGrp(field, edit=True, text=selection)


    def selectionList(self, channel=False, **kwargs):
        tsl = mc.textScrollList(**kwargs)
        mc.button(label='Append Selected', command=partial(self._populateSelectionList, channel, tsl))
        return tsl


    def _populateSelectionList(self, channel, control, *args):

        selectedChannels = None
        if channel:
            selectedChannels = getSelectedChannels()
            if not selectedChannels:
                raise RuntimeError('Please select an attribute in the channelBox.')
            if len(selectedChannels) > 1:
                raise RuntimeError('Please select only one attribute.')

        sel = mc.ls(sl=True)
        if not sel:
            raise RuntimeError('Please select a node.')
        if len(sel) > 1:
            raise RuntimeError('Please select only one node.')

        selection = sel[0]
        if selectedChannels:
            selection = selection+'.'+selectedChannels[0]

        mc.textScrollList(control, edit=True, append=[selection])


    class ButtonWithPopup():

        def __init__(self, label=None, name=None, command=None, annotation='', shelfLabel='', shelfIcon='render_useBackground', readUI_toArgs={}, **kwargs):
            '''
            The fancy part of this object is the readUI_toArgs argument.
            '''

            self.uiArgDict = readUI_toArgs
            self.name = name
            self.command = command
            self.kwargs = kwargs

            self.annotation = annotation
            self.shelfLabel = shelfLabel
            self.shelfIcon = shelfIcon

            if annotation and not annotation.endswith('.'):
                annotation+='.'

            button = mc.button(label=label, command=self.runCommand, annotation=annotation+' Or right click for more options.')

            mc.popupMenu()
            mc.menuItem(label='Create Shelf Button', command=self.createShelfButton, image=shelfIcon)

            mc.menuItem(label='Create Hotkey',
                        command=self.createHotkey, image='commandButton')


        def readUI(self):
            '''
            This reads the UI elements and turns them into arguments saved in a kwargs style member variable
            '''

            if self.uiArgDict:
                #this is some fanciness to read the values of UI elements and generate or run the resulting command
                #keys represent the argument names, the values are UI elements
                for k in list(self.uiArgDict.keys()):

                    uiType = mc.objectTypeUI(self.uiArgDict[k])
                    value = None
                    if uiType == 'rowGroupLayout':
                        controls = mc.layout(self.uiArgDict[k], query=True, childArray=True)
                        if 'check1' in controls:
                            value = mc.checkBoxGrp(self.uiArgDict[k], query=True, value1=True)
                        elif 'radio1' in controls:
                            #this will be a 1 based index, we want to return formatted button name?
                            value = mc.radioButtonGrp(self.uiArgDict[k], query=True, select=True)-1
                        elif 'slider' in controls:
                            try:
                                value = mc.floatSliderGrp(self.uiArgDict[k], query=True, value=True)

                            except Exception:
                                pass
                            try:
                                value = mc.intSliderGrp(self.uiArgDict[k], query=True, value=True)

                            except Exception:
                                pass
                        elif 'field1' in controls:
                            value = mc.floatFieldGrp(self.uiArgDict[k], query=True, value1=True)
                        elif 'OptionMenu' in controls:
                            value = mc.optionMenuGrp(self.uiArgDict[k], query=True, select=True)
                    else:
                        OpenMaya.MGlobal.displayWarning('Cannot read '+uiType+' UI element: '+self.uiArgDict[k])
                        continue

                    self.kwargs[k] = value


        def runCommand(self, *args):
            '''
            This compiles the kwargs and runs the command directly
            '''
            self.readUI()
            self.command(**self.kwargs)


        def stringCommand(self):
            '''
            This takes the command
            '''

            cmd = 'import '+self.name+'\n'+self.name+'.'+self.command.__name__+'('

            comma = False
            for k,v in list(self.kwargs.items()):
                value = v
                if isinstance(v, str):
                    value = "'"+value+"'"
                else:
                    value = str(value)

                if comma:
                    cmd+=', '
                cmd = cmd+k+'='+value

                comma = True

            cmd+=')'

            return cmd


        def createShelfButton(self,*args):
            '''
            Builds the command and creates a shelf button out of it
            '''
            self.readUI()
            pythonCommand = self.stringCommand()
            createShelfButton(pythonCommand, self.shelfLabel, self.name, description=self.annotation, image=self.shelfIcon)


        def createHotkey(self, annotation='', menuLabel='Create Hotkey'):
            '''
            Builds the command and prompts to create a hotkey.
            '''

            self.readUI()
            pythonCommand = self.stringCommand()
            createHotkey(pythonCommand, self.name, description=self.annotation)


class SkipUndo():
    '''
    Skips adding the encapsulated commands to the undo queue, so that you
    cannot undo them.
    '''

    def __enter__(self):
        '''
        Turn off undo
        '''
        mc.undoInfo(stateWithoutFlush=False)

    def __exit__(self,*args):
        '''
        Turn on undo
        '''
        mc.undoInfo(stateWithoutFlush=True)


class UndoChunk():
    '''
    In versions of maya before 2011, python doesn't always undo properly, so in
    some cases we have to manage the undo queue ourselves.
    '''

    def __init__(self, force=False):
        self.force = force

    def __enter__(self):
        '''open the undo chunk'''
        if self.force or MAYA_VERSION < 2011:
            self.force = True
            mc.undoInfo(openChunk=True)

    def __exit__(self, *args):
        '''close the undo chunk'''
        if self.force:
            mc.undoInfo(closeChunk=True)


class Vector:

    def __init__(self, x=0, y=0, z=0):
        '''
        Initialize the vector with 3 values, or else
        '''

        if self._isCompatible(x):
            x = x[0]
            y = x[1]
            z = x[2]
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Vector({0:.2f}, {1:.2f}, {2:.2f})'.format(*self)

    #iterator methods
    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __getitem__(self, key):
        return (self.x, self.y, self.z)[key]

    def __setitem__(self, key, value):
        [self.x, self.y, self.z][key] = value

    def __len__(self):
        return 3

    def _isCompatible(self, other):
        '''
        Return true if the provided argument is a vector
        '''
        if isinstance(other,(Vector,list,tuple)) and len(other)==3:
            return True
        return False


    def __add__(self, other):

        if not self._isCompatible(other):
            raise TypeError('Can only add to another vector of the same dimension.')

        return Vector(*[a+b for a,b in zip(self,other)])


    def __sub__(self, other):

        if not self._isCompatible(other):
            raise TypeError('Can only subtract another vector of the same dimension.')

        return Vector(*[a-b for a,b in zip(self,other)])


    def __mul__(self, other):

        if self._isCompatible(other):
            return Vector(*[a*b for a,b in zip(self,other)])
        elif isinstance(other, (float,int)):
            return Vector(*[x*float(other) for x in self])
        else:
            raise TypeError("Can't multiply {} with {}".format(self, other))

    def __div__(self, other):
        '''
        Python 2.7
        '''
        if isinstance(other, (float,int)):
            return Vector(*[x/float(other) for x in self])
        else:
            raise TypeError("Can't divide {} by {}".format(self, other))
    
    def __truediv__(self, other):
        '''
        Python 3
        '''
        if isinstance(other, (float,int)):
            return Vector(*[x/float(other) for x in self])
        else:
            raise TypeError("Can't divide {} by {}".format(self, other))

    def magnitude(self):
        return math.sqrt(sum([x**2 for x in self]))

    def delta(self, other):
        return self - other

    def distance(self, other):
        return self.delta(other).magnitude()

    def equivalent(self, other, tolerence=0.001):
        if self.distance(other) < tolerence:
            return True
        return False

    def normalize(self):
        d = self.magnitude()
        if d:
            self.x /= d
            self.y /= d
            self.z /= d
        return self


    def normalized(self):
        d = self.magnitude()
        if d:
            return self/d
        return self


    def dot(self, other):
        if not self._isCompatible(other):
            raise TypeError('Can only perform dot product with another Vector object of equal dimension.')
        return sum([a*b for a,b in zip(self,other)])


    def cross(self, other):
        if not self._isCompatible(other):
            raise TypeError('Can only perform cross product with another Vector object of equal dimension.')
        return Vector(self.y * other.z - self.z * other.y,
                       -self.x * other.z + self.z * other.x,
                       self.x * other.y - self.y * other.x)

    def axis_angle(self, other):
        if not self._isCompatible(other):
            raise TypeError('Vectors arent compatible for axis/angle.')
        a = self.normalized()
        b = other.normalized()
        angle = math.acos(a.dot(b))
        axis = a.cross(b)
        return axis,angle


class Matrix:

    def __init__(self, *args):
        '''
        Initialize the vector with either a maya matrix, or a 16 item array
        '''
        self._array = None

        if not args:
            self._array = [1,0,0,0,
                          0,1,0,0,
                          0,0,1,0,
                          0,0,0,1]
        elif len(args) == 1:
            if isinstance(args[0], Matrix):
                self._array = args[0]._array
            elif isinstance(args[0], om.MMatrix):
                self._array = [x for x in args[0]]
            elif isinstance(args[0], (list,tuple)) and len(args[0]) == 16:
                self._array = args[0]
        elif len(args) == 16:
            self._array = args
        
    def __repr__(self):
        return 'Matrix({0:.2f},{1:.2f},{2:.2f} ... {4:.2f},{5:.2f},{6:.2f} ... {8:.2f},{9:.2f},{10:.2f} ... {12:.2f},{13:.2f},{14:.2f})'.format(*self)

    #iterator methods
    def __iter__(self):
        return iter(self.array)

    def __getitem__(self, key):
        return self.array[key]

    def __setitem__(self, key, value):
        self.array[key] = value
        self._MMatrix = None
        self._MTransformMatrix = None

    def __len__(self):
        return 16
    
    def __mul__(self, other):

        if not isinstance(other, Matrix):
            raise TypeError('Other matrix must be a Matrix type.')
        return Matrix(self.MMatrix * other.MMatrix)
    
    @property
    def MMatrix(self):
        return om.MMatrix(self._array)
    
    @property
    def MTransformMatrix(self):
        return om.MTransformMatrix(self.MMatrix)
    
    def inverse(self):
        return Matrix(self.MMatrix.inverse())
    
    @property
    def x(self):
        return Vector(self._array[0],self._array[1],self._array[2])
        
    @property
    def y(self):
        return Vector(self._array[4],self._array[5],self._array[6])
        
    @property
    def z(self):
        return Vector(self._array[8],self._array[9],self._array[10])
    
    def translate(self):
        return self.MTransformMatrix.translation(om.MSpace.kWorld)

    def rotate(self, rotateOrder):
        r = self.MTransformMatrix.trotation(om.MSpace.kWorld, asQuaternion=False)
        return [math.degrees(x) for x in r]
        
    def scale(self):
        return self.MTransformMatrix.tscale(om.MSpace.kWorld)

    def mult_point(self, point):
        pass
    
#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: : First publish
#
# Revision 2: 2011-05-04 : Fixed error in frameRange.
#
# Revision 3: 2012-05-31 : Adding Menu and Icon update to UI, adding KeyframeSelection object, and a few random utility functions.
#
# Revision 4: 2012-06-01 : Fixing bug with UI icons
#
# Revision 5: 2012-07-23 : Expanding and bug fixing Keyselection, added SkipUndo, minor bug fixes.
#
# Revision 6: 2012-07-23 : KeySelection bug fix
#
# Revision 7: 2012-08-07 : Minor bug with Keyselection, adding functions.
#
# Revision 8: 2012-11-06 : Backwards incompatable update to KeySelection, and several new functions.
#
# Revision 9: 2013-10-29 : Update to support more options for goToKeyframe, update to preserve isolateSelect.
#
# Revision 10: 2014-03-01 : adding category, updating contact.
#
# Revision 11: 2014-03-08 : Fixed keySelection bug with keyed channels.
#
# Revision 12: 2015-04-27 : updated for ml_puppet support
#
# Revision 13: 2015-05-13 : UI function updates
#
# Revision 14: 2015-05-16 : minor update to setAnimValue
#
# Revision 15: 2015-05-18 : Small bugfix in matchBake
#
# Revision 16: 2016-02-29 : Support for animCurveEditor and fixing some old hotkey bugs.
#
# Revision 17: 2016-03-23 : keySelection bug fix.
#
# Revision 18: 2016-05-05 : Update matchBake to support tangent weights.
#
# Revision 19: 2016-06-02 : temp patching hotkey issue with > 2015
#
# Revision 20: 2016-07-31 : Update to MlUi to support subclassing.
#
# Revision 21: 2016-07-31 : MlUi bug fixes.
#
# Revision 21: 2016-08-11 : windows support for icons
#
# Revision 22: 2016-10-01 : changing frameRange to return consistent results when returning timeline or selection.
#
# Revision 23: 2016-10-12 : Tangent bug fixes for 2016.5
#
# Revision 24: 2016-10-31 : Adding selection field to mlUI
#
# Revision 25: 2016-11-21 : silly icon path bug
#
# Revision 26: 2016-12-05 : Adding getSkinCluster
#
# Revision 27: 2016-12-10 : Adding Vector class to remove euclid dependency
#
# Revision 28: 2017-03-20 : bug fix and support for ml_puppet
#
# Revision 29: 2017-04-25 : matchBake support input frames
#
# Revision 30: 2017-06-13 : unify version test, isolate view update
#
# Revision 31: 2017-06-30 : getCamera support for stereo camera
#
# Revision 32: 2018-02-17 : Updating license to MIT.
#
# Revision 33: 2018-07-18 : getNamespace bug
#
# Revision 34: 2019-03-07 : github URL update