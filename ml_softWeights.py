# 
#   -= ml_softWeights.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 1, 2016-12-31
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_softWeights.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_softWeights
#     ml_softWeights.ui()
# From MEL, this looks like:
#     python("import ml_softWeights;ml_softWeights.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Set cluster or skinCluster weights based on the current vertex soft selection.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# For clusters, just select vertices and adjust the desired soft selection, then
# press the button. For skinClusters, do the same, but additionally select the
# desired joint as well, then press the skinCluster button. 
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'riggingScripts'
__revision__ = 1

import maya.cmds as mc
import maya.mel as mm
import maya.OpenMaya as om

try:
    import ml_utilities as utl
    utl.upToDateCheck(27)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
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
