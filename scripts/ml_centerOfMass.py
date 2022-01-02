# -= ml_centerOfMass.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_centerOfMass.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_centerOfMass
#     ml_centerOfMass.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Create a locator that approximates the Center of Mass for the character. This
# locator can be live and simply used as reference, or you can transfer the root
# animation of your character to the center of mass, and then back again after
# you've adjusted any motion. This workflow is helpful for debugging action
# animation when a characters body needs to move in a believable way.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool to launch the UI. Select the root control of your puppet. The tool
# may not error if you select something other than the root, but it may behave
# strangely, so it's up to you to choose the correct control. Then choose to
# either create a live COM node, or transfer your root animation to the center of
# mass. After transferring from Root to COM, you can then transfer back after
# editing.
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
__revision__ = 2

import warnings
import math
import maya.cmds as mc

import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

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

COM_ATTR = 'ml_comSource'
PROGRESS_BAR = None

def ui():
    '''Launch the UI
    '''
    win = CenterOfMassUI()
    win.buildMainLayout()
    win.finish()


class CenterOfMassUI(utl.MlUi):
    '''Inherited from MlUi
    '''

    def __init__(self):

        super(CenterOfMassUI, self).__init__('ml_centerOfMass',
                                               'Center Of Mass',
                                               width=400,
                                               height=150,
                                               info='''Select the root control of your puppet.
Either create a live COM, which will follow center of mass for reference,
or transfer anim to COM for editing, and then back to root again.''')
        self.buildWindow()


    def buildMainLayout(self):
        '''Build the main part of the ui
        '''
        #self.cbBakeOnes = mc.checkBoxGrp(label='Bake on Ones',
                                         #annotation='Bake every frame. If deselected, the tool will preserve keytimes.')

        #mc.separator()
        self.ButtonWithPopup(label='Create Live COM',
                             command=createCenterOfMass,
                             annotation='Create a constrained COM node based on selected Root Control.')

        mc.paneLayout(configuration='vertical2',separatorThickness=1)
        self.ButtonWithPopup(label='Transfer Root Anim to COM',
                             command=bakeCenterOfMass,
                             annotation='Bake out the Root animation to the COM node.')
        self.ButtonWithPopup(label='Transfer COM back to Root',
                             command=bakeRoot,
                             annotation='A previously baked COM will be baked back to its corresponding Root.')
        mc.setParent('..')



def createCenterOfMass(*args):
    '''
    Create a center of mass node, and constrain it to the
    character based on the selected root node.
    '''

    sel = mc.ls(sl=True)

    if not len(sel) == 1:
        raise RuntimeError('Please select the root control of your puppet.')

    print('Create Center Of Mass Node')
    print('--------------------------')

    meshes = meshesFromReference(sel[0]) or meshesFromHistory(sel[0])

    if not meshes:
        raise RuntimeError('Could not determine geometry from selected control. Make sure geo is visible.')

    mc.select(meshes)
    mc.refresh()

    print('Discovered Meshes:')
    for mesh in meshes:
        print('\t',mesh)

    skinnedMeshes = []
    for mesh in meshes:
        if utl.getSkinCluster(mesh):
            skinnedMeshes.append(mesh)
            continue
        hist = mc.listHistory(mesh, breadthFirst=True)
        skins = mc.ls(hist, type='skinCluster')
        if not skins:
            warnings.warn('Could not find a skinned mesh affecting {}'.format(mesh))
            continue
        outGeo = mc.listConnections(skins[0]+'.outputGeometry[0]', source=False)
        outGeo = mc.ls(outGeo, type=['mesh','transform'])
        if not outGeo:
            warnings.warn('Could not find a skinned mesh affecting {}'.format(mesh))
            continue
        skinnedMeshes.append(outGeo[0])

    if not skinnedMeshes:
        raise RuntimeError('Could not determine skinned geometry from selected control. This tool will only work if geo is skinned.')

    locator = centerOfMassLocator(skinnedMeshes)

    mc.addAttr(locator, longName=COM_ATTR, attributeType='message')
    mc.connectAttr('.'.join((sel[0],'message')), '.'.join((locator,COM_ATTR)))

    mc.select(sel)
    return locator


def bakeCenterOfMass(*args):
    '''
    Bake root animation to center of mass.
    '''

    sel = mc.ls(sl=True)

    if not len(sel) == 1:
        raise RuntimeError('Please select the root control of your puppet.')

    root, com = getRootAndCOM(sel[0])

    if not root:
        root = sel[0]
    if not com:
        com = createCenterOfMass()

    start, end = utl.frameRange()
    with utl.IsolateViews():
        mc.bakeResults(com, time=(start,end), sampleBy=1, attribute=['tx','ty','tz'], simulation=True)

    rootOffset = mc.group(em=True, name='rootOffset')
    rootOffset = mc.parent(rootOffset, com)[0]

    #bake
    utl.matchBake(source=[root],
                  destination=[rootOffset],
                  bakeOnOnes=True,
                  maintainOffset=False,
                  preserveTangentWeight=False,
                  translate=True,
                  rotate=True)

    mc.cutKey(root, attribute=['tx','ty','tz','rx','ry','rz'])
    mc.parentConstraint(rootOffset, root)

    mc.select(com)


def bakeRoot(*args):
    '''
    Transfer previously baked animation back to the root.
    '''

    sel = mc.ls(sl=True)

    if not len(sel) == 1:
        raise RuntimeError('Please select the root control or COM locator.')

    root, com = getRootAndCOM(sel[0])

    if not root or not com:
        raise RuntimeError('Could not determine root, please ensure that a COM bake setups has been previously run.')

    parCon = mc.listConnections(root, source=True, destination=True, type='parentConstraint')
    if not parCon:
        raise RuntimeError('Root is not constrained, transfer anim to COM node first.')

    src = mc.listConnections(parCon[0]+'.target[0].targetParentMatrix', source=True, destination=False)

    mc.delete(parCon)

    utl.matchBake(source=[src[0]],
                  destination=[root],
                  bakeOnOnes=True,
                  maintainOffset=False,
                  preserveTangentWeight=False,
                  translate=True,
                  rotate=True)

    for kid in mc.listRelatives(com, pa=True):
        if kid.split('|')[-1] == 'rootOffset':
            mc.delete(kid)
            break

    #reconnect constraint
    con = mc.listRelatives(com, type='pointConstraint', pa=True)
    if con:
        mc.cutKey(com)
        for a in 'XYZ':
            mc.connectAttr(con[0]+'.constraintTranslate'+a, com+'.translate'+a)


def getRootAndCOM(node):
    '''
    Given either the root or COM, return root and COM based on connections.
    '''

    com = None
    root = None

    if mc.attributeQuery(COM_ATTR, node=node, exists=True):
        com = node
        messageCon = mc.listConnections(com+'.'+COM_ATTR, source=True, destination=False)
        if not messageCon:
            raise RuntimeError('Could not determine root from COM, please select root and run again.')
        root = messageCon[0]
    else:
        messageCon = mc.listConnections(node+'.message', source=False, destination=True, plugs=True)
        if messageCon:
            for each in messageCon:
                eachNode, attr = each.rsplit('.',1)
                if attr == COM_ATTR:
                    com = eachNode
                    root = node
                    break

    return root, com


def isNodeVisible(node):
    '''
    Simply return whether or not the node can be seen.
    '''

    if not mc.attributeQuery('visibility', node=node, exists=True):
        return False
    if not mc.getAttr(node+'.v'):
        return False
    if mc.attributeQuery('intermediateObject', node=node, exists=True):
        if mc.getAttr(node+'.intermediateObject'):
            return False
    if not mc.getAttr(node+'.lodVisibility'):
        return False
    if mc.getAttr(node+'.overrideEnabled') and not mc.getAttr(node+'.overrideVisibility'):
        return False

    parent = mc.listRelatives(node, parent=True, pa=True)
    if parent:
        return isNodeVisible(parent[0])
    return True


def meshesFromReference(control):
    '''
    Get meshes from the referenced file. This is faster and more accurate in most
    cases than traversing history, but only works if the rig is referenced.
    '''

    if not mc.referenceQuery(control, isNodeReferenced=True):
        return []

    ref = mc.referenceQuery(control, referenceNode=True)
    nodes = mc.referenceQuery(ref, nodes=True)

    meshes = mc.ls(nodes, type='mesh')

    return [x for x in meshes if isNodeVisible(x)]


def meshesFromHistory(control):
    '''
    Return all visible meshes downstream from a given control.
    '''

    #try searching backward first for speed
    meshes = []
    allMeshes = mc.ls(type='mesh')
    for mesh in allMeshes:
        hist = mc.listHistory(mesh, allConnections=True)
        if control in hist:
            if isNodeVisible(mesh):
                meshes.append(mesh)

    if meshes:
        return meshes

    #if we didn't find any, search forward from control
    #this takes a bit longer
    hier = mc.listRelatives(control, ad=True, pa=True)
    if not hier:
        hier = [control]
    else:
        hier.append(control)

    hist = mc.listHistory(hier, future=True, allFuture=True, allConnections=True)
    hist = list(set(hist))
    meshes = mc.ls(hist, type='mesh')
    meshes = [x for x in meshes if isNodeVisible(x)]

    return meshes


def centerOfMassLocator(meshes):
    '''
    Constrains a locator at the approximate center of mass of a list of skinned meshes.
    '''

    constraintWeights = {}

    numJoints = 0
    skinnedMeshes = []
    for mesh in meshes:
        skin = utl.getSkinCluster(mesh)
        if not skin:
            continue
        numJoints += len(mc.skinCluster(skin, query=True, influence=True))
        skinnedMeshes.append(mesh)

    if not skinnedMeshes:
        raise RuntimeError('No skinClusters affecting the geometry.')

    mc.progressWindow(title='Center Of Mass',
                      progress=0,
                      maxValue=numJoints,
                      status='Prep...',
                      isInterruptable=True )

    mins = [0,0,0]
    maxs = [0,0,0]

    for mesh in skinnedMeshes:

        bb = mc.exactWorldBoundingBox(mesh)
        for i,x in enumerate(bb[:3]):
            mins[1] = min(x,mins[i])
        for i,x in enumerate(bb[3:]):
            maxs[1] = min(x,maxs[i])

        mc.progressWindow(edit=True, step=1, status=('Getting influence data from {}...'.format(mesh)))

        jointMap = getMaxInfluenceMap(mesh)

        mc.progressWindow(edit=True, status='Calculating joint weights...')

        for joint, verts in list(jointMap.items()):

            # Check if the dialog has been cancelled
            if mc.progressWindow( query=True, isCancelled=True ):
                return

            mc.progressWindow(edit=True, step=1)

            faces = mc.polyListComponentConversion(verts, fromVertex=True, toFace=True)
            if not faces:
                continue
            faces = mc.ls(faces,fl=True)

            area = getFacesArea(faces)

            #approximate volume is based on ratio of lateral surface area to volume of a cylinder
            #approxVolume = (area * area) / (4 * math.pi)
            approxVolume = area
            if not joint in constraintWeights:
                constraintWeights[joint] = 0.0
            constraintWeights[joint]+=approxVolume

    mc.progressWindow(endProgress=True)
    if not constraintWeights:
        raise RuntimeError('No skinned geometry found')

    loc = mc.spaceLocator(name='COM_#')[0]
    locShape = mc.listRelatives(loc, shapes=True)[0]

    #set the scale of the locator shape
    scales = [a-b for a,b in zip(maxs,mins)]
    scale = sum(scales)*2
    mc.setAttr(locShape+'.localScale',scale,scale,scale)

    args = list(constraintWeights.keys())
    args.append(loc)
    con = mc.pointConstraint(*args)[0]
    weightAttrs = mc.listAttr(con, ud=True)
    for attr,value in zip(weightAttrs, list(constraintWeights.values())):
        mc.setAttr('{}.{}'.format(con, attr), value)

    return loc


def getFacesArea(faces):
    '''
    Get the area of a list of mesh faces.
    '''

    total=0
    for f in faces:
        om.MGlobal.clearSelectionList()
        om.MGlobal.selectByName(f)
        sList = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(sList)

        sIter = om.MItSelectionList(sList, om.MFn.kMeshPolygonComponent) #change1

        dagPath = om.MDagPath()
        component = om.MObject()

        sIter.getDagPath(dagPath, component) #change2
        polyIter = om.MItMeshPolygon(dagPath, component)

        util = om.MScriptUtil()
        util.createFromDouble(0.0)
        ptr = util.asDoublePtr()
        polyIter.getArea(ptr, om.MSpace.kWorld)
        area = om.MScriptUtil(ptr).asDouble()
        total+=area

    return total


def getMaxInfluenceMap(model):
    '''
    return mesh faces with highest weight for each joint.
    '''
    skin = utl.getSkinCluster(model)
    if not skin:
        return {}

    # get the MFnSkinCluster
    selList = om.MSelectionList()
    selList.add(skin)
    clusterNode = om.MObject()
    selList.getDependNode(0, clusterNode)
    skinFn = oma.MFnSkinCluster(clusterNode)

    # get the MDagPath for all influence
    infDags = om.MDagPathArray()
    skinFn.influenceObjects(infDags)

    # create a dictionary whose key is the MPlug indice id and
    # whose value is the influence list id
    infIds = {}
    joints = {}
    for x in range(infDags.length()):
        infPath = infDags[x].fullPathName()
        infId = int(skinFn.indexForInfluenceObject(infDags[x]))
        infIds[infId] = x
        joints[infId] = infPath

    # get the MPlug for the weightList and weights attributes
    wlPlug = skinFn.findPlug('weightList')
    wPlug = skinFn.findPlug('weights')
    wlAttr = wlPlug.attribute()
    wAttr = wPlug.attribute()
    wInfIds = om.MIntArray()

    #joint is key, value is list of vertices
    weights = {}
    for vId in range(wlPlug.numElements()):
        #loop through verts

        # tell the weights attribute which vertex id it represents
        wPlug.selectAncestorLogicalIndex(vId, wlAttr)
        # get the indice of all non-zero weights for this vert
        wPlug.getExistingArrayAttributeIndices(wInfIds)

        # create a copy of the current wPlug
        infPlug = om.MPlug(wPlug)

        maxWeight = 0
        maxInfId = None
        for infId in wInfIds:
            #loop through influences
            infPlug.selectAncestorLogicalIndex(infId, wAttr)
            #try:
            weight = infPlug.asDouble()
            if weight > maxWeight:
                maxWeight = weight
                maxInfId = infId
                if weight > 0.5:
                    break
            #except KeyError:
            #    pass
        if maxInfId is None:
            continue
        if not maxInfId in joints:
            continue
        joint = joints[maxInfId]
        if not joint in weights:
            weights[joint] = []
        weights[joint].append('{}.vtx[{}]'.format(model,vId))

    return weights

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-12-05 : First publish.
#
# Revision 2: 2018-02-17 : Updating license to MIT.