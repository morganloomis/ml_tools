# 
#   -= ml_parentShape.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 1, 2014-03-02
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_parentShape.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_parentShape
#     ml_parentShape.ui()
# From MEL, this looks like:
#     python("import ml_parentShape;ml_parentShape.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Reparent shape nodes to a different transform, or unparent shape
# nodes to a new transform.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# For parenting shapes, select the child and then the parent, just 
# as if you were parenting nodes normally, and run the command.
# For unparenting shapes, select any number of nodes and run the command,
# just as if you were unparenting nodes from a hierarchy.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Parent Shape] : Parent shape of the first selected object to the second
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
from maya import OpenMaya

try:
    import ml_utilities as utl
    utl.upToDateCheck(9)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
hotkey = {'Ctrl+p':'parentShape()','Ctrl+P':'unparentShape()'}

def ui():
    '''
    User interface for parent shape
    '''

    with utl.MlUi('ml_parentShape', 'Parent Shapes', width=400, height=180, info='''Select the child and then the parent.
When parenting shapes, the original transform gets deleted unless it has children.
When unparenting shapes, a transform is created which the shape is parented to.''') as win:

        win.buttonWithPopup(label='Parent Shape', command=parentShape, annotation='Parent shape of the first selected object to the second', 
                            shelfLabel='pShp')
        win.buttonWithPopup(label='Unparent Shape', command=unparentShape, annotation="Unparent the selected objects' shapes to a new transform.", 
                            shelfLabel='upShp')


def parentShape(child=None, parent=None, maintainOffset=True):
    '''
    Parent a child shape node to a parent transform. The child node can be a shape,
    or a transform which has any number of shapes.
    '''
    
    if not child or not parent:
        sel = mc.ls(sl=True)
        if sel and len(sel) > 1:
            child = sel[:-1]
            parent = sel[-1]
        else:
            OpenMaya.MGlobal.displayWarning('Please make a selection.')
            return
    
    parentNodeType = mc.nodeType(parent)
    if not parentNodeType in ('transform', 'joint', 'ikHandle'):
        OpenMaya.MGlobal.displayWarning('Parent must be a transform node.')
        return
    
    if not isinstance(child, (list, tuple)):
        child = [child]
    
    newChild = unparentShape(child)
    
    shapes = list()
    for each in newChild:
        thisChild = mc.parent(each, parent)[0]
        mc.makeIdentity(thisChild, apply=True)
    
        for s in mc.listRelatives(thisChild, shapes=True, noIntermediate=True, path=True):
            shape = mc.parent(s, parent, shape=True, relative=True)[0]
            #move to bottom
            mc.reorder(shape, back=True)
            
            #rename
            parentName = mc.ls(parent, shortNames=True)[0]
            shapes.append(mc.rename(shape, parentName+'Shape#'))

    mc.delete(newChild)
    
    for each in child:
        if not mc.listRelatives(each):
            #if it doesn't have any kids, delete it
            mc.delete(each)
        
    return shapes
    

def unparentShape(objs=None):

    if not objs:
        objs = mc.ls(sl=True)
        if not objs:
            OpenMaya.MGlobal.displayWarning('Please select one or more nodes with shapes to unparent.')
            return
    elif not isinstance(objs, (list,tuple)):
        objs = [objs]
    
    #are these shapes or transforms
    transforms = list()
    shapes = list()
    for obj in objs:
        nodeType = mc.nodeType(obj)
        if nodeType in ('mesh','nurbsCurve','nurbsSurface','locator','annotationShape'):
            shapes.append(obj)
        elif nodeType in ('transform', 'joint', 'ikHandle'):
            if not mc.listRelatives(obj, shapes=True, path=True, noIntermediate=True):
                OpenMaya.MGlobal.displayWarning(obj+' has no shapes, skipping.')
                return
            transforms.append(obj)
        else:
            OpenMaya.MGlobal.displayWarning(obj+' must be a shape, or a transform with shapes. Skipping')
            return
    
    for each in transforms:
        childShapes = mc.listRelatives(each, shapes=True, path=True, noIntermediate=True)
        shapes.extend([x for x in childShapes if x not in shapes])
    
    #shapes that share a common parent get unparented together
    newTransforms = dict()
    for each in shapes:
        shapeParent = mc.listRelatives(each, parent=True, fullPath=True)[0]
        if not shapeParent in newTransforms:
            newTransforms[shapeParent] = mc.createNode('transform', name='unparentedShape#')
            newTransforms[shapeParent] = mc.parent(newTransforms[shapeParent], shapeParent)[0]
            mc.setAttr(newTransforms[shapeParent]+'.translate', 0,0,0)
            mc.setAttr(newTransforms[shapeParent]+'.rotate', 0,0,0)
            mc.setAttr(newTransforms[shapeParent]+'.scale', 1,1,1)
            newTransforms[shapeParent] = mc.parent(newTransforms[shapeParent], world=True)[0]
        
        shape = mc.parent(each, newTransforms[shapeParent], shape=True, relative=True)[0]
    return newTransforms.values()
        

if __name__ == '__main__':
    ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2014-03-02 : First publish.
