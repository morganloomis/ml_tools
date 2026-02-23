# -= ml_keyValueDragger.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 5
#   / / / / / / /  2018-05-14
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_keyValueDragger.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_keyValueDragger
#     ml_keyValueDragger.drag()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Scale keyframes to their default value by dragging in the viewport.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool, and the cursor will turn into a hand. Left-click and hold in the
# viewport, and then drag either left or right to scale the key value up or down.
# If you have no keys selectd, the tool will act only on curves that are visibile
# in the graph editor. If there are no keys at the current frame, keys will be
# set.
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
__revision__ = 5
__category__ = 'animation'

shelfButton = {'annotation': 'Adjust the value of the current key by dragging in the viewport.',
               'command': 'import ml_keyValueDragger;ml_keyValueDragger.drag()',
               'order': 13}

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
    KeyValueDragger()


class KeyValueDragger(utl.Dragger):
    '''Creates the tool and manages the data'''

    def __init__(self,
                 name='mlKeyValueDraggerContext',
                 minValue=0,
                 maxValue=None,
                 defaultValue=1,
                 title = 'Scale'):

        self.keySel = utl.KeySelection()
        selected = False
        if self.keySel.selectedKeys():
            selected = True
            pass
        elif self.keySel.visibleInGraphEditor():
            self.keySel.setKeyframe()
        elif self.keySel.keyedChannels():
            self.keySel.setKeyframe()
        elif self.keySel.selectedObjects():
            self.keySel.setKeyframe()

        if not self.keySel.initialized:
            return

        utl.Dragger.__init__(self, defaultValue=defaultValue, minValue=minValue, maxValue=maxValue, name=name, title=title)

        self.time = dict()
        self.default = dict()
        self.value = dict()
        self.curves = self.keySel.curves

        for curve in self.curves:
            if selected:
                self.time[curve] = mc.keyframe(curve, query=True, timeChange=True, sl=True)
                self.value[curve] = mc.keyframe(curve, query=True, valueChange=True, sl=True)
            else:
                self.time[curve] = self.keySel.time
                self.value[curve] = mc.keyframe(curve, time=self.keySel.time, query=True, valueChange=True)

            #get the attribute's default value
            node, attr = mc.listConnections('.'.join((curve,'output')), source=False, plugs=True)[0].split('.')
            self.default[curve] = mc.attributeQuery(attr, listDefault=True, node=node)[0]

        self.setTool()
        onscreenInstructions = 'Drag left to scale toward default, and right to go in the opposite direction.'
        self.drawString(onscreenInstructions)
        OpenMaya.MGlobal.displayWarning(onscreenInstructions)


    def dragLeft(self):
        '''
        Activated by the left mouse button, this scales keys toward or away from their default value.
        '''
        self.drawString('Scale '+str(int(self.x*100))+' %')
        for curve in self.curves:
            for i,v in zip(self.time[curve], self.value[curve]):
                mc.keyframe(curve, time=(i,), valueChange=self.default[curve]+((v-self.default[curve])*self.x))

