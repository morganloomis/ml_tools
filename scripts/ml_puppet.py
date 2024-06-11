# -= ml_puppet.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 26
#   / / / / / / /  2023-04-22
#  /_/ /_/ /_/_/  _________
#               /_________/
# 
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copyright 2018-2023 Morgan Loomis
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
# select_controls, it will select all the controls for that puppet only. With
# nothing selected it will select all controls in the scene. For Fk/Ik switching,
# select any part of the appendage you want to switch. So for an arm, you can select
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

ml_match = None
try:
    import ml_match
except ImportError:
    pass

ml_snap = None
try:
    import ml_snap
except ImportError:
    pass

poseCapture = None
try:
    from leap import poseCapture
except ImportError:
    pass


PUP_ID_PREFIX = 'pupID_'
CONTROL_ATTR = PUP_ID_PREFIX+'control'
PUPPET_ATTR = PUP_ID_PREFIX+'puppet'
APPENDAGE_ATTR = 'puppeteer_appendage'
JOINT_WORLD_MATRIX_ATTR = 'skinCluster_worldMatrix'

def main():
    initPuppetContextMenu()
    filter_graphEditor()


# ====================================================================================
# TAGS
# ====================================================================================

def get_tagged_nodes_below(node, tag):
    nodes = []
    allKids = mc.listRelatives(node, ad=True, pa=True)
    for kid in allKids:
        if mc.attributeQuery(tag, exists=True, node=kid):
            nodes.append(kid)
    return nodes

def get_tagged_nodes_above(node, tag):
    nodes = []
    antecedents = mc.listRelatives(node, ad=True, pa=True, parent=True)
    for each in antecedents:
        if mc.attributeQuery(tag, exists=True, node=each):
            nodes.append(each)
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


def get_tagged_nodes(tag, namespaceFromNodes=None):

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
        allNodes.extend(mc.ls(ns+'*.'+tag, o=True))
    return allNodes

# ====================================================================================
# CONTROLS
# ====================================================================================


def is_control(node):
    return mc.attributeQuery(CONTROL_ATTR, exists=True, node=str(node))


def get_controls(nodes=None):
    return get_tagged_nodes(CONTROL_ATTR, namespaceFromNodes=nodes)


def get_controls_below(node):
    return get_tagged_nodes_below(node, CONTROL_ATTR)


# ====================================================================================
# PUPPET
# ====================================================================================

def is_puppet(node):
    return mc.attributeQuery(PUPPET_ATTR, exists=True, node=str(node))

def get_puppets(node=None):
    
    nodes = mc.ls(sl=True)
    if not nodes:
        if not node:
            return get_tagged_nodes(PUPPET_ATTR)
        nodes = [node]
    
    return get_tagged_nodes(PUPPET_ATTR, namespaceFromNodes=nodes)
    

def select_puppets(nodes=None, *args):

    pups = get_puppets(nodes)
    if pups:
        mc.select(pups)


def select_controls(nodes=None, *args):
    ctrls = get_controls(nodes=nodes)
    if ctrls:
        mc.select(ctrls)


def getWorldSpaceControls(nodes, *args):

    ctrls = get_controls(nodes=nodes)
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


def select_keyed(nodes, *args):
    if nodes:
        mc.select(nodes)
    keySel = utl.KeySelection()
    if keySel.keyedInHierarchy():
        mc.select(keySel.nodes, replace=True)
    else:
        mc.select(clear=True)


def selectIkControls(nodes, *args):
    ctrls = get_controls(nodes)
    if not ctrls:
        return
    mc.select( [x for x in ctrls if getTag(x, 'descriptor') == 'ik'])


def selectFkControls(nodes, *args):
    ctrls = get_controls(nodes)
    if not ctrls:
        return
    mc.select( [x for x in ctrls if getTag(x, 'descriptor') == 'fk'])


def invertSelection(nodes, *args):

    ctrls = get_controls(nodes)
    if not ctrls:
        return
    sel = mc.ls(sl=True)
    if not sel:
        mc.select(ctrls)
    else:
        mc.select([x for x in ctrls if x not in sel])


# ====================================================================================
# APPENDAGES
# ====================================================================================

def is_appendage(node):
    return mc.attributeQuery(APPENDAGE_ATTR, exists=True, node=str(node))


def get_appendage_controls(nodes=None):

    if not nodes:
        nodes = mc.ls(sl=True)
    appendages = get_appendages(nodes)
    if not appendages:
        return
    controls = []
    for appendage in appendages:
        controlsBelow = get_tagged_nodes_below(appendage, CONTROL_ATTR)
        if controlsBelow:
            controls.extend(controlsBelow)
    return controls

def select_appendage_controls(nodes=None, *args):
    ctrls = get_appendage_controls(nodes=nodes)
    if ctrls:
        mc.select(ctrls)

def get_appendage(node):
    if mc.attributeQuery(APPENDAGE_ATTR, node=node, exists=True):
        return node
    parent = mc.listRelatives(node, parent=True, pa=True)
    if parent:
        return get_appendage(parent[0])
    return None

def get_appendages(nodes):
    return list(set([get_appendage(x) for x in nodes]))

def select_appendage(nodes=None, *args):

    apps = get_appendages(nodes=nodes)
    if apps:
        mc.select(apps)


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

def defer_initPuppetContextMenu():
    #cmd = 'import ml_puppet;ml_puppet.initPuppetContextMenu()'
    mc.evalDeferred('initPuppetContextMenu()')

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

                    patchedProc.append('if(`python ("ml_puppet.is_control(\'"+$object+"\')")`){')
                    patchedProc.append('    python ("ml_puppet.puppetContextMenu(\'"+$parent+"\',\'"+$object+"\')");')
                    patchedProc.append('    setParent -m $parent;')
                    patchedProc.append('    return;')
                    patchedProc.append('}')

                patchedProc.append(line.rstrip())

            line = f.readline()

    if not readLine:
        return

    mm.eval(''.join(patchedProc))


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
        puppets = get_puppets(appendage)
        if puppets:
            puppet = puppets[0]

    #create menu
    mc.setParent(parent, menu=True)

    #build the radial menu
    mc.menuItem(label='Select Top', radialPosition='N', command=partial(select_puppets,nodes))
    mc.menuItem(label='All Controls', radialPosition='S', command=partial(select_controls,nodes))

    mc.menuItem(label='Keyed', radialPosition='SE', command=partial(select_keyed, nodes))

    if appendage:
        mc.menuItem(label='Select Appendage', radialPosition='NE', command=partial(select_appendage,nodes))
        mc.menuItem(label='Select Appendage Controls', radialPosition='E', command=partial(select_appendage_controls,nodes))

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


    #rotate order
    if ml_convertRotationOrder and mc.getAttr(node+'.rotateOrder', channelBox=True):
        roo = mc.getAttr(node+'.rotateOrder')
        #rotOrders = ('xyz')
        mc.menuItem(label='Convert Rotate Order...', command=partial(convertRotateOrderUI, nodes))    
        mc.menuItem(divider=True)

    if poseCapture and appendage and 'hand' in appendage:
        mc.menuItem(label='Ultraleap Pose Capture')    
        mc.menuItem(label='Ultraleap Animation Capture')    
        mc.menuItem(divider=True)
    
    #== from here out, populate by code nodes ===============================
    # codeNodes = []
    # for a in [node, appendage]:
    #     connected = mc.listConnections(a+'.message', source=False) or []
    #     for b in connected:
    #         if mc.attributeQuery('puppeteer_data_code', node=b, exists=True):
    #             codeNodes.append(b)
    
    # for codeNode in codeNodes:
    #     #eval menu command
    #     pass

    #== generic matching ===============================
    # includes fk/ik and space switching

    if not ml_match:
        return
    
    systems = ml_match.get_systems(nodes)
    if not systems:
        return
    
    driverAttrs = []
    #need to combine systems that have the same driver names and ranges into one menu item
    menu = {}
    for system in systems:
        driverNode, driverAttr = system.driver.split('.',1)

        if not mc.attributeQuery(driverAttr, node=driverNode, maxExists=True):
            print('Max value required for menu')
            continue
        
        min = mc.attributeQuery(driverAttr, node=driverNode, min=True)[0]
        max = mc.attributeQuery(driverAttr, node=driverNode, max=True)[0]
        valueList = mc.attributeQuery(driverAttr, node=driverNode, listEnum=True)

        if valueList:
            valueList = valueList[0].split(':')
        else:
            valueList = list(range(int(min), int(max+1)))

        #special case for fk/ik readability
        if len(valueList) == 2 and driverAttr in ['fk_ik', 'fkIk']:
            valueList = ['FK', 'IK']

        menuData = tuple([driverAttr]+valueList)
        if not menuData in menu:
            menu[menuData] = []
        menu[menuData].append(system)
    
    labels = [x[0] for x in menu.keys()]
    labelsUnique = len(labels) == len(set(labels))
    for menuData in menu.keys():
        #figure the label based on the number of unique things selected
        #two identical labels can have different value lists, so they need to prefixed.
        #prefix labels unless there's only 1 entry, or if all the labels are already unique
        label = menuData[0]
        systems = menu[menuData]

        if len(labels) > 1 and not labelsUnique:
            systemDrivers = [x.driver.split('.')[0] for x in systems]
            prefix = ', '.join(systemDrivers)
            if len(prefix) > 24:
                prefix = prefix[:20] + '. . .'
            label = prefix+label
        
        mc.menuItem(label=label, subMenu=True)
        system = systems[0]

        currentValue = None
        value = None
        values = [mc.getAttr(system.system+'.driver') for system in systems]
        allEqual = values.count(values[0]) == len(values)

        currentValue = mc.getAttr(system.system+'.driver')
        
        # -------------------------------------------
        mc.menuItem(label='Switch Current', subMenu=True)
        for i, each in enumerate(menuData[1:]):
            if allEqual and i == currentValue: #need to take into account min
                continue
            mc.menuItem(label=each, command=partial(do_match_current, system, i))
        mc.setParent('..', menu=True)

        # -------------------------------------------
        mc.menuItem(label='Switch Range', subMenu=True)
        for i, each in enumerate(valueList):
            mc.menuItem(label=each, command=partial(do_match_range, system, i))
        mc.setParent('..', menu=True)
    
        mc.setParent('..', menu=True)
    
def do_match_current(system, toValue, *args):
    system.match_current(toValue)

def do_match_range(system, toValue, *args):
    system.match_range(toValue)

def match_fk_range(*args):
    match_selected(0, range=True)

def match_ik_range(*args):
    match_selected(1, range=True)

def match_fk_current(*args):
    match_selected(0, range=False)

def match_ik_current(*args):
    match_selected(1, range=False)

def match_selected(toValue, range=False):
    sel = mc.ls(sl=True)
    if not sel:
        return
    systems = ml_match.get_systems(sel)
    for system in systems:
        if range:
            system.match_range(toValue)
        else:
            system.match_current(toValue)


def convertRotateOrderUI(nodes, *args):
    '''
    wrapper
    '''
    if ml_convertRotationOrder:
        if nodes:
            mc.select(nodes[-1])
        ml_convertRotationOrder.ui()
        ml_convertRotationOrder.loadTips()


def fk_ik_ui():
    '''
    User interface for arc tracer
    '''

    with utl.MlUi('matching', 'Matching', width=400, height=180, info='''Select systems to match.
Any control affected by the fk/ik system will do.''') as win:
    
        win.buttonWithPopup(label='Match Current FK', command=match_fk_current, annotation='Match to FK over range.',
                            shelfLabel='fk', shelfIcon='ikEffector')
        win.buttonWithPopup(label='Match Current IK', command=match_ik_current, annotation='Match to FK over range.',
                            shelfLabel='ik', shelfIcon='ikEffector')
        win.buttonWithPopup(label='Match Range FK', command=match_fk_range, annotation='Match to FK over range.',
                            shelfLabel='fk', shelfIcon='ikEffector')
        win.buttonWithPopup(label='Match Range IK', command=match_ik_range, annotation='Match to FK over range.',
                            shelfLabel='ik', shelfIcon='ikEffector')


#=================

def space_switch(nodes=None, toSpace=None, switchRange=False, bakeOnOnes=False):

    sel = mc.ls(sl=True)

    if switchRange:
        start, end = utl.frameRange()
    
    controls = []
    attributes = []
    locators = []
    values = []
    for node in nodes:
        ml_snap.setAttr_preserveTransform(node+'.space', toSpace)

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

# __________________________________
# == POSE AND ANIM MIRRORING =======

def getMirrorName(node, a='Lf_', b='Rt_'):
    if a in node:
        return node.replace(a,b)
    elif b in node:
        return node.replace(b,a)
    return None
        

def getMirrorMap(nodes=None):
    '''
    Returns a map of all paired nodes within a puppet
    '''

    puppets = get_puppets(nodes)
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
        if mirror and mc.objExists(mirror):
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
    pairs = getMirrorPairs(nodes)
    if not pairs:
        return
    mc.select(list(pairs.values()))


def selectAddMirror(nodes, *args):
    pairs = getMirrorPairs(nodes)
    if not pairs:
        return
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


def hasFlippedParent(node, testRange=3):

    parent = mc.listRelatives(node, parent=True, pa=True)
    for null in range(testRange):
        if not parent:
            return False
        if mc.getAttr(parent[0]+'.scaleX') < 0:
            return True
        parent = mc.listRelatives(parent[0], parent=True, pa=True)
    return False


def export_animation(namespace=None, fbxFile=None):
    '''
    Export the puppet with the given namespace, to the given filepath.
    Namespace is required.
    '''
    
    if not namespace:
        sel = mc.ls(sl=True)
        if not len(sel) == 1:
            raise RuntimeError('select 1 puppet')
        
        ns = utl.getNamespace(sel[0])
        namespace = ns.strip(':')
        if not namespace:
            raise RuntimeError('puppet must have a namespace')

    if fbxFile:
        if not os.path.isdir(os.path.dirname(fbxFile)):
            raise RuntimeError('Directory does not exist: {}'.format(fbxFile))
    else:
        filename = mc.fileDialog2(caption='Export Animation', 
                                fileFilter='Animation Files (*.fbx)', 
                                fileMode=0,
                                dialogStyle=1)
        fbxFile = filename[0]
        if not fbxFile.endswith('.fbx'):
            fbxFile+='.fbx'
    
    
    fbxFile = os.path.normpath(fbxFile).replace('\\', '/')
    
    skel = Skeleton(namespace=namespace)
    skel.init_skeletonNodes()
    skel.create_skeleton()
    skel.connect_skeleton()
    
    mc.select(skel.roots)
    try:
        FBX_export(fbxFile, 
                #animationOnly=True,
                inputConnections=False,
                bakeComplexAnimation=True)
    except Exception as err:
        raise err
    finally:
        mc.delete(skel.roots)
    
    
def FBX_export(filename, selection=True, **kwargs):
    '''
    FBX command wrapper.
    '''
    
    #if not 'fileVersion' in kwargs:
        #kwargs['fileVersion'] = 'FBX202000'
    if not 'generateLog' in kwargs:
        kwargs['generateLog'] = False
    
    for k,v in kwargs.items():
        if isinstance(v, bool):
            v = str(v).lower()
        elif isinstance(v, str):
            v = '"'+v+'"'
        cmd = 'FBXExport{}{} -v {}'.format(k[0].upper(), k[1:], v)
        mm.eval(cmd)
    
    cmd = 'FBXExport -f "{}"'.format(filename)
    if selection:
        cmd+=' -s'
    print(cmd)
    mm.eval(cmd)   
    
    
def get_skeleton_nodes(namespace=None):
    '''Return all skeleton nodes found within a given namespace.'''
    ns = ''
    if namespace:
        ns = '{}:'.format(namespace)
    return mc.ls(ns+'*.puppeteerDataSkeleton', o=True)


class Skeleton(object):
    '''
    Skeleton object represents the skeleton data for a character.
    It mostly just handles the SkeletonEntry objects, which do most of the heavy lifting.
    '''
    
    def __init__(self, namespace=None):
        #entries is a dictionary of skeletonEntries with key being name
        self._entries = {}
        self.roots = []
        self.namespace = namespace
        
    def init_skeletonNodes(self):
        for skelNode in get_skeleton_nodes(namespace=self.namespace):
            i=0
            while True:
                if not mc.listConnections('{}.jointChain[{}]'.format(skelNode, i), source=True, destination=False):
                    break
                entry = SkeletonEntry(skelNode, i)
                self._entries[entry.name] = entry
                i+=1

    def create_skeleton(self):
        '''
        create a joint hierarchy from initialized skeleton entries
        '''
        
        for entry in self._entries.values():
            entry.create_joint()
        
        for entry in self._entries.values():
            if not entry.parent:
                self.roots.append(entry.name)
                continue
            entry.joint = mc.parent(entry.joint, entry.parent.name)[0]
            
        #create a joint proxy of the blendshape node
        if self.namespace:
            blendshapes = mc.ls(self.namespace+':*', type='blendShape') or []
        else:
            blendshapes = mc.ls(type='blendShape') or []
        for bs in blendshapes:
            aliasList = mc.aliasAttr(bs, query=True)
            mc.select(clear=True)
            joint = mc.joint(name=bs.split(':')[-1])
            joint = mc.parent(joint, self.roots[0])[0]
            
            for n in range(0,len(aliasList),2):
                attr = aliasList[n]
                mc.addAttr(joint, ln=attr, keyable=True)
                mc.connectAttr(bs+'.'+attr, joint+'.'+attr)
    
    
    def connect_skeleton(self):
        '''
        Connect joints to skeleton nodes in the scene
        '''
        for entry in self._entries.values():
            entry.connect_joint()


    def connect_skin(self):
        for entry in list(self._entries.values()):
            entry.connect_skin()
        mc.dgdirty(a=True)
    
    
class SkeletonEntry(object):
    '''
    Data point representing a joint in a skeleton hierarchy, before and after it is created.
    '''
    
    def __init__(self, skeletonNode, index):
        self._name = None
        self._parent = False
        self._children = []
        self._localMatrix = None
        self.skeletonNode = skeletonNode
        self.index = index
        self.joint = None
    
    @property
    def plug(self):
        return '{}.jointChain[{}]'.format(self.skeletonNode, self.index)
        
    @property
    def name(self):
        '''
        Joint name is derived from the node providing the world matrix for the joint, minus suffix.
        '''
        if not self._name:
            source = mc.listConnections('{}.jointChain[{}]'.format(self.skeletonNode, self.index), source=True, destination=False)
            if not source:
                raise RuntimeError('{}.jointChain[{}] has no connection.'.format(self.skeletonNode, self.index))
            name = source[0].rsplit('_',1)[0].rsplit(':',1)[-1]
            self._name = name.replace('__','_')         
        return self._name
    
    @property
    def parent(self):
        '''
        walk up the parent connection until we find another skeleton node
        '''
        if self._parent is False:
            if mc.getAttr('{}.hierarchical'.format(self.skeletonNode)) and self.index != 0:
                self.set_parent(SkeletonEntry(self.skeletonNode, self.index-1))
            #trace the parent
            else:
                self._parent = None
                trace = mc.listConnections('{}.parent'.format(self.skeletonNode), source=True, destination=False, plugs=True)
                while trace:
                    if mc.attributeQuery('puppeteerDataSkeleton', node=trace[0], exists=True):
                        node = trace[0].split('.')[0]
                        index = int(trace[0].split('[')[-1].strip(']'))
                        #found the parent skeleton data node, get the joint it's pointing to
                        self.set_parent(SkeletonEntry(node, index))
                        break
                    trace = mc.listConnections(trace[0], source=True, destination=False, plugs=True)
        return self._parent
    
    def set_parent(self, parent):
        ''''''
        if not isinstance(parent, SkeletonEntry):
            raise RuntimeError('Parent should be SkeletonEntry type.')
        parent.append_child(self)
        self._parent = parent
        
    def append_child(self, child):
        if not child in self._children:
            self._children.append(child)
        
    def create_joint(self):
        mc.select(clear=True)
        self.joint = mc.createNode('joint', name=self.name)
        mc.setAttr('{}.segmentScaleCompensate'.format(self.joint), 0)
    
    @property
    def localMatrix(self):
        if not self.joint:
            self._localMatrix = None
            return None
        if not self._localMatrix:
            #look for it first
            a = mc.listConnections('{}.translate'.format(self.joint), d=False, type='decomposeMatrix')
            if a:
                b = mc.listConnections('{}.inputMatrix'.format(a[0]), type='multMatrix', d=False)
                if b:
                    j = mc.listConnections('{}.matrixIn[0]'.format(b[0]), type='joint', d=False)
                    if j and j == self.joint:
                        self._localMatrix = b

        if not self._localMatrix:

            mc.addAttr(self.joint, ln=JOINT_WORLD_MATRIX_ATTR, dt='matrix', keyable=True)
            mc.connectAttr(self.plug, '{}.{}'.format(self.joint, JOINT_WORLD_MATRIX_ATTR))

            self._localMatrix = mc.createNode('multMatrix', name='{}_localMatrix'.format(self.name))
            mc.connectAttr('{}.jointChain[{}]'.format(self.skeletonNode, self.index), '{}.matrixIn[0]'.format(self._localMatrix))
            mc.connectAttr('{}.parentInverseMatrix[0]'.format(self.joint), '{}.matrixIn[1]'.format(self._localMatrix))
            
        return self._localMatrix
    
    def connect_joint(self):
        if not self.joint:
            raise RuntimeError('joint not created yet.')
        
        self.decompose = mc.createNode('decomposeMatrix', name='{}_decompose'.format(self.name))

        mc.connectAttr('{}.matrixSum'.format(self.localMatrix), '{}.inputMatrix'.format(self.decompose))
        
        mc.connectAttr('{}.outputTranslate'.format(self.decompose), '{}.translate'.format(self.joint))
        mc.connectAttr('{}.outputRotate'.format(self.decompose), '{}.rotate'.format(self.joint))
        mc.connectAttr('{}.outputScale'.format(self.decompose), '{}.scale'.format(self.joint))


    def connect_skin(self):
        #connect to skincluster
        for skinCon in mc.listConnections(self.plug, source=False, destination=True, type='skinCluster', plugs=True) or []:
            mc.connectAttr(self.joint+'.worldMatrix[0]', skinCon, force=True)
            

def add_skeleton(includeBlendshapes=False):
    
    skel = Skeleton()
    skel.init_skeletonNodes()
    joints = skel.create_skeleton()
    skel.connect_skeleton()
    skel.connect_skin()


def remove_skeleton():
    '''
    '''
    specialJoints = mc.ls('*.'+JOINT_WORLD_MATRIX_ATTR, o=True, type='joint')
    count = 0
    for joint in specialJoints:
        matrix = mc.listConnections('{}.{}'.format(joint, JOINT_WORLD_MATRIX_ATTR), source=True, destination=False, plugs=True)
        outputs = mc.listConnections('{}.worldMatrix[0]'.format(joint), source=False, destination=True, plugs=True) or []
        
        for each in outputs:
            if mc.nodeType(each.split('.')[0]) != 'skinCluster':
                continue
            mc.connectAttr(matrix[0], each, force=True)
            count+=1
    
    #selectively delete special joints that only have special joint children
    for joint in specialJoints:
        try:
            mc.delete(joint)
        except:
            pass
    mc.dgdirty(a=True)
        
    return count

def filter_graphEditor():
    if not mc.outlinerEditor('graphEditor1OutlineEd', q=True, exists=True):
        mm.eval('GraphEditor;')
    filter = mc.itemFilter(byName='*.offsetParentMatrix', negate=True)
    mc.outlinerEditor('graphEditor1OutlineEd', e=True, attrFilter=filter, ignoreHiddenAttribute=True)
    mm.eval('AEdagNodeCommonRefreshOutliners();')

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