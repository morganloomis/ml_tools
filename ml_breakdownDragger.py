# 
#   -= ml_breakdownDragger.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 5, 2014-10-10
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_breakdownDragger.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_breakdownDragger
#     ml_breakdownDragger.drag()
# From MEL, this looks like:
#     python("import ml_breakdownDragger;ml_breakdownDragger.drag()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Blend a keyframe or pose with the next or previous keys, essentially
# creating a breakdown pose that is weighted one way or the other.
# The weight of the blend is controlled by dragging the mouse in the viewport.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool, and the cursor will turn into a hand. Left-click and hold in
# the viewport, and then drag either left or right to weight the key to the
# next or previous key.
# Alternately, press and hold the middle mouse button to weight the key toward
# or away from the average of the surrounding keys.
# If you have no keys selectd, the tool will act only on curves
# that are visibile in the graph editor. If there are no keys at the 
# current frame, keys will be set.
#      ____________________
# - -/__ Video Tutorial __/- - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# http://www.youtube.com/watch?v=D8yD4zbHTP8
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
__revision__ = 5

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya

try:
    import ml_utilities as utl
    utl.upToDateCheck(11)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
def drag():
    '''The primary command to run the tool'''
    BreakdownDragger()

class BreakdownDragger(utl.Dragger):
    '''Creates the tool and manages the data'''

    def __init__(self, 
                 name='mlBreakdownDraggerContext',
                 minValue=None,
                 maxValue=None,
                 defaultValue=0,
                 title = 'Breakdown'):
        
        self.keySel = utl.KeySelection()
        if self.keySel.selectedKeys():
            pass
        elif self.keySel.visibleInGraphEditor():
            self.keySel.setKeyframe()
        elif self.keySel.keyedChannels():
            self.keySel.setKeyframe()
        
        if not self.keySel.curves:
            return
        
        utl.Dragger.__init__(self, defaultValue=defaultValue, minValue=minValue, maxValue=maxValue, name=name, title=title)

        
        #setup tangent type
        itt,ott = utl.getHoldTangentType()
        
        self.time = dict()
        self.value = dict()
        self.next = dict()
        self.prev = dict()
        self.average = dict()

        for curve in self.keySel.curves:
            if self.keySel.selected:
                self.time[curve] = mc.keyframe(curve, query=True, timeChange=True, sl=True)
                self.value[curve] = mc.keyframe(curve, query=True, valueChange=True, sl=True)
            else:
                self.time[curve] = self.keySel.time
                self.value[curve] = mc.keyframe(curve, time=self.keySel.time, query=True, valueChange=True)
                
            self.next[curve] = list()
            self.prev[curve] = list()
            self.average[curve] = list()
            
            for i in self.time[curve]:
                next = mc.findKeyframe(curve, time=(i,), which='next')
                prev = mc.findKeyframe(curve, time=(i,), which='previous')
                n = mc.keyframe(curve, time=(next,), query=True, valueChange=True)[0]
                p = mc.keyframe(curve, time=(prev,), query=True, valueChange=True)[0]
                
                self.next[curve].append(n)
                self.prev[curve].append(p)
                self.average[curve].append((n+p)/2)
                
                #set the tangents on this key, and the next and previous, so they flatten properly
                mc.keyTangent(curve, time=(i,), itt=itt, ott=ott)
                mc.keyTangent(curve, time=(next,), itt=itt)
                mc.keyTangent(curve, time=(prev,), ott=ott)
        
        self.setTool()
        self.drawString('Left: Weight Prev/Next, Middle: Weight Average')
        OpenMaya.MGlobal.displayWarning('Left: Weight Prev/Next, Middle: Weight Average')


    def dragLeft(self):
        '''This is activated by the left mouse button, and weights to the next or previous keys.'''

        #clamp it
        if self.x < -1:
            self.x = -1
        if self.x > 1:
            self.x = 1
            
        if self.x > 0:
            self.drawString('>> '+str(int(self.x*100))+' %')
            for curve in self.keySel.curves:
                for i,v,n in zip(self.time[curve],self.value[curve],self.next[curve]):
                    mc.keyframe(curve, time=(i,), valueChange=v+((n-v)*self.x))
        elif self.x <0:
            self.drawString('<< '+str(int(self.x*-100))+' %')
            for curve in self.keySel.curves:
                for i,v,p in zip(self.time[curve],self.value[curve],self.prev[curve]):
                    mc.keyframe(curve, time=(i,), valueChange=v+((p-v)*(-1*self.x)))
    
    
    def dragMiddle(self):
        '''This is activated by the middle mouse button, and weights to the average of the surrounding keys.'''
        
        #clamp it
        if self.x < -1:
            self.x = -1
        if self.x > 1:
            self.x = 1
            
        self.drawString('Average '+str(int(self.x*100))+' %')
        for curve in self.keySel.curves:
            for i,v,n in zip(self.time[curve],self.value[curve],self.average[curve]):
                mc.keyframe(curve, time=(i,), valueChange=v+((n-v)*self.x))


    def dragShiftLeft(self):
        '''This is activated by Shift and the left mouse button, and weights to the next or previous keys, without clamping.'''
        if self.x > 0:
            self.drawString('>> '+str(int(self.x*100))+' %')
            for curve in self.keySel.curves:
                for i,v,n in zip(self.time[curve],self.value[curve],self.next[curve]):
                    mc.keyframe(curve, time=(i,), valueChange=v+((n-v)*self.x))
        elif self.x <0:
            self.drawString('<< '+str(int(self.x*-100))+' %')
            for curve in self.keySel.curves:
                for i,v,p in zip(self.time[curve],self.value[curve],self.prev[curve]):
                    mc.keyframe(curve, time=(i,), valueChange=v+((p-v)*(-1*self.x)))


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - - 
#
# Revision 1: : First publish
#
# Revision 4: 2014-03-01 : adding category
#
# Revision 5: 2014-10-10 : Bug fixes
