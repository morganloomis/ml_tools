import maya.cmds as mc
import maya.api.OpenMaya as om
from math import isclose
   
def snap(node=None, target=None, offset=None):
    '''
    match one transform to another.
    '''

    #target can be selection....
    if not node and not target:
        sel = mc.ls(sl=True)
        if not len(sel) == 2:
            raise RuntimeError('Select 2 nodes to snap.')
        node, target = sel

    #or a matrix
    if not(isinstance(target, (list, tuple)) and len(target) == 16):
        target = get_worldMatrix(target) 

    set_worldMatrix(node, target, offsetMatrix=offset)


def setAttr_preserveTransform(plug, value):
    '''snap a node to itself after changing a value'''
    node = plug.split('.')[0]
    matrix = get_worldMatrix(node)
    mc.setAttr(plug, value)
    set_worldMatrix(node, matrix)


def get_worldMatrix(node):
    '''
    Fastest way to get world matrix from what I can tell
    '''
    selList = om.MSelectionList()
    matrix = selList.add(node).getDagPath(0).inclusiveMatrix()
    return [x for x in matrix]


def set_worldMatrix(node, matrix, offsetMatrix=None, iterateTolerance=0.0001, iterationMax=4):
    '''
    best way to decompose and set world matrix all in one go?
    om is faster but doesn't undo.
    '''

    if offsetMatrix:
        matrix = [x for x in om.MMatrix(offsetMatrix) * om.MMatrix(matrix)]
    
    iterationMax = iterationMax or 1

    for i in range(iterationMax):
        mc.xform(node, matrix=matrix, worldSpace=True)
        tryAgain = False
        for a,b in zip(matrix, get_worldMatrix(node)):
            if not isclose(a,b,rel_tol=iterateTolerance):
                tryAgain = True
                break
        if not tryAgain:
            return
    