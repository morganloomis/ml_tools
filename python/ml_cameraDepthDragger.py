# -= ml_cameraDepthDragger.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_cameraDepthDragger.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_cameraDepthDragger
#     ml_cameraDepthDragger.drag()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Move objects closer to or further from camera, such that they don't change
# location in screen space, just get larger or smaller in frame.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool, and then click and drag the mouse in the viewport to move
# selected objects closer or further from camera. When you release click, the tool
# will exit.
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
__revision__ = 4

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya

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

def drag():
    '''The primary command to run the tool'''
    CameraDepthDragger()


class CameraDepthDragger(utl.Dragger):

    def __init__(self,
                 name='mlCameraDepthDraggerContext',
                 minValue=None,
                 maxValue=None,
                 defaultValue=0,
                 title = 'CameraDepth'):

        utl.Dragger.__init__(self, defaultValue=defaultValue, minValue=minValue, maxValue=maxValue, name=name, title=title)

        #get the camera that we're looking through, and the objects selected
        cam = utl.getCurrentCamera()
        sel = mc.ls(sl=True)

        if not sel:
            OpenMaya.MGlobal.displayWarning('Please make a selection.')
            return

        #get the position of the camera in space and convert it to a vector
        camPnt = mc.xform(cam, query=True, worldSpace=True, rotatePivot=True)
        self.cameraVector = utl.Vector(camPnt[0],camPnt[1],camPnt[2])

        self.objs = list()
        self.vector = list()
        self.normalized = list()
        for obj in sel:
            #make sure all translate attributes are settable
            if not mc.getAttr(obj+'.translate', settable=True):
                print 'not settable'
                continue

            #get the position of the objects as a vector, and subtract the camera vector from that
            objPnt = mc.xform(obj, query=True, worldSpace=True, rotatePivot=True)
            objVec = utl.Vector(objPnt[0],objPnt[1],objPnt[2])
            self.objs.append(obj)
            self.vector.append(objVec-self.cameraVector)
            self.normalized.append(self.vector[-1].normalized())

        if not self.objs:
            OpenMaya.MGlobal.displayWarning('No selected objects are freely translatable')
            return

        if len(sel) != len(self.objs):
            OpenMaya.MGlobal.displayWarning('Some objects skipped, due to not being freely translatable')

        self.setTool()


    def dragMult(self, mult):
        #as the mouse is dragging, update the position of each object by muliplying
        #the vector and adding to the original position
        for obj, v, n in zip(self.objs,self.vector,self.normalized):
            vector = (n * self.x * mult) + v + self.cameraVector

            mc.move(vector[0],vector[1],vector[2], obj, absolute=True, worldSpace=True)


    def dragLeft(self):
        '''
        drag normal speed
        '''
        self.dragMult(4)


#     def dragShiftLeft(self):
#         '''
#         drag double speed
#         '''
#         print 'shift'
#         self.dragMult(8)
#
#
#     def dragControlLeft(self):
#         '''
#         drag half speed
#         '''
#         print 'ctrl'
#         self.dragMult(2)

if __name__ == '__main__': drag()


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2012-03-12 : First publish.
#
# Revision 2: 2014-03-01 : adding category
#
# Revision 3: 2016-12-10 : Removing euclid dependency
#
# Revision 4: 2018-02-17 : Updating license to MIT.