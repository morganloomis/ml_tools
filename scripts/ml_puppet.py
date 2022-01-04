# -= ml_puppet.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 24
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_puppet.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_puppet
#     ml_puppet.main()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Support tools for puppets.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Launch the UI to see the options available. Press a button to make a selection
# or run a command. Right click buttons to create a hotkey for that option. All
# options are selection-sensitive, so for example if you have two puppets
# referenced into a scene, and select any part of one of them and run
# selectControls, it will select all the controls for that puppet only. With
# nothing selected it will select all controls in the scene. For Fk/Ik switching,
# select any part of the element you want to switch. So for an arm, you can select
# the ik hand control, the fk shoulder, the pole vector, and either way it will
# know to do the switch for that arm.
# 
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
__category__ = 'None'
__revision__ = 24

import maya.cmds as mc
import maya.mel as mm
from functools import partial
import math, re, warnings, os

try:
    import ml_utilities as utl
    utl.upToDateCheck(35)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/tool/ml_utilities/',absolute=True)

ml_convertRotationOrder = None
try:
    import ml_convertRotationOrder
except ImportError:
    pass

ml_resetChannels = None
try:
    import ml_resetChannels
except ImportError:
    pass

ml_copyAnim = None
try:
    import ml_copyAnim
except ImportError:
    pass


PUP_ID_PREFIX = 'pupID_'
CONTROL_ATTR = PUP_ID_PREFIX+'control'
APPENDAGE_ATTR = 'puppeteer_appendage'

def main():
    initPuppetContextMenu()


def ui():

    with utl.MlUi('ml_puppet', 'Puppet Interface', width=400, height=130, info='''Support tools for Puppets, including group selection and fk/ik switching.
Selection tools and switching tools are based on element selection.
Right click buttons to create hotkeys.''') as win:
        win.ButtonWithPopup(label='Select Puppets', name=win.name, command=selectPuppets,
                            annotation='Selects the puppet top node(s) of a given selection. No selection selects all puppets in scene.')
        win.ButtonWithPopup(label='Select All Controls', name=win.name, command=selectControls,
                            annotation='Select all controls for the selected puppet. No selection selects all controls in scene.')
        win.ButtonWithPopup(label='Select All Element Controls', name=win.name, command=selectElementControls,
                            annotation='Select all controls within a selected element.')
        win.ButtonWithPopup(label='Fk/Ik Switch', name=win.name, command=fkIkSwitchUI,
                            annotation='Toggle selected element between FK and IK.')
        #win.ButtonWithPopup(label='Space Switch', name=win.name, command=spaceSwitchUI,
        #                            annotation='Toggle selected element between FK and IK.')


def fkIkSwitchUI(*args):

    with utl.MlUi('ml_puppet', 'Puppet Interface', width=400, height=130, info='''Support tools for Puppets, including group selection and fk/ik switching.
Selection tools and switching tools are based on element selection.
Right click buttons to create hotkeys.''') as win:

        win.ButtonWithPopup(label='Fk/Ik Switch Current Frame', name=win.name, command=fkIkSwitchSel,
                            annotation='Toggle selected element between FK and IK.')
        win.ButtonWithPopup(label='Fk/Ik Switch Frame Range', name=win.name, command=fkIkSwitchRangeSel,
                            annotation='Bake selected element from FK to IK and vice versa.')


class SpaceSwitchUI(object):
    
    win_name = 'spaceSwitchWin'
    
    def __init__(self, title='SpaceSwitch', width=400, height=200):
        
        
        sel = mc.ls(sl=True)
        if not sel:
            return 
        
        spaces = None
        nodes = []
        for each in sel:
            data = getSpaceSwitchData(each)
            if not data:
                continue
            nodes.append(each)
            theseSpaces = set(data['space']['enumValues'])
            if not spaces:
                spaces = theseSpaces
            else:
                spaces.intersection(theseSpaces)
        
        if not spaces:
            return
        
        self.width = width
        self.height = height
        
        self.close()

        mc.window(self.win_name, title=title, iconName=title, width=self.width, height=self.height, menuBar=True)
        self.column = mc.columnLayout(adj=True)
        
        for space in list(spaces):
            mc.button(space, command=partial(self.setSpace, nodes, space))
        
        self.show()
        
        
    def setSpace(self, nodes, space, *args):
        switchSpace(nodes=nodes, toSpace=space, switchRange=True, bakeOnOnes=False)
        self.close()
        
    def close(self):
        if mc.window(self.win_name, exists=True):
            mc.deleteUI(self.win_name)
    
    def show(self):
        mc.showWindow(self.win_name)
        mc.window(self.win_name, edit=True, width=self.width, height=self.height)
            
    

def fkIkSwitchSel(*args):
    fkIkSwitch()


def fkIkSwitchRangeSel(*args):
    fkIkSwitch(switchRange=True)


def getPuppets(node=None):
    
    #LEGACY:
    if node:
        puppets = []
        if not isinstance(node, (list,tuple)):
            node = [node]
        for n in node:
            if getNodeType(n) == 'puppet':
                puppets.append(n)
            else:
                above = getNodeTypeAbove(n,'puppet')
        if puppets:
            return puppets
    return getNodesOfType('puppet')


def selectPuppets(nodes=None, *args):

    pups = getPuppets(nodes)
    if pups:
        mc.select(pups)


def getControls(nodes=None):
    return getNodesOfType('control', namespaceFromNodes=nodes)


def selectControls(nodes=None, *args):
    ctrls = getControls(nodes=nodes)
    if ctrls:
        mc.select(ctrls)


def getWorldSpaceControls(nodes, *args):

    ctrls = getControls(nodes=nodes)
    if not ctrls:
        return
    wsCtrls = []
    for ctrl in ctrls:
        if getTag(ctrl, 'baseName') == 'root':
            wsCtrls.append(ctrl)
            continue

        ssData = getSpaceSwitchData(ctrl)
        if not ssData:
            continue

        for attr, value in list(ssData.items()):
            if value['currentValue'] == 'World':
                wsCtrls.append(ctrl)
                break
    return wsCtrls


def selectWorldSpaceControls(nodes, *args):
    ctrls = getWorldSpaceControls(nodes)
    if ctrls:
        mc.select(ctrls)


def selectKeyed(nodes, *args):
    if nodes:
        mc.select(nodes)
    keySel = utl.KeySelection()
    if keySel.keyedInHierarchy():
        mc.select(keySel.nodes, replace=True)
    else:
        mc.select(clear=True)


def selectIkControls(nodes, *args):
    ctrls = getControls(nodes)
    if not ctrls:
        return
    mc.select( [x for x in ctrls if getTag(x, 'descriptor') == 'ik'])


def selectFkControls(nodes, *args):
    ctrls = getControls(nodes)
    if not ctrls:
        return
    mc.select( [x for x in ctrls if getTag(x, 'descriptor') == 'fk'])


def invertSelection(nodes, *args):

    ctrls = getControls(nodes)
    if not ctrls:
        return
    sel = mc.ls(sl=True)
    if not sel:
        mc.select(ctrls)
    else:
        mc.select([x for x in ctrls if x not in sel])

def getElementControls(nodes=None):

    if not nodes:
        nodes = mc.ls(sl=True)
    elements = getElementsAbove(nodes)
    if not elements:
        return
    controls = []
    for element in elements:
        controlsBelow = getNodesOfTypeBelow(element, 'control')
        if controlsBelow:
            controls.extend(controlsBelow)
    return controls


def selectElementControls(nodes=None, *args):
    ctrls = getElementControls(nodes=nodes)
    if ctrls:
        mc.select(ctrls)

def get_appendage(node):
    if mc.attributeQuery(APPENDAGE_ATTR, node=node, exists=True):
        return node
    parent = mc.listRelatives(node, parent=True, pa=True)
    if parent:
        return get_appendage(parent[0])
    return None


def getElementsAbove(nodes=None):
    '''
    Legacy, no longer used.
    '''
    elements = []
    if not nodes:
        nodes = mc.ls(sl=True)
    for each in nodes:
        if getNodeType(each) in ['element','puppet']:
            elements.append(each)
        else:
            elem = getNodeTypeAbove(each, 'element')
            if elem:
                elements.append(elem)
    return list(set(elements))


def selectElements(nodes=None, *args):

    elems = getElementsAbove(nodes=nodes)
    if elems:
        mc.select(elems)


def getNodeTypeAbove(node, nodeType):
    '''
    This is a recursive function.
    '''
    parent = mc.listRelatives(node, parent=True)
    if not parent:
        return False
    if getNodeType(parent[0]) == nodeType:
        return parent[0]
    return getNodeTypeAbove(parent[0], nodeType)


def getNodesOfTypeBelow(node, nodeType):
    nodes = []
    allKids = mc.listRelatives(node, ad=True, pa=True)
    for kid in allKids:
        if mc.attributeQuery(PUP_ID_PREFIX+nodeType, exists=True, node=kid):
            nodes.append(kid)
    return nodes


def getTag(node, tag):

    ntAttr = PUP_ID_PREFIX+tag
    if mc.attributeQuery(ntAttr, exists=True, node=node):
        return mc.getAttr(node+'.'+ntAttr)
    return False


def getNodeType(node):
    if mc.attributeQuery('asset_type', node=node, exists=True):
        return mc.getAttr(node+'.asset_type', asString=True)
    return getTag(node, 'nodeType')


def getNodesOfType(nodeType, namespaceFromNodes=None):

    allNodes = []

    #if something is selected, get it from within that namespace.
    if not namespaceFromNodes:
        namespaceFromNodes = mc.ls(sl=True)
    namespaces = []
    if namespaceFromNodes:
        for each in namespaceFromNodes:
            namespaces.append(utl.getNamespace(each))
    else:
        namespaces = ['*:','']
    for ns in list(set(namespaces)):
        if nodeType == 'control' or nodeType == 'element' or nodeType == 'puppet':
            #special case for commonly queried nodes, for speed
            #get with and without namespaces
            allNodes.extend(mc.ls(ns+'*.'+PUP_ID_PREFIX+nodeType, o=True))
    return allNodes


def showAllControls(puppet, *args):

    elements = mc.listRelatives(puppet, pa=True)
    for element in elements:
        for visAttr in ('geoVisibility','controlVisibility','secondaryControlVisibility'):
            if mc.attributeQuery(visAttr, exists=True, node=element):
                mc.setAttr(element+'.'+visAttr, 1)

def snap(node, snapTo):

    #duplicate the node we want snap
    dup = mc.duplicate(node, parentOnly=True)[0]
    #unlock translates and rotates
    for a in ('.t','.r'):
        for b in 'xyz':
            mc.setAttr(dup+a+b, lock=False)

    mc.parentConstraint(snapTo, dup)

    for a in ('.t','.r'):
        for b in ('x','y','z'):
            try:
                mc.setAttr(node+a+b, mc.getAttr(dup+a+b))
            except Exception:
                pass

    mc.delete(dup)


def hasFlippedParent(node, testRange=3):

    parent = mc.listRelatives(node, parent=True, pa=True)
    for null in range(testRange):
        if not parent:
            return False
        if mc.getAttr(parent[0]+'.scaleX') < 0:
            return True
        parent = mc.listRelatives(parent[0], parent=True, pa=True)
    return False


def fkIkData(element):

    #here's all the attributes we need:
    switchAttr = 'fkIkSwitch'
    fkAttr = 'pup_fkControls'
    ikAttr = 'pup_ikControls'
    legacyIkAttr = 'pup_ikControl'

    pvAttr = 'pup_pvControl'
    matchToAttr = 'pup_matchTo'
    #pvMatchToAttr = 'pup_pv_matchTo'
    aimMatchToAttr = 'pup_aim_matchTo'

    data = {}

    #if this is an fk/ik switchable attribute
    if not mc.attributeQuery(switchAttr, node=element, exists=True):
        return
    if not mc.attributeQuery(fkAttr, node=element, exists=True):
        return
    if not mc.attributeQuery(ikAttr, node=element, exists=True) and not mc.attributeQuery(legacyIkAttr, node=element, exists=True):
        return

    #these are the nodes we need to find
    data['fkChain'] = []
    data['ikControls'] = []
    data['pvControl'] = None

    data['baseChain'] = []
    data['ikMatchTo'] = []

    #get the fk chain
    for i in range(mc.getAttr(element+'.'+fkAttr, size=True)):
        con = mc.listConnections('%s.%s[%s]' % (element,fkAttr,i), source=True, destination=False)
        if con:
            data['fkChain'].append(con[0])

    for x in data['fkChain']:
        if not mc.attributeQuery(matchToAttr, node=x, exists=True):
            continue
        con = mc.listConnections(x+'.'+matchToAttr, source=True, destination=False)
        data['baseChain'].append(con[0])

    #get the ik control(s)
    #legacy support:
    if mc.attributeQuery(legacyIkAttr, node=element, exists=True):
        con = mc.listConnections(element+'.'+legacyIkAttr, source=True, destination=False)
        if con:
            data['ikControls'] = [con[0]]
            if mc.attributeQuery(matchToAttr, node=con[0], exists=True):
                con = mc.listConnections(con[0]+'.'+matchToAttr, source=True, destination=False)
                if con:
                    data['ikMatchTo'] = [con[0]]
    else:
        for i in range(mc.getAttr(element+'.'+ikAttr, size=True)):
            con = mc.listConnections('%s.%s[%s]' % (element,ikAttr,i), source=True, destination=False)

            data['ikControls'].append(con[0])

            if mc.attributeQuery(matchToAttr, node=con[0], exists=True):
                con = mc.listConnections(con[0]+'.'+matchToAttr, source=True, destination=False)
                if con:
                    data['ikMatchTo'].append(con[0])
                else:
                    data['ikMatchTo'].append(None)
            else:
                data['ikMatchTo'].append(None)

    if mc.attributeQuery(pvAttr, node=element, exists=True):
        con = mc.listConnections(element+'.'+pvAttr, source=True, destination=False)
        if con:
            data['pvControl'] = con[0]

    return data


def fkIkSwitch(nodes=None, switchTo=None, switchRange=False, bakeOnOnes=False):

    switchAttr = 'fkIkSwitch'

    start, end = utl.frameRange()

    if not nodes:
        nodes = mc.ls(sl=True)

    if not nodes:
        return

    elems = getElementsAbove(nodes)

    if not elems:
        return

    selection = []
    bakeToLocators = []

    elemDict = {}
    matchLocators = []
    aimLocators = []
    matchTo = []
    matchControls = []
    pvControls = []
    pvMatchTo = []
    garbage = []

    for elem in elems:

        data = fkIkData(elem)

        if not data:
            continue

        elemDict[elem] = {}
        #0 is fk
        #1 is ik
        fkIkState = mc.getAttr(elem+'.'+switchAttr)

        elemDict[elem]['switchTo'] = switchTo
        if switchTo == None or isinstance(switchTo, bool):
            if fkIkState < 0.5:
                elemDict[elem]['switchTo'] = 1
            else:
                elemDict[elem]['switchTo'] = 0

        if elemDict[elem]['switchTo'] == 1:
            #ik

            #key fk controls to preserve position
            if switchRange:
                mc.setKeyframe(data['fkChain'], animated=True, insert=True, time=(start,end))
            else:
                mc.setKeyframe(data['fkChain'], animated=True)

            for a, b in zip(data['ikControls'], data['ikMatchTo']):
                locator = mc.spaceLocator(name='TEMP#')[0]
                snap(locator, b)

                #flip the locator if the control's parent is scaled in -X
                if hasFlippedParent(a):
                    mc.setAttr(locator+'.rotateX', mc.getAttr(locator+'.rotateX') + 180)

                matchLocators.append(locator)

            matchTo.extend(data['ikMatchTo'])
            matchControls.extend(data['ikControls'])
            elemDict[elem]['ikControls'] = data['ikControls']

            if data['pvControl']:
                pvLocs = matchPoleVectorControl(data['baseChain'][0:3], data['pvControl'], doSnap=False)

                locator = mc.spaceLocator(name='TEMP#')[0]
                snap(locator, pvLocs)

                matchLocators.append(locator)
                matchTo.append(pvLocs[1])
                matchControls.append(data['pvControl'])

                garbage.extend(pvLocs)

                for x in data['ikControls']:
                    if mc.attributeQuery('poleTwist', exists=True, node=x):
                        utl.setAnimValue(x+'.poleTwist', 0)

            if switchRange:
                keytimes = mc.keyframe(data['fkChain'], time=(start,end), query=True, timeChange=True)
                if keytimes:
                    elemDict[elem]['keytimes'] = list(set(keytimes))
                else:
                    elemDict[elem]['keytimes'] = list(range(int(start), int(end)))
                elemDict[elem]['controls'] = data['ikControls']
                elemDict[elem]['controls'].append(data['pvControl'])

            selection.extend(data['ikControls'])

        else:
            #fk
            #key ik controls to preserve position
            controls = list(data['ikControls'])
            controls.append(data['pvControl'])
            if switchRange:
                mc.setKeyframe(controls, animated=True, insert=True, time=(start,end))
            else:
                mc.setKeyframe(controls, animated=True)

            for x in data['baseChain']:
                locator = mc.spaceLocator(name='TEMP#')[0]
                snap(locator, x)
                matchLocators.append(locator)

            matchTo.extend(data['baseChain'])
            matchControls.extend(data['fkChain'])

            if switchRange:
                keytimes = mc.keyframe(controls, time=(start,end), query=True, timeChange=True)
                if keytimes:
                    elemDict[elem]['keytimes'] = list(set(keytimes))
                else:
                    elemDict[elem]['keytimes'] = list(range(int(start),int(end)))
                elemDict[elem]['controls'] = data['fkChain']

            selection.append(data['fkChain'][0])

    if switchRange:
        utl.matchBake(matchTo, matchLocators, bakeOnOnes=True, maintainOffset=True, start=start, end=end)

        #if switching to ik, reset ik control attributes
        for elem in elems:
            if elemDict[elem]['switchTo'] == 1:
                for x in elemDict[elem]['ikControls']:
                    attrs = mc.listAttr(x, userDefined=True, keyable=True)
                    for attr in attrs:
                        if 'paceSwitch' in attr:
                            continue
                        if mc.getAttr(x+'.'+attr, lock=True):
                            continue
                        default = mc.attributeQuery(attr, listDefault=True, node=x)
                        if not default:
                            default = 0
                        elif isinstance(default, list):
                            default = default[0]
                        if mc.keyframe(x+'.'+attr, query=True, name=True):
                            mc.cutKey(x+'.'+attr, time=(start, end), includeUpperBound=False)
                            mc.setKeyframe(x+'.'+attr, time=(start,end), value=default)

                        else:
                            try:
                                utl.setAnimValue(x+'.'+attr, default)
                            except Exception:
                                pass
        utl.matchBake(matchLocators, matchControls, bakeOnOnes=True, start=start, end=end)
    else:
        #if switching to ik, reset ik control attributes
        for elem in elems:
            if elemDict[elem]['switchTo'] == 1:
                for x in elemDict[elem]['ikControls']:
                    attrs = mc.listAttr(x, userDefined=True, keyable=True)
                    for attr in attrs:
                        if 'paceSwitch' in attr:
                            continue
                        try:
                            default = mc.attributeQuery(attr, listDefault=True, node=x)[0]
                            mc.setAttr(x+'.'+attr, default)
                        except:
                            pass
        for a, b in zip(matchControls, matchLocators):
            snap(a,b)

    for elem in elems:
        switchPlug = elem+'.'+switchAttr

        #keytimes
        if switchRange:
            for f in range(int(start), int(end)):
                if not f in elemDict[elem]['keytimes']:
                    mc.cutKey(elemDict[elem]['controls'], time=(f,))

            if mc.keyframe(switchPlug, query=True, name=True):
                mc.cutKey(switchPlug, time=(start,end))
                mc.setKeyframe(switchPlug, value=elemDict[elem]['switchTo'], time=(start,end))
            else:
                mc.setAttr(switchPlug, elemDict[elem]['switchTo'])
        else:
            utl.setAnimValue(switchPlug, elemDict[elem]['switchTo'])
            #if keyed, set tangent type to stepped
            if mc.keyframe(switchPlug, query=True, name=True):
                #get previous key
                previousKeyTime = mc.findKeyframe(switchPlug, which='previous')
                mc.keyTangent(switchPlug, time=(previousKeyTime,), outTangentType='step')


    garbage.extend(matchLocators)

    mc.delete(garbage)
    mc.select(selection)


def matchPoleVectorControl(jointChain, pv=None, doSnap=True):
    '''
    Position a pole vector based on a 3-joint chain

    '''

    def distanceBetween(a,b):
        difference = [x-y for x,y in zip(a,b)]
        return math.sqrt(sum([x**2 for x in difference]))

    p1 = mc.xform(jointChain[0], query=True, rotatePivot=True, worldSpace=True)
    p2 = mc.xform(jointChain[1], query=True, rotatePivot=True, worldSpace=True)
    p3 = mc.xform(jointChain[2], query=True, rotatePivot=True, worldSpace=True)

    mag1 = distanceBetween(p2,p1)
    mag2 = distanceBetween(p3,p2)

    #these are all temporary nodes
    loc = mc.spaceLocator(name='TEMP#')[0]

    mc.pointConstraint(jointChain[0], loc, weight=mag2)
    mc.pointConstraint(jointChain[2], loc, weight=mag1)
    mc.aimConstraint(jointChain[1], loc, aimVector=(1,0,0), upVector=(0,1,0), worldUpType='object', worldUpObject=jointChain[0])

    pCenter = mc.xform(loc, query=True, rotatePivot=True, worldSpace=True)
    pPV = mc.xform(pv, query=True, rotatePivot=True, worldSpace=True)
    pvDist = distanceBetween(pPV,pCenter)

    loc2 = mc.spaceLocator(name='TEMP#')[0]
    loc2 = mc.parent(loc2, loc)[0]
    mc.setAttr(loc2+'.translate', (pvDist),0,0)

    if doSnap:
        snap(pv, loc2)
        mc.delete(loc)
    else:
        #for matching a range
        return loc, loc2


def switchSpace(nodes=None, toSpace=None, switchRange=False, bakeOnOnes=False):

    if not toSpace:
        return

    sel = mc.ls(sl=True)
    if not nodes:
        nodes = sel

    if switchRange:
        start, end = utl.frameRange()
    
    #check for dynamics
    for node in nodes:
        nucleus = utl.getNucleusHistory(node)
        if not nucleus:
            parent = mc.listRelatives(node, parent=True, pa=True)
            if parent:
                nucleus = utl.getNucleusHistory(parent[0])
        if nucleus:
            if mc.getAttr(nucleus+'.enable'):
                start = mc.getAttr(nucleus+'.startFrame')
                bakeOnOnes = True
            break
    #need to support this eventually for controls which have multiple space attributes.
    selChan = utl.getSelectedChannels()

    controls = []
    attributes = []
    locators = []
    values = []
    for node in nodes:

        ssData = getSpaceSwitchData(node)
        if not ssData:
            continue
        if selChan and selChan[0] in list(ssData.keys()):
            ssAttr = selChan[0]
        else:
            #silly, but take the shortest one, as that's usually default
            ssAttr = min(list(ssData.keys()), key=len)
        
        value = None
        if isinstance(toSpace, str):
            for i, e in enumerate(ssData[ssAttr]['enumValues']):
                if e.lower() == toSpace.lower():
                    value=i
                    break
        elif isinstance(value, (float, int)):
            value = toSpace
        else:
            print('Space value not valid:',toSpace)
            continue
        currentValue = mc.getAttr(node+'.'+ssAttr)

        if currentValue == value:
            print('{} space already set to {}, skipping'.format(node, toSpace))
            continue

        locator = mc.spaceLocator(name='TEMP#')[0]
        snap(locator, node)

        #need to test flipped before and after switch
        preFlipped = hasFlippedParent(node)

        mc.setAttr(node+'.'+ssAttr, value)
        postFlipped = hasFlippedParent(node)

        mc.setAttr(node+'.'+ssAttr, currentValue)

        #flip locator if we're going to or from a mirrored space
        if preFlipped != postFlipped:
            mc.setAttr(locator+'.rotateX', mc.getAttr(locator+'.rotateX') + 180)

        controls.append(node)
        attributes.append(ssAttr)
        locators.append(locator)
        values.append(value)

    if not values:
        return

    if switchRange:
        utl.matchBake(controls, locators, maintainOffset=True, bakeOnOnes=bakeOnOnes)

        for ctrl, attr, value in zip(controls, attributes, values):
            if mc.keyframe(ctrl+'.'+attr, query=True, name=True):
                mc.cutKey(ctrl+'.'+attr, time=(start,end))
                mc.setKeyframe(ctrl+'.'+attr, value=value, time=(start,end))
            else:
                mc.setAttr(ctrl+'.'+attr, value)

        utl.matchBake(locators, controls)

    else:
        for ctrl, attr, value, loc in zip(controls, attributes, values, locators):
            utl.setAnimValue(ctrl+'.'+attr, value)
            snap(ctrl, loc)

    mc.delete(locators)
    if sel:
        mc.select(sel)


def getDagMenuScript():
    result = mm.eval('whatIs createSelectMenuItems')
    filename = None
    if 'found in: ' in result:
        filename = result.split('found in: ')[-1]
        if os.path.isfile(filename):
            return filename
    mm.eval('source dagMenuProc.mel')
    result = mm.eval('whatIs dagMenuProc')
    if not 'found in: ' in result:
        return None
    filename = result.split('found in: ')[-1]
    return filename


def initPuppetContextMenu():

    #get the file name
    filename = getDagMenuScript()
    if not filename:
        raise RuntimeError('Unable to initialize Puppet Context Menu.')
    

    #globalize a proc which would otherwise fail
    mm.eval('''global proc optionalDagMenuProc( string $parent, string $item )
{
    string $object[] = `listRelatives -path -s $item`;
    string $shape = "";
    int $gotVisible = 0;
    if( size($object) < 1 ) return;
    for( $i=0; $i<size($object); $i+=1) {
        if( (0 == getAttr($object[$i] + ".io")) &&
            getAttr($object[$i] + ".v") ) {
            $shape = $object[$i];
            $gotVisible = 1;
            break;
        }
    }
    if( !$gotVisible ) {
        for( $i=0; $i<size($object); $i+=1) {
            if( 0 == getAttr($object[$i] + ".io")) {
                $shape = $object[$i];
                break;
            }
        }
    }
    if( "" != $shape ) {
        string $nt = `nodeType $shape`;
        switch( $nt ) {
          case "subdiv":
            subdOptionalDagMenuProc( $parent, $item );
            menuItem -d true;
            break;
          default:
            string $apiNt = `nodeType -api $shape`;
            if ( startsWith( $apiNt, "kPlugin" ) ) {
                string $nodeMenuCommand = $nt + "DagMenuProc";
                string $nodeMenuCommandWithArgs = $nodeMenuCommand + "(\\"" + $parent + "\\" , \\"" + $item + "\\" )";
                if ( exists( $nodeMenuCommand ) ) {
                   eval( $nodeMenuCommandWithArgs );
                }
            }
            break;
        }
    }
}
''')

    procRE = re.compile('(?<=global proc\s).+(?=\()')

    readLine = False
    patchedProc = []

    #open the file
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            if not readLine:
                if 'globalprocdagMenuProc(string$' in line.replace(' ',''):
                    readLine = True
                    patchedProc.append(line)
            else:
                if procRE.search(line):
                    #we've gotten to the next proc
                    break

                #remove any trailing comments
                if '//' in line:
                    line = line.split('//')[0]

                #search for when we want to add our custom stuff
                if 'createSelectMenuItems($parent' in line.replace(' ',''):
                    #add custom stuff before this function
                    patchedProc.append('python("import ml_puppet");')
                    patchedProc.append('if(`python ("ml_puppet.isNodePuppetControl(\'"+$object+"\')")`){')
                    patchedProc.append('    python ("ml_puppet.puppetContextMenu(\'"+$parent+"\',\'"+$object+"\')");')
                    patchedProc.append('    setParent -m $parent;')
                    patchedProc.append('    return;')
                    patchedProc.append('}')

                patchedProc.append(line.rstrip())

            line = f.readline()

    if not readLine:
        return

    mm.eval(''.join(patchedProc))


def isNodePuppetControl(node):
    if mc.attributeQuery(PUP_ID_PREFIX+'control', exists=True, node=node):
        return True
    if getNodeType(node) == 'control':
        return True
    return False


def getSpaceSwitchData(node):

    data = {}

    attrs = mc.listAttr(node, userDefined=True, keyable=True)

    if not attrs:
        return data

    ssAttrs = [x for x in attrs if 'paceSwitch' in x or x == 'space']
    for attr in ssAttrs:
        enumValues = []
        spaceEnum = 'space'
        if attr == 'spaceSwitch' or attr == 'space':
            if not 'space' in attrs:
                spaceEnum = 'spaceSwitch'
            enumValues = mc.attributeQuery(spaceEnum, node=node, listEnum=True)
        elif 'SpaceSwitch' in attr:
            baseName = attr.replace('SpaceSwitch','')
            if baseName + 'Space' in attrs:
                spaceEnum = baseName+'Space'
            else:
                spaceEnum = attr
            if spaceEnum in attrs and mc.attributeQuery(spaceEnum, node=node, attributeType=True) == 'enum':
                enumValues = mc.attributeQuery(spaceEnum, node=node, listEnum=True)
        if not enumValues:
            continue
        data[attr] = {}
        data[attr]['enumValues'] = enumValues[0].split(':')
        data[attr]['currentValue'] = mc.getAttr(node+'.'+spaceEnum, asString=True)

    return data


def puppetContextMenu(parent, node):

    nodes = mc.ls(sl=True)
    if not nodes:
        nodes = [node]

    appendage = None
    puppet = None
    for node in nodes:
        appendage = get_appendage(node)
        if appendage:
            break
    if appendage:
        puppets = getPuppets(appendage)
        if puppets:
            puppet = puppets[0]

    #create menu
    mc.setParent(parent, menu=True)

    #build the radial menu
    mc.menuItem(label='Select Top', radialPosition='N', command=partial(selectPuppets,nodes))
    mc.menuItem(label='All Controls', radialPosition='S', command=partial(selectControls,nodes))

    mc.menuItem(label='Keyed', radialPosition='SE', command=partial(selectKeyed, nodes))

    if appendage:
        mc.menuItem(label='Select Appendage', radialPosition='NE', command=partial(selectElements,nodes))
        mc.menuItem(label='Select Appendage Controls', radialPosition='E', command=partial(selectElementControls,nodes))

    #mirror controls west
    mc.menuItem(label='Flip Selection', radialPosition='W', command=partial(selectReplaceMirror, nodes))
    mc.menuItem(label='Mirror Selection', radialPosition='NW', command=partial(selectAddMirror, nodes))
    #main menu items

    if ml_resetChannels:
        append = ''
        if len(nodes) > 1:
            append = 's'
        mc.menuItem(label='Reset Control'+append, command=ml_resetChannels.resetPuppetControl)
        mc.menuItem(divider=True)

    ##selection
    #if appendage or puppet:

        #mc.menuItem(label='Selection', subMenu=True)

        ##select parent element

        ##select all worldspace controls
        #mc.menuItem(label='Select World Space Controls', command=partial(selectWorldSpaceControls, nodes))
        #mc.menuItem(label='Select Ik Controls', command=partial(selectIkControls, nodes))
        #mc.menuItem(label='Select Fk Controls', command=partial(selectFkControls, nodes))
        ##invert control selection
        #mc.menuItem(label='Invert Selection', command=partial(invertSelection, nodes))
        #mc.setParent('..', menu=True)

        #mc.menuItem(divider=True, dividerLabel='Visibility')

        #mc.menuItem(label='Control Visibility', subMenu=True)

        #mc.menuItem(label='Show All', command=partial(showAllControls, puppet))

        ##mc.menuItem(divider=True)
        ##for visAttr,shortName in zip(('geoVisibility','controlVisibility','secondaryControlVisibility'),('Geo','Controls','Secondary')):

            ##if mc.attributeQuery(visAttr, exists=True, node=element):
                ##if mc.getAttr(element+'.'+visAttr):
                    ##mc.menuItem(label='Hide '+shortName, command=partial(mc.setAttr, element+'.'+visAttr, 0))
                ##else:
                    ##mc.menuItem(label='Show '+shortName, command=partial(mc.setAttr, element+'.'+visAttr, 1))

        #mc.setParent('..', menu=True)

        #if puppet:
            #if mc.attributeQuery('visibilitySets', exists=True, node=puppet):
                #sets = mc.listConnections('{}.visibilitySets'.format(puppet), type='objectSet', source=False, destination=True)
                #if sets:
                    #mc.menuItem(label='Hide Sets', subMenu=True)
                    #for s in sets:
                        #mc.menuItem(label=s, command='import maya.cmds;maya.cmds.hide("{}")'.format(s))
                    #mc.setParent('..', menu=True)

                    #mc.menuItem(label='Show Sets', subMenu=True)
                    #mc.menuItem(label='Show All', command='import maya.cmds;maya.cmds.showHidden({})'.format(','.join(['"{}"'.format(x) for x in sets])))
                    #mc.menuItem(divider=True)
                    #for s in sets:
                        #mc.menuItem(label=s, command='import maya.cmds;maya.cmds.showHidden("{}")'.format(s))
                    #mc.setParent('..', menu=True)

        #mc.menuItem(divider=True)

    #mc.menuItem(label='Mirroring', subMenu=True)
    #mc.menuItem(label='Mirror Pose', command=partial(mirrorPose, nodes))
    #mc.menuItem(label='Flip Pose', command=partial(flipPose, nodes))
    #mc.menuItem(divider=True)
    #mc.menuItem(label='Mirror Animation', command=partial(mirrorAnimation, nodes))
    #mc.menuItem(label='Flip Animation', command=partial(flipAnimation, nodes))
    #mc.setParent('..', menu=True)
    
    #rotate order
    if ml_convertRotationOrder and mc.getAttr(node+'.rotateOrder', channelBox=True):
        mc.menuItem(divider=True)
        roo = mc.getAttr(node+'.rotateOrder')
        #rotOrders = ('xyz')
        mc.menuItem(label='Rotate Order', subMenu=True)
        mc.menuItem(label='Convert Rotate Order UI', command=partial(convertRotateOrderUI, nodes))    
    
    #== from here out, populate by code nodes ===============================
    codeNodes = []
    for a in [node, appendage]:
        connected = mc.listConnections(a+'.message', source=False)
        for b in connected:
            if mc.attributeQuery('puppeteer_data_code', node=b, exists=True):
                codeNodes.append(b)
    
    for codeNode in codeNodes:
        #eval menu command
        pass
    
    #== custom by node type ===============================
    #fkIkSwitching
    if appendage and mc.attributeQuery('fkIkSwitch', exists=True, node=element):
        mc.menuItem(divider=True, dividerLabel='FK/IK')
        state = mc.getAttr(element+'.fkIkSwitch')

        if state > 0:
            mc.menuItem(label='Toggle to FK', command=partial(fkIkSwitch, nodes))
        if state < 1:
            mc.menuItem(label='Toggle to IK', command=partial(fkIkSwitch, nodes))

        mc.menuItem(label='Bake To', subMenu=True)
        mc.menuItem(label='FK', command=partial(fkIkSwitch, nodes, 0, True))
        mc.menuItem(label='IK', command=partial(fkIkSwitch, nodes, 1, True))
        mc.setParent('..', menu=True)

    
    #space switching
    #attrs = mc.listAttr(node, userDefined=True, keyable=True)
    enumValues = mc.attributeQuery('space', node=node, listEnum=True)
    if enumValues:
        enumValues = enumValues[0].split(':')
        currentValue = mc.getAttr(node+'.space', asString=True)
        mc.menuItem(label='Switch Space', subMenu=True)
        for each in enumValues:
            if each == currentValue:
                continue
            mc.menuItem(label=each, command=partial(switchSpace, nodes, each))
        mc.setParent('..', menu=True)
        mc.menuItem(label='Bake Space', subMenu=True)
        for each in enumValues:
            if each == currentValue:
                continue
            mc.menuItem(label=each, command=partial(switchSpace, nodes, each, True))
        mc.setParent('..', menu=True)



def attributeMenuItem(node, attr):

    plug = node+'.'+attr
    niceName = mc.attributeName(plug, nice=True)

    #get attribute type
    attrType = mc.getAttr(plug, type=True)

    if attrType == 'enum':
        listEnum = mc.attributeQuery(attr, node=node, listEnum=True)[0]
        if not ':' in listEnum:
            return
        listEnum = listEnum.split(':')
        mc.menuItem(label=niceName, subMenu=True)
        for value, label in enumerate(listEnum):
            mc.menuItem(label=label, command=partial(mc.setAttr, plug, value))
        mc.setParent('..', menu=True)
    elif attrType == 'bool':
        value = mc.getAttr(plug)
        label = 'Toggle '+ niceName
        mc.menuItem(label=label, command=partial(mc.setAttr, plug, not value))


def convertRotateOrderUI(nodes, *args):
    '''
    wrapper
    '''
    if ml_convertRotationOrder:
        if nodes:
            mc.select(nodes[-1])
        ml_convertRotationOrder.ui()
        ml_convertRotationOrder.loadTips()


# __________________________________
# == POSE AND ANIM MIRRORING =======

def getMirrorName(node, a='Lf_', b='Rt_'):
    if a in node:
        return node.replace(a,b)
    elif b in node:
        return node.replace(b,a)
        


def getMirrorMap(nodes=None):
    '''
    Returns a map of all paired nodes within a puppet
    '''

    puppets = getPuppets(nodes)
    puppets = mc.ls(puppets, long=True)[0]

    allNodes = mc.ls('*.mirrorIndex', o=True, long=True, recursive=True)

    found = {}
    pairs = {}
    for node in allNodes:
        for puppet in puppets:
            if not node.startswith(puppet):
                continue
            value = mc.getAttr('{}.mirrorIndex'.format(node))

            if value in list(found.keys()):
                pairs[found[value]] = node
                pairs[node] = found[value]
                continue
            found[value] = node
    return pairs


def getMirrorPairs(nodes):
    '''
    Returns a dictionary of paired nodes.
    Keys are the input nodes, values are the mirrored nodes.
    '''

    nodes = mc.ls(nodes, long=True)
    #mirrorMap = getMirrorMap(nodes)
    mirrorPairs = {}
    #for each in nodes:
        #if each in mirrorMap:
            #mirrorPairs[each] = mirrorMap[each]
    for each in nodes:
        mirror = getMirrorName(each)
        if mc.objExists(mirror):
            mirrorPairs[each] = mirror
            
    return mirrorPairs


def getMirrorAxis(node):

    axis = []
    if mc.attributeQuery('mirrorAxis', exists=True, node=node):
        mirrorAxis = mc.getAttr('{}.mirrorAxis'.format(node))
        if mirrorAxis and not hasFlippedParent(node):
            axis = mirrorAxis.split(',')
    return axis


def selectReplaceMirror(nodes, *args):
    mc.select(list(getMirrorPairs(nodes).values()))


def selectAddMirror(nodes, *args):
    pairs = getMirrorPairs(nodes)
    mc.select(list(pairs.keys())+list(pairs.values()))


def copyPose(fromNode, toNode, flip=False):

    attrs = mc.listAttr(fromNode, keyable=True)
    if not attrs:
        return

    #if attributes are aliased, get the real names for mirroring axis
    aliases = mc.aliasAttr(fromNode, query=True)
    if aliases:
        for alias,real in zip(aliases[::2],aliases[1::2]):
            if alias in attrs:
                attrs.remove(alias)
                attrs.append(real)

    axis = getMirrorAxis(toNode)

    for attr in attrs:
        if attr == 'mirrorAxis':
            continue
        if not mc.attributeQuery(attr, node=toNode, exists=True):
            continue
        fromPlug = '{}.{}'.format(fromNode, attr)
        toPlug = '{}.{}'.format(toNode, attr)
        fromValue = mc.getAttr(fromPlug)
        toValue = mc.getAttr(toPlug)

        if attr in axis:
            fromValue *= -1.0
            toValue *= -1.0

        try:
            utl.setAnimValue(toPlug, fromValue)
        except:pass

        if flip:
            try:
                utl.setAnimValue(fromPlug, toValue)
            except:pass


def mirrorPose(nodes=None, *args):
    
    if not nodes:
        nodes = mc.ls(sl=True)
        
    if not nodes:
        raise RuntimeError('No nodes provided to mirror.')

    pairs = getMirrorPairs(nodes)
    done = []
    for node, mirror in list(pairs.items()):
        if node not in done:
            copyPose(node, mirror)
            done.append(mirror)


def flipPose(nodes=None, *args):
    
    if not nodes:
        nodes = mc.ls(sl=True)
        
    if not nodes:
        raise RuntimeError('No nodes provided to mirror.')

    nodes = mc.ls(nodes, long=True)

    flipPairs = getMirrorPairs(nodes)
    flipSingles = [x for x in nodes if x not in list(flipPairs.keys())]

    #do the singles:
    for node in flipSingles:
        for axis in getMirrorAxis(node):
            plug = '{}.{}'.format(node,axis)
            if mc.getAttr(plug, keyable=True):
                try:
                    utl.setAnimValue(plug, mc.getAttr(plug)*-1.0)
                except:pass
    #do the pairs
    done = []
    for node, mirror in list(flipPairs.items()):
        if node not in done:
            copyPose(node, mirror, flip=True)
            done.append(mirror)


def copyAnimation(fromNode, toNode):
    print('copy', fromNode.split('|')[-1], toNode.split('|')[-1])
    mc.copyKey(fromNode)
    mc.pasteKey(toNode, option='replaceCompletely')
    for axis in getMirrorAxis(toNode):
        mc.scaleKey(toNode, attribute=axis, valueScale=-1)


def swapAnimation(fromNode, toNode):

    if not mc.keyframe(fromNode, query=True, name=True):
        mc.cutKey(toNode, clear=True)
        return

    attrs = mc.listAttr(fromNode, keyable=True)
    if not attrs:
        return

    for attr in attrs:
        if not mc.attributeQuery(attr, node=toNode, exists=True):
            mc.cutKey(fromNode, attribute=attr, clear=True)
            continue

        fromPlug = '{}.{}'.format(fromNode, attr)
        toPlug = '{}.{}'.format(toNode, attr)

        srcCurve = mc.listConnections(fromPlug, source=True, destination=False, type='animCurve')
        dstCurve = mc.listConnections(toPlug, source=True, destination=False, type='animCurve')

        copySrc=None
        copyDst=None

        if srcCurve:
            copySrc = mc.duplicate(srcCurve[0])[0]

        if dstCurve:
            copyDst = mc.duplicate(dstCurve[0])[0]

        if copySrc:
            try:
                mc.cutKey(copySrc)
                mc.pasteKey(toNode, attribute=attr, option='replaceCompletely')
            except:pass
        if copyDst:
            try:
                mc.cutKey(copyDst)
                mc.pasteKey(fromNode, attribute=attr, option='replaceCompletely')
            except:pass

    for axis in getMirrorAxis(toNode):
        mc.scaleKey(toNode, attribute=axis, valueScale=-1)
        mc.scaleKey(fromNode, attribute=axis, valueScale=-1)


def mirrorAnimation(nodes=None, *args):
    
    if not nodes:
        nodes = mc.ls(sl=True)
        
    if not nodes:
        raise RuntimeError('No nodes provided to mirror.')
    
    pairs = getMirrorPairs(nodes)
    done = []
    for node, mirror in list(pairs.items()):
        if node not in done:
            copyAnimation(node, mirror)
            done.append(mirror)


def flipAnimation(nodes, *args):

    nodes = mc.ls(nodes, long=True)
    pairs = getMirrorPairs(nodes)
    flipSingles = [x for x in nodes if x not in list(pairs.keys())]

    #do the singles:
    for node in flipSingles:
        for axis in getMirrorAxis(node):
            plug = '{}.{}'.format(node,axis)
            mc.scaleKey(plug, attribute=axis, valueScale=-1)

    done = []
    for node, mirror in list(pairs.items()):
        if node not in done:
            swapAnimation(node, mirror)
            done.append(mirror)


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2013-03-10 : First publish, fkIk switching only.
#
# Revision 2: 2014-02-24 : Added selection scripts, UI, and updated for latest version of Puppeteer.
#
# Revision 3: 2014-03-01 : adding category
#
# Revision 4: 2015-04-27 : First major support for puppet marking menu.
#
# Revision 5: 2015-04-27 : temp node clean up bug fixed.
#
# Revision 6: 2015-05-14 : Space switch bake bug fixed.
#
# Revision 7: 2015-05-18 : Minor bugfixes.
#
# Revision 8: 2015-06-23 : puppet context menu fix for windows paths
#
# Revision 9: 2015-11-18 : Updated fk ik switching code for latest puppeteer
#
# Revision 10: 2016-09-25 : Minor KeyError bug fix.
#
# Revision 11: 2017-02-08 : zero out pole twist when matching to ik
#
# Revision 12: 2017-02-21 : fixing stepped tangents on ik switch attribute
#
# Revision 13: 2017-03-28 : mirroring and visibility sets
#
# Revision 14: 2017-03-28 : removing hide all sets, maya not allow
#
# Revision 15: 2017-04-06 : Context menu bug fixes and additional features.
#
# Revision 16: 2017-04-23 : Space Switch context menu bug fix
#
# Revision 17: 2017-04-25 : FK IK switching keying update
#
# Revision 18: 2017-05-24 : search higher for mirrored nodes when matching
#
# Revision 19: 2017-06-04 : adding puppet settings attributes
#
# Revision 20: 2017-06-13 : space switch matching bug fix
#
# Revision 21: 2017-06-29 : full context menu for puppet node
#
# Revision 22: 2017-06-30 : proper testing for puppet
#
# Revision 23: 2017-07-07 : space switch and mirroring bugs
#
# Revision 24: 2018-02-17 : Updating license to MIT.