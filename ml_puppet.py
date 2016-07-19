# 
#   -= ml_puppet.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 9, 2015-11-18
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_puppet.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_puppet
#     ml_puppet.main()
# From MEL, this looks like:
#     python("import ml_puppet;ml_puppet.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Support tools for puppets created by http://morganloomis.com/puppeteer
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Launch the UI to see the options available. Press a button to make a
# selection or run a command. Right click buttons to create a hotkey for that option.
# All options are selection-sensitive, so for example if you have two 
# puppets referenced into a scene, and select any part of one of them and
# run selectControls, it will select all the controls for that puppet only.
# With nothing selected it will select all controls in the scene.
# For Fk/Ik switching, select any part of the element you want to switch.
# So for an arm, you can select the ik hand control, the fk shoulder, 
# the pole vector, and either way it will know to do the switch for that arm.
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
__revision__ = 9

import maya.cmds as mc
import maya.mel as mm
from functools import partial
import math, re

try:
    import ml_utilities as utl
    utl.upToDateCheck(15)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
ml_convertRotationOrder = None
try:
    import ml_convertRotationOrder
except:
    pass

ml_worldBake = None
try:
    import ml_worldBake
except:
    pass

ml_resetChannels = None
try:
    import ml_resetChannels
except:
    pass


PUP_ID_PREFIX = 'pupID_'

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
    
    
def fkIkSwitchSel(*args):
    fkIkSwitch()


def fkIkSwitchRangeSel(*args):
    fkIkSwitchRange()
    
    
def getPuppets(nodes=None):
    
    if nodes:
        return getNodeTypeAbove(nodes,'puppet')
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
    wsCtrls = list()
    for ctrl in ctrls:
        if getTag(ctrl, 'baseName') == 'root':
            wsCtrls.append(ctrl)
            continue
        
        ssData = getSpaceSwitchData(ctrl)
        if not ssData:
            continue
        
        for attr, value in ssData.items():
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
    controls = list()
    for element in elements:
        controlsBelow = getNodesOfTypeBelow(element, 'control')
        if controlsBelow:
            controls.extend(controlsBelow)
    return controls


def selectElementControls(nodes=None, *args):
    ctrls = getElementControls(nodes=nodes)
    if ctrls:
        mc.select(ctrls)
        
    
def getElementsAbove(nodes=None):
    
    elements = list()
    if not nodes:
        nodes = mc.ls(sl=True)
    for each in nodes:
        if getNodeType(each) == 'element':
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
    nodes = list()
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
    return getTag(node, 'nodeType')

    
def getNodesOfType(nodeType, namespaceFromNodes=None):
    
    allNodes = list()
    
    #if something is selected, get it from within that namespace.    
    if not namespaceFromNodes:
        namespaceFromNodes = mc.ls(sl=True)
    namespaces = list()    
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
        else:
            pass
            #allNodes = getAllPupNodes()
            #if not allNodes:
            #    return
            #allTypeNodes = list()
            #for each in allNodes:
            #    if mc.getAttr(each+'.'+PUP_ID_PREFIX+'nodeType') == nodeType:
            #        allTypeNodes.append(each)
            #return allTypeNodes
    return allNodes        


def snap(node, snapTo):
    
    #duplicate the node we want snap
    dup = mc.duplicate(node, parentOnly=True)[0]
    #unlock translates and rotates
    for a in ('.t','.r'):
        for b in ('x','y','z'):
            mc.setAttr(dup+a+b, lock=False)
    
    mc.parentConstraint(snapTo, dup)
    
    for a in ('.t','.r'):
        for b in ('x','y','z'):
            try:
                mc.setAttr(node+a+b, mc.getAttr(dup+a+b))
            except StandardError:
                pass

    mc.delete(dup)
        
        
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
    
    data = dict()
    
    #if this is an fk/ik switchable attribute
    if not mc.attributeQuery(switchAttr, node=element, exists=True):
        return
    if not mc.attributeQuery(fkAttr, node=element, exists=True):
        return
    if not mc.attributeQuery(ikAttr, node=element, exists=True) and not mc.attributeQuery(legacyIkAttr, node=element, exists=True):
        return
    
    #these are the nodes we need to find
    data['fkChain'] = list()
    data['ikControls'] = list()
    data['pvControl'] = None
    
    data['baseChain'] = list()
    data['ikMatchTo'] = list()
    
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

    selection = list()
    bakeToLocators = list()
    
    elemDict = dict()
    matchLocators = list()
    aimLocators = list()
    matchTo = list()
    matchControls = list()
    pvControls = list()
    pvMatchTo = list()
    garbage = list()

    for elem in elems:

        data = fkIkData(elem)

        if not data:
            #(data['fkChain'] and data['ikControl'] and data['pvControl'] and data['baseChain'] and data['ikMatchTo']):
            continue
        
        elemDict[elem] = dict()
    
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
            for x in data['ikControls']:
                matchLocators.append(mc.spaceLocator(name='TEMP#')[0]) 
            matchTo.extend(data['ikMatchTo'])
            matchControls.extend(data['ikControls'])
            
            if data['pvControl']:
                pvLocs = matchPoleVectorControl(data['baseChain'][0:3], data['pvControl'], doSnap=False)
                matchLocators.append(mc.spaceLocator(name='TEMP#')[0])
                matchTo.append(pvLocs[1])
                matchControls.append(data['pvControl'])
            
                garbage.extend(pvLocs)
            
            if switchRange:
                keytimes = mc.keyframe(data['fkChain'], time=(start,end), query=True, timeChange=True)
                if keytimes:
                    elemDict[elem]['keytimes'] = list(set(keytimes))
                else:
                    elemDict[elem]['keytimes'] = range(int(start), int(end))
                #elemDict[elem]['controls'] = [data['ikControl'],data['pvControl']]
                elemDict[elem]['controls'] = data['ikControls']
                elemDict[elem]['controls'].append(data['pvControl'])
                
                
            selection.extend(data['ikControls'])
            
        else:
            #fk
            for x in data['baseChain']:
                matchLocators.append(mc.spaceLocator(name='TEMP#')[0])
            matchTo.extend(data['baseChain'])
            matchControls.extend(data['fkChain'])
            
            if switchRange:
                keytimes = mc.keyframe([data['ikControl'],data['pvControl']], time=(start,end), query=True, timeChange=True)
                if keytimes:
                    elemDict[elem]['keytimes'] = list(set(keytimes))
                else:
                    elemDict[elem]['keytimes'] = range(int(start),int(end))
                elemDict[elem]['controls'] = data['fkChain']
                
            selection.append(data['fkChain'][0])
    
    #For Debugging
    #for a, b in zip(matchControls, matchTo):
    #    print a,'\t->\t',b
        
    if switchRange:
        utl.matchBake(matchTo, matchLocators, bakeOnOnes=True)
        utl.matchBake(matchLocators, matchControls, bakeOnOnes=True)
    else:
        for a, b in zip(matchLocators, matchTo):
            mc.delete(mc.parentConstraint(b,a))
        for a, b in zip(matchControls, matchLocators):
            snap(a,b)
    
    for elem in elems:
        #keytimes
        
        if switchRange:
            for f in range(int(start), int(end)):
                if not f in elemDict[elem]['keytimes']:
                    mc.cutKey(elemDict[elem]['controls'], time=(f,))            
            
            if mc.keyframe(elem+'.'+switchAttr, query=True, name=True):
                mc.cutKey(elem+'.'+switchAttr, time=(start,end))
                mc.setKeyframe(elem+'.'+switchAttr, value=elemDict[elem]['switchTo'], time=(start,end))
            else:
                mc.setAttr(elem+'.'+switchAttr, elemDict[elem]['switchTo'])
        else:
            utl.setAnimValue(elem+'.'+switchAttr, elemDict[elem]['switchTo'])

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
    
    #
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
    
    sel = None
    if not nodes:
        nodes = mc.ls(sl=True)
        sel = nodes
        
    if switchRange:
        start, end = utl.frameRange()
    
    #need to support this eventually for controls which have multiple space attributes.
    selChan = utl.getSelectedChannels()
    
    controls = list()
    attributes = list()
    locators = list()
    values = list()
    for node in nodes:
        ssData = getSpaceSwitchData(node)
        if not ssData:
            continue
        if selChan and selChan[0] in ssData.keys():
            ssAttr = selChan[0]
        else:
            #silly, but take the shortest one, as that's usually default
            ssAttr = min(ssData.keys(), key=len)
        
        if isinstance(toSpace, basestring):
            for i, e in enumerate(ssData[ssAttr]['enumValues']):
                if e.lower() == toSpace.lower():
                    value=i
                    break
        elif isinstance(value, (float, int)):
            value = toSpace
        else:
            print 'Space value not valid:',toSpace
            continue
        
        controls.append(node)
        attributes.append(ssAttr)
        locators.append(mc.spaceLocator(name='TEMP#')[0])
        values.append(value)
    
    if not values:
        return
    
    if switchRange:
        utl.matchBake(controls, locators)
        
        for ctrl, attr, value in zip(controls, attributes, values):
            if mc.keyframe(ctrl+'.'+attr, query=True, name=True):
                mc.cutKey(ctrl+'.'+attr, time=(start,end))
                mc.setKeyframe(ctrl+'.'+attr, value=value, time=(start,end))
            else:
                mc.setAttr(ctrl+'.'+attr, value)
        
        utl.matchBake(locators, controls)
    
    else:
        for ctrl, attr, value, loc in zip(controls, attributes, values, locators):
            mc.delete(mc.parentConstraint(ctrl, loc))
            utl.setAnimValue(ctrl+'.'+attr, value)
            snap(ctrl, loc)
            
    mc.delete(locators)
    if sel:
        mc.select(sel)


def initPuppetContextMenu():

    result = mm.eval('whatIs createSelectMenuItems')
    
    #may need sourcing if it isn't found
    if result == 'Unknown':
        mm.eval('source dagMenuProc.mel')
        #try again
        result = mm.eval('whatIs dagMenuProc')
    
    #now check again if its from a file, if not we've already done this.
    if not 'found in: ' in result:
        #if this function was added interactively already, don't do anything
        return
    
    #get the file name
    filename = result.split('found in: ')[-1]    
    
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
    patchedProc = list()
    
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
    
    if mc.attributeQuery(PUP_ID_PREFIX+'nodeType', exists=True, node=node):
        return True
    if getNodeType(node) == 'control':
        return True
    return False


def getSpaceSwitchData(node):
    
    data = dict()
    
    attrs = mc.listAttr(node, userDefined=True, keyable=True)
    
    if not attrs:
        return data
    
    ssAttrs = [x for x in attrs if 'paceSwitch' in x]
    for attr in ssAttrs:
        enumValues = list()
        spaceEnum = 'space'
        if attr == 'spaceSwitch' and 'space' in attrs:
            enumValues = mc.attributeQuery(spaceEnum, node=node, listEnum=True)
        elif 'SpaceSwitch' in attr:
            baseName = attr.replace('SpaceSwitch','')
            if mc.attributeQuery(baseName+'Space', node=node, exists=True):
                spaceEnum = baseName+'Space'
            elif not 'spaceSwitch' in ssAttrs and 'space' in attrs:
                spaceEnum = 'space'
            if spaceEnum:
                enumValues = mc.attributeQuery(spaceEnum, node=node, listEnum=True)
        if not enumValues:
            continue
        data[attr] = dict()
        data[attr]['enumValues'] = enumValues[0].split(':')
        data[attr]['currentValue'] = mc.getAttr(node+'.'+spaceEnum, asString=True)
        
    return data


def puppetContextMenu(parent, node):
    
    nodes = mc.ls(sl=True)
    if not nodes:
        nodes = [node]
    
    element = None
    elements = getElementsAbove(nodes)
    if elements:
        element = elements[0]
        
    
    #create menu
    mc.setParent(parent, menu=True)
    
    #build the radial menu
    #east, element selection controls
    mc.menuItem(label='Select Top', radialPosition='N', command=partial(selectPuppets,nodes))
    mc.menuItem(label='All Controls', radialPosition='S', command=partial(selectControls,nodes))
    #mc.menuItem(label='SE', radialPosition='SE')
    
    mc.menuItem(label='Keyed', radialPosition='SE', command=partial(selectKeyed, nodes))
    
    if element:
        mc.menuItem(label='Select Element', radialPosition='NE', command=partial(selectElements,nodes))
        mc.menuItem(label='Select Elem Controls', radialPosition='E', command=partial(selectElementControls,nodes))
        
        #west: visibility controls
        for visAttr,shortName,cardinal in zip(('geoVisibility','controlVisibility','secondaryControlVisibility'),('Geo','Controls','Secondary'),('NW','W','SW')):
        
            if mc.attributeQuery(visAttr, exists=True, node=element):
                if mc.getAttr(element+'.'+visAttr):
                    mc.menuItem(label='Hide '+shortName, 
                                radialPosition=cardinal, 
                                command=partial(mc.setAttr, element+'.'+visAttr, 0))
                else:
                    mc.menuItem(label='Show '+shortName, 
                                radialPosition=cardinal, 
                                command=partial(mc.setAttr, element+'.'+visAttr, 1))
    
    #main menu items
    
    #optional, check for gui. 
    #mc.menuItem(label='Launch GUI (if it exists)')
    
    if ml_resetChannels:
        append = ''
        if len(nodes) > 1:
            append = 's'
        mc.menuItem(label='Reset Control'+append, command=ml_resetChannels.resetPuppetControl)
        mc.menuItem(divider=True)
    
    #selection
    if element:
        mc.menuItem(label='Selection', subMenu=True)
        
        #select parent element
        
        #select all worldspace controls
        mc.menuItem(label='Select World Space Controls', command=partial(selectWorldSpaceControls, nodes))
        mc.menuItem(label='Select Ik Controls', command=partial(selectIkControls, nodes))
        mc.menuItem(label='Select Fk Controls', command=partial(selectFkControls, nodes))
        #invert control selection
        mc.menuItem(label='Invert Selection', command=partial(invertSelection, nodes))
        #select all keyed
        
        mc.setParent('..', menu=True)
        mc.menuItem(divider=True)
    
    #== custom by node type ===============================
    #fkIkSwitching
    if element:
        if mc.attributeQuery('fkIkSwitch', exists=True, node=element):
            state = mc.getAttr(element+'.fkIkSwitch')
            
            if state > 0:
                mc.menuItem(label='Toggle to FK', command=partial(fkIkSwitch, nodes))
            if state < 1:
                mc.menuItem(label='Toggle to IK', command=partial(fkIkSwitch, nodes))
                
            mc.menuItem(label='Bake To', subMenu=True)
            mc.menuItem(label='FK', command=partial(fkIkSwitch, nodes, 0, True))
            mc.menuItem(label='IK', command=partial(fkIkSwitch, nodes, 1, True))
            mc.setParent('..', menu=True)
            mc.menuItem(divider=True)
    
    
    #space switching
    #attrs = mc.listAttr(node, userDefined=True, keyable=True)
    ssData = getSpaceSwitchData(node)
    if ssData:
        for key, value in ssData.items():
            mc.menuItem(label='Switch '+key, subMenu=True)
            for each in value['enumValues']:
                if each == value['currentValue']:
                    continue
                mc.menuItem(label=each, command=partial(switchSpace, nodes, each))
            mc.setParent('..', menu=True)
            mc.menuItem(label='Bake '+key, subMenu=True)
            for each in value['enumValues']:
                if each == value['currentValue']:
                    continue
                mc.menuItem(label=each, command=partial(switchSpace, nodes, each, True))
            mc.setParent('..', menu=True)
            mc.menuItem(divider=True)
            
    #rotate order
    if ml_convertRotationOrder:
        if mc.getAttr(node+'.rotateOrder', channelBox=True):
            roo = mc.getAttr(node+'.rotateOrder')
            #rotOrders = ('xyz')
            mc.menuItem(label='Rotate Order', subMenu=True)
            mc.menuItem(label='Convert Rotate Order UI', command=partial(convertRotateOrderUI, nodes))
            

def convertRotateOrderUI(nodes, *args):
    '''
    wrapper
    '''
    if ml_convertRotationOrder:
        if nodes:
            mc.select(nodes[-1])
        ml_convertRotationOrder.ui()
        ml_convertRotationOrder.loadTips()
        

if __name__ == '__main__':
    import ml_puppet
    reload(ml_puppet)
    #fkIkSwitchUI()
    initPuppetContextMenu()
    #switchSpace(['ctrlIK_Lf_HindLeg_'],'world')
    #print getSpaceSwitchData('ctrlFK_Head_1_')

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
