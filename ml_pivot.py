# 
#   -= ml_pivot.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 2, 2017-06-26
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_pivot.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_pivot
#     ml_pivot.ui()
# From MEL, this looks like:
#     python("import ml_pivot;ml_pivot.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Change the rotate pivot of animated nodes. This is not a pivot switcher, it changes the pivot for
# the whole animation but preserves position by baking translation on ones. Eventually
# I'd like to make it a bit smarter about how it bakes.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI. Select a node whose pivot you'd like to change, and press Edit Pivot.
# Your selection with change to handle, position this where you'd like the pivot to be 
# and press Return. Or press ESC or select something else to cancel.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Edit Pivot] : Creates a temporary node to positon for the new pivot.
# [Reset Pivot] : Rest the rotation pivot to zero.
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
__revision__ = 2

try:
    from PySide2 import QtGui, QtCore
    import shiboken2 as shiboken
except ImportError:
    from PySide import QtGui, QtCore
    import shiboken

import maya.OpenMaya as om
import maya.OpenMayaUI as mui
import maya.cmds as mc

try:
    import ml_utilities as utl
    utl.upToDateCheck(30)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    

#get maya window as qt object
main_window_ptr = mui.MQtUtil.mainWindow()
qt_maya_window = shiboken.wrapInstance(long(main_window_ptr), QtCore.QObject)

def ui():
    '''
    user interface for ml_pivot
    '''

    with utl.MlUi('ml_pivot', 'Change Pivot', width=400, height=150, info='''Select an animated control whose pivot you'd like to change, and press Edit Pivot.
Your selection with change to handle, position this where you'd like the pivot to be 
and press Return. Or press ESC or deselect to cancel.''') as win:

        win.buttonWithPopup(label='Edit Pivot', command=edit_pivot, annotation='Creates a temporary node to positon for the new pivot.', shelfLabel='pivot', shelfIcon='defaultTwoStackedLayout')
        win.buttonWithPopup(label='Reset Pivot', command=reset_pivot, annotation='Rest the rotation pivot to zero.', shelfLabel='reset', shelfIcon='defaultTwoStackedLayout')


def edit_pivot(*args):
    context = EditPivotContext()
    context.editPivot()


class PivotKeypressFilter(QtCore.QObject):
    '''
    A qt event filter to catch the enter or escape keypresses.
    '''
    def __init__(self, enterCommand, escapeCommand):
        self.enterCommand = enterCommand
        self.escapeCommand = escapeCommand
        super(PivotKeypressFilter, self).__init__()


    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                with utl.UndoChunk(force=True):
                    self.enterCommand()
            if event.key() == QtCore.Qt.Key_Escape:
                self.escapeCommand()
                qt_maya_window.removeEventFilter(self)
        return False


class EditPivotContext(object):
    
    def __init__(self):
        
        self.node = None
        self.pivotHandle = None
        self.scriptJob = None
        self.keypressFilter = PivotKeypressFilter(self.bakePivot, self.cleanup)
        
    
    
    def editPivot(self, *args):
        sel = mc.ls(sl=True)
        
        if not sel:
            om.MGlobal.displayWarning('Nothing selected.')
            return
        
        if len(sel) > 1:
            om.MGlobal.displayWarning('Only works on one node at a time.')
            return
        
        if mc.attributeQuery('ml_pivot_handle', exists=True, node=sel[0]):
            #we have a pivot handle selected
            return
        
        if is_pivot_connected(sel[0]):
            return
        
        self.node = sel[0]
        
        qt_maya_window.installEventFilter(self.keypressFilter)        
        
        
        #create transform
        self.pivotHandle = mc.group(em=True, name='Adjust_Pivot')
        mc.setAttr(self.pivotHandle+'.rotate', lock=True)
        mc.setAttr(self.pivotHandle+'.rx', keyable=False)
        mc.setAttr(self.pivotHandle+'.ry', keyable=False)
        mc.setAttr(self.pivotHandle+'.rz', keyable=False)
        mc.setAttr(self.pivotHandle+'.scale', lock=True)
        mc.setAttr(self.pivotHandle+'.sx', keyable=False)
        mc.setAttr(self.pivotHandle+'.sy', keyable=False)
        mc.setAttr(self.pivotHandle+'.sz', keyable=False)
        mc.setAttr(self.pivotHandle+'.visibility', lock=True, keyable=False)
        mc.setAttr(self.pivotHandle+'.displayHandle', True)
        
        self.pivotHandle = mc.parent(self.pivotHandle, self.node)[0]
        
        mc.addAttr(self.pivotHandle, ln='ml_pivot_handle', at='bool', keyable=False)
        
        #set initial position
        mc.setAttr(self.pivotHandle+'.translate', *mc.getAttr(self.node+'.rotatePivot')[0])
        
        #lock it so you don't delete it or something.
        mc.lockNode(self.pivotHandle, lock=True)
        
        self.scriptJob = mc.scriptJob(event=['SelectionChanged', self.cleanup], runOnce=True)
        
        mc.setToolTo('Move')
        
        mc.inViewMessage( amg='After moving the pivot, press <hl>Return</hl> to bake or <hl>Esc</hl> to cancel.', pos='midCenterTop', fade=True, fadeStayTime=4000, dragKill=True)
    
    
    def bakePivot(self):
        
        if not mc.objExists(self.pivotHandle) or not mc.objExists(self.node):
            self.cleanup()
            return
        
        newPivot = mc.getAttr(self.pivotHandle+'.translate')[0]
        
        if newPivot == mc.getAttr(self.node+'.rotatePivot')[0]:
            self.cleanup()
            return
        
        if not mc.keyframe(self.node, attribute=('tx','ty','tz','rx','ry','rz'), query=True, name=True):
            mc.setAttr(self.node+'.rotatePivot', *newPivot)
            self.cleanup()
            return
    
        tempPosition = mc.group(em=True)
        mc.delete(mc.parentConstraint(self.pivotHandle, tempPosition))
    
        utl.matchBake(source=[self.node], destination=[tempPosition], bakeOnOnes=True, maintainOffset=True, preserveTangentWeight=False, rotate=False)
        
        mc.setAttr(self.node+'.rotatePivot', *newPivot)
        utl.matchBake(source=[tempPosition], destination=[self.node], bakeOnOnes=True, maintainOffset=False, preserveTangentWeight=False, rotate=False)
        
        mc.delete(tempPosition)    
        
        mc.select(self.node)
        
        self.cleanup()
        
        #end context
        try:
            qt_maya_window.removeEventFilter(self.keypressFilter)
        except:
            pass
        
    
    def cleanup(self):
        '''
        Clean up the mess we made.
        '''
        try:
            mc.lockNode(self.pivotHandle, lock=False)
            mc.delete(self.pivotHandle)
        except: pass
        
        try:
            if mc.scriptJob(exists=self.scriptJob):
                mc.scriptJob(kill=self.scriptJob, force=True)
        except: pass
        
        pivotHandles = mc.ls('*.ml_pivot_handle', o=True)
        if pivotHandles:
            for each in pivotHandles:
                mc.lockNode(each, lock=False)
                mc.delete(each)


def is_pivot_connected(node):
    for each in ('rotatePivot', 'rotatePivotX', 'rotatePivotY', 'rotatePivotZ'):
        if mc.listConnections(node+'.'+each, source=True, destination=False):
            om.MGlobal.displayWarning('Pivot attribute is connected, unable to edit.')
            return True
    return False


def reset_pivot(*args):

    sel = mc.ls(sl=True)
    if not sel:
        om.MGlobal.displayWarning('Nothing selected.')
        return

    if len(sel) > 1:
        om.MGlobal.displayWarning('Only works on one node at a time.')
        return

    if is_pivot_connected(sel[0]):
        return    

    node = sel[0]

    pivotPosition = mc.getAttr(node+'.rotatePivot')[0]
    if pivotPosition  == (0.0,0.0,0.0):
        return

    tempPosition = mc.group(em=True)
    tempPivot = mc.group(em=True)
    tempPivot = mc.parent(tempPivot, node)[0]
    mc.setAttr(tempPivot+'.translate', 0,0,0)
    mc.setAttr(tempPivot+'.rotate', 0,0,0)

    utl.matchBake(source=[tempPivot], destination=[tempPosition], bakeOnOnes=True, maintainOffset=False, preserveTangentWeight=False, rotate=False)

    mc.setAttr(node+'.rotatePivot', 0,0,0)
    utl.matchBake(source=[tempPosition], destination=[node], bakeOnOnes=True, maintainOffset=False, preserveTangentWeight=False, rotate=False)

    mc.delete(tempPosition,tempPivot)    

    mc.select(node)


if __name__ == '__main__':
    ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-06-21 : First publish.
#
# Revision 2: 2017-06-26 : update for pySide2, maya 2017
