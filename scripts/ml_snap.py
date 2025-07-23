import maya.cmds as mc
import maya.api.OpenMaya as om
import math
import ml_utilities as utl

def snap(node=None, target=None, offset=None, position=True, orientation=True, iterationMax=4):
    '''
    match one transform to another.
    '''

    #target can be selection....
    if not node and not target:
        sel = mc.ls(sl=True)
        if not len(sel) == 2:
            utl.error('Select a source and target node to snap.')
        node, target = sel
    
    if isinstance(target, (list, tuple, utl.Vector)):
        if len(target) == 3:
            #point
            target = position_to_matrix(target)
        elif len(target) != 16:
            raise RuntimeError(f'Target {target} is not valid')
    elif mc.objExists(target):
        #object
        target = get_worldMatrix(target)
    else:
        raise RuntimeError(f'Target {target} is not valid')
    
    set_worldMatrix(node, target, offsetMatrix=offset, position=position, orientation=orientation, iterationMax=iterationMax)


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

def get_worldPosition(node):
    return get_worldMatrix(node)[12:15]

def position_to_matrix(position):
    return [1,0,0,0, 0,1,0,0, 0,0,1,0, position[0], position[1], position[2], 1]


def set_worldMatrix(node, matrix, offsetMatrix=None, iterateTolerance=0.0001, iterationMax=4, position=True, orientation=True):
    '''
    best way to decompose and set world matrix all in one go?
    om is faster but doesn't undo.
    '''

    if offsetMatrix:
        matrix = [x for x in om.MMatrix(offsetMatrix) * om.MMatrix(matrix)]
        #need to support offsets and iteration
        iterationMax=1
    
    iterationMax = iterationMax or 1

    #check if there's a better way to do this with xform
    translate = [0,0,0]
    for i in range(iterationMax):
        if not position:
            p = get_worldPosition(node)
            for i,p in zip([12,13,14,15], p):
                matrix[i] = p
        if not orientation:
            pass

        mc.xform(node, matrix=matrix, worldSpace=True)

        if iterationMax == 1:
            return
        tryAgain = False
        for a,b in zip(matrix, get_worldMatrix(node)):
            if not math.isclose(a,b,rel_tol=iterateTolerance):
                tryAgain = True
                break
        if not tryAgain:
            return
    
def copy_values(src, dst):
    srcAnimatable = mc.listAnimatable(src)
    if not srcAnimatable:
        return
    dstAnimatable = mc.listAnimatable(dst)
    if not dstAnimatable:
        return

    srcAttr = [x.split('.',1)[-1] for x in srcAnimatable]
    dstAttr = [x.split('.',1)[-1] for x in dstAnimatable]

    srcAttr.extend(mc.listAttr(src, cb=True) or [])
    dstAttr.extend(mc.listAttr(dst, cb=True) or [])

    attrs = list( set(srcAttr).intersection(set(dstAttr)))
    for attr in attrs:
        try:
            mc.setAttr(f'{dst}.{attr}', mc.getAttr(f'{src}.{attr}'))
        except:
            pass
    