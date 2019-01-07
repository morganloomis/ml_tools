# -= ml_softWeights.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_softWeights.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_softWeights
#     ml_softWeights.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Set cluster or skinCluster weights based on the current vertex soft selection.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# For clusters, just select vertices and adjust the desired soft selection, then
# press the button. For skinClusters, do the same, but additionally select the
# desired joint as well, then press the skinCluster button.
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

import maya.cmds as mc
import maya.mel as mm
import maya.OpenMaya as om

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

def ui():
    '''
    User interface for ml_softWeights
    '''

    with utl.MlUi('ml_softWeights', 'Soft Weights', width=400, height=180, info='''Set deformer weights based on current soft-selection.
Follow the instructions below for either cluster or skin.
''') as win:

        mc.text(label='Select vertices with soft selection.')
        win.buttonWithPopup(label='Create Cluster', command=softSelectionClusterWeights,
                            annotation='Select a vertex with soft selection to create a cluster.')
        mc.separator(height=20)
        mc.text(label='Select vertices with soft selection, followed by a joint.')
        win.buttonWithPopup(label='Set Joint Weights', command=softSelectionSkinWeights,
                            annotation='Select vertices with soft selection, followed by a joint.')


def getSoftSelectionWeights():

    #get selection
    sel = om.MSelectionList()
    softSelection = om.MRichSelection()
    om.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(sel)

    dagPath = om.MDagPath()
    component = om.MObject()

    iter = om.MItSelectionList(sel, om.MFn.kMeshVertComponent)
    weights = {}

    while not iter.isDone():

        iter.getDagPath( dagPath, component )
        dagPath.pop() #Grab the parent of the shape node
        node = dagPath.fullPathName()
        fnComp = om.MFnSingleIndexedComponent(component)

        for i in range(fnComp.elementCount()):
            weight = 1.0
            if fnComp.hasWeights():
                weight = fnComp.weight(i).influence()

            weights['{}.vtx[{}]'.format(node, fnComp.element(i))] = weight

        iter.next()

    return weights


def softSelectionClusterWeights(*args):

    sel = mc.ls(sl=True, o=True)

    if not sel:
        raise RuntimeError('Please select some vertices.')

    weights = getSoftSelectionWeights()

    if not weights:
        raise RuntimeError('Please select some vertices.')

    #get manipulator position for pivot
    mc.setToolTo('Move')
    moveMode = mc.manipMoveContext('Move', query=True, mode=True)
    mc.manipMoveContext('Move', edit=True, mode=0)
    position = mc.manipMoveContext('Move', query=True, position=True)
    mc.manipMoveContext('Move', edit=True, mode=moveMode)

    clusterNode, clusterHandle = mc.cluster(sel[0])

    for vert in mc.ls(sel[0]+'.vtx[*]', fl=True, l=True):
        weight = 0.0
        if vert in weights.keys():
            weight = weights[vert]
        mc.percent(clusterNode, vert, v=weight)

    #set cluster pivot
    mc.xform(clusterHandle, a=True, ws=True, piv=(position[0], position[1], position[2]))
    clusterShape = mc.listRelatives(clusterHandle, c=True, s=True)
    mc.setAttr(clusterShape[0] + '.origin', position[0], position[1], position[2])


def softSelectionSkinWeights(*args):

    model = mc.ls(sl=True, o=True)
    joints = mc.ls(model, type='joint')
    mc.select(joints, deselect=True)
    weights = getSoftSelectionWeights()

    if not model or not joints or not weights:
        raise RuntimeError('Select vertices followed by a joint')

    if len(joints) > 1:
        raise RuntimeError('Only one joint can be selected at a time')

    joint = joints[0]

    skin = utl.getSkinCluster(model[0])

    if not skin:
        raise RuntimeError('Mesh must have an existing skinCluster')

    influences = mc.skinCluster(skin, query=True, influence=True)
    if joint not in influences:
        mc.skinCluster(skin, edit=True, addInfluence=joint, lockWeights=False, weight=0)

    for influence in influences:
        mc.skinCluster(skin, edit=True, influence=influence, lockWeights=False)

    for vertex, weight in weights.items():
        mc.skinPercent(skin, vertex, transformValue=(joint, weight))

    mc.select(joint)


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-12-31 : Initial publish
#
# Revision 2: 2018-02-17 : Updating license to MIT.