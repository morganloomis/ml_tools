# -= ml_pivot.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 4
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_pivot.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_pivot
#     ml_pivot.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Change the rotate pivot of animated nodes. This is not a pivot switcher, it
# changes the pivot for the whole animation but preserves position by baking
# translation on ones. Eventually I'd like to make it a bit smarter about how it
# bakes.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI. Select a node whose pivot you'd like to change, and press Edit
# Pivot. Your selection with change to handle, position this where you'd like the
# pivot to be and press Return. Or press ESC or select something else to cancel.
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Edit Pivot] : Creates a temporary node to positon for the new pivot.
# [Reset Pivot] : Rest the rotation pivot to zero.
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
__revision__ = 1
__category__ = 'animation'

try:
    from PySide2 import QtGui, QtCore
    import shiboken2 as shiboken
except ImportError:
    from PySide import QtGui, QtCore
    import shiboken

import maya.OpenMaya as om
import maya.OpenMayaUI as mui
import maya.cmds as mc
import math

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


#get maya window as qt object
main_window_ptr = mui.MQtUtil.mainWindow()
qt_maya_window = shiboken.wrapInstance(int(main_window_ptr), QtCore.QObject)

def ui():
    '''
    user interface for ml_spacing
    '''

    with utl.MlUi('ml_spacing', 'Sp a c i  n    g', width=400, height=150, info='''Things,
And stuff.''') as win:

        win.buttonWithPopup(label='Edit Pivot', command=edit_pivot, annotation='Creates a temporary node to positon for the new pivot.', shelfLabel='pivot', shelfIcon='defaultTwoStackedLayout')
        win.buttonWithPopup(label='Reset Pivot', command=reset_pivot, annotation='Rest the rotation pivot to zero.', shelfLabel='reset', shelfIcon='defaultTwoStackedLayout')


def linear(x):
    return x
    
def sigmoid(x):
    return 1 / (1 + math.exp(-10*(x-0.5)))

def easeIn_sine(x):
    return math.sin(((x*0.5)-0.5)*math.pi)+1

def easeOut_sine(x):
    return math.sin((x*0.5)*math.pi)

def easeInOut_sine(x):
    return math.sin((x+1.5)*math.pi)/2+0.5

def easeIn_quad(x):
    return x**2

def easeOut_quad(x):
    return -1*x*(x-2)

def easeInOut_quad(x):
    if x<0.5:
        return easeIn_quad(x)*2
    else:
        return easeOut_quad(x)*2-1

def easeIn_cubic(x):
    return x**3

def easeOut_cubic(x):
    return (x-1)**3 + 1

def easeInOut_cubic(x):
    #this doesn't work
    if x<0.5:
        x/=2
        return easeIn_cubic(x)/2
    else:
        x/=2
        return (easeOut_cubic(x)+2)/2


def getPose(node):
    data = {}
    for attr in mc.listAttr(node, keyable=True):
        plug = '{}.{}'.format(node, attr)
        data[plug] = mc.getAttr(plug)
    return data
                

def applySpacing(startPose, endPose, startFrame, endFrame, spacingFunction):
    
    r = endFrame-startFrame
    step = 1.0/r
    for attr,value in list(startPose.items()):
        if not attr in endPose:
            continue
        for i in range(r+1):
            newValue = (spacingFunction(step*i) * (endPose[attr] - value)) + value
            mc.setKeyframe(attr, time=startFrame+i, value=newValue)
    


def spacing(*args):
    context = SpacingContext()
    context.editPivot()


class KeypressFilter(QtCore.QObject):
    '''
    A qt event filter to catch the enter or escape keypresses.
    '''
    def __init__(self, enterCommand, escapeCommand):
        '''
        Pass a command to run on enter, and one to run on escape.
        '''
        self.enterCommand = enterCommand
        self.escapeCommand = escapeCommand
        super(KeypressFilter, self).__init__()


    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                with utl.UndoChunk(force=True):
                    self.enterCommand()
            if event.key() == QtCore.Qt.Key_Escape:
                self.escapeCommand()
                qt_maya_window.removeEventFilter(self)
        return False


class SpacingContext(object):

    def __init__(self):

        self.node = None
        self.pivotHandle = None
        self.scriptJob = None
        self.keypressFilter = KeypressFilter(self.bakePivot, self.cleanup)


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

        self.node = sel[0]

        if is_pivot_connected(sel[0]):
            driverAttr = pivot_driver_attr(sel[0])
            if driverAttr:
                self.editPivotDriver(driverAttr)
            else:
                om.MGlobal.displayWarning('Pivot attribute is connected, unable to edit.')
            return

        self.editPivotHandle()


    def editPivotDriver(self, driver):

        self.pivotDriver = driver

        #get driver range
        node,attr = driver.split('.',1)
        value = mc.getAttr(driver)

        minValue = mc.attributeQuery(attr, node=node, minimum=True)[0]
        maxValue = mc.attributeQuery(attr, node=node, maximum=True)[0]

        #create a ui with a slider
        self.pivotDriverWindow = 'ml_pivot_editPivotDriverUI'

        if mc.window(self.pivotDriverWindow, exists=True):
            mc.deleteUI(self.pivotDriverWindow)
        window = mc.window(self.pivotDriverWindow, width=1, height=1)
        mc.columnLayout()
        self.floatSlider = mc.floatSliderButtonGrp(label=attr,
                                                   field=True,
                                                   value=value,
                                                   buttonLabel='Bake',
                                                   minValue=minValue,
                                                   maxValue=maxValue,
                                                   buttonCommand=self.doEditPivotDriver )
        mc.showWindow( window )
        mc.window(self.pivotDriverWindow, edit=True, width=1, height=1)

    def doEditPivotDriver(self, *args):

        newValue = mc.floatSliderButtonGrp(self.floatSlider, query=True, value=True)
        try:
            mc.deleteUI(self.pivotDriverWindow)
        except:
            pass

        currentValue = mc.getAttr(self.pivotDriver)
        if newValue == currentValue:
            return

        oldRP = mc.getAttr(self.node+'.rotatePivot')[0]
        mc.setAttr(self.pivotDriver, newValue)
        newRP = mc.getAttr(self.node+'.rotatePivot')[0]
        mc.setAttr(self.pivotDriver, currentValue)

        parentPosition = mc.group(em=True)
        offsetPosition = mc.group(em=True)
        offsetPosition = mc.parent(offsetPosition, parentPosition)[0]
        mc.setAttr(offsetPosition+'.translate', newRP[0]-oldRP[0], newRP[1]-oldRP[1], newRP[2]-oldRP[2])

        mc.delete(mc.parentConstraint(self.node, parentPosition))

        utl.matchBake(source=[self.node], destination=[parentPosition], bakeOnOnes=True, maintainOffset=False, preserveTangentWeight=False)

        mc.cutKey(self.pivotDriver)
        mc.setAttr(self.pivotDriver, newValue)
        mc.refresh()
        utl.matchBake(source=[offsetPosition], destination=[self.node], bakeOnOnes=True, maintainOffset=False, preserveTangentWeight=False, rotate=False)

        mc.delete(parentPosition)


    def editPivotHandle(self):

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




if __name__ == '__main__':
    ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-06-21 : First publish.
#