# -= ml_breakdown.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 4
#   / / / / / / /  2018-05-13
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_breakdown.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_breakdown
#     ml_breakdown.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Blend a keyframe or pose with the next or previous keys, essentially creating a
# breakdown pose that is weighted one way or the other.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Press the "Breakdown Dragger" button to enter the dragger, and the cursor will
# turn into a hand. Left-click and hold in the viewport, and then drag either left
# or right to weight the key to the next or previous key. Press and hold the
# middle mouse button to weight the key toward or away from the average of the
# surrounding keys. Alternately, set the slider to the desired weight, and press
# the Next, Previous or Average buttons to increment the breakdown. Right click
# the buttons to assign to hotkeys. If you have no keys selected, the tool will
# act only on curves that are visibile in the graph editor. If there are no keys
# at the current frame, keys will be set.
# 
#     ____________
# - -/__ Video __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# http://www.youtube.com/watch?v=D8yD4zbHTP8
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Breakdown Dragger] : Drag in the viewport to weight a breakdown toward the next or previous frame.
# [<<] : Weight toward the previous frame.
# [Average] : Weight toward the average of the next and previous frame.
# [>>] : Weight toward the next frame.
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
__revision__ = 4
__category__ = 'animation'

shelfButton = {'annotation': 'Click to weight keys by dragging, double click to open UI.',
               'command': 'import ml_breakdown;ml_breakdown.drag()',
               'doubleClickCommand': 'import ml_breakdown;ml_breakdown.ui()',
               'imageOverlayLabel': 'BD',
               'menuItem': [['Breakdown UI', 'import ml_breakdown;ml_breakdown.ui()'],
                            ['<< Previous', 'import ml_breakdown;ml_breakdown.weightPrevious()'],
                            ['>> Next', 'import ml_breakdown;ml_breakdown.weightNext()'],
                            ['Average', 'import ml_breakdown;ml_breakdown.weightAverage()']],
               'order': 12}

import maya.cmds as mc
from maya import OpenMaya
from functools import partial

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
    User interface for breakdown
    '''

    with utl.MlUi('ml_breakdown', 'Breakdown Tools', width=400, height=180, info='''Select objects.
Press Breakdown Dragger to create a new key and weight it by dragging in the viewport.
Otherwise use the increment buttons to nudge a key's value toward the next or previous key.''') as win:

        win.buttonWithPopup(label='Breakdown Dragger', command=drag, annotation='Drag in the viewport to weight a breakdown toward the next or previous frame.',
                            shelfLabel='BDD')

        mc.separator(height=20)
        mc.floatSliderGrp('ml_breakdown_value_floatSlider', value=0.2, field=True, minValue=0, maxValue=2)
        mc.paneLayout(configuration='vertical3',separatorThickness=1)
        win.ButtonWithPopup(label='<<', command=weightPrevious, annotation='Weight toward the previous frame.', shelfLabel='<', shelfIcon='defaultTwoStackedLayout',
                            readUI_toArgs={'weight':'ml_breakdown_value_floatSlider'})
        win.ButtonWithPopup(label='Average', command=weightAverage, annotation='Weight toward the average of the next and previous frame.', shelfLabel='><', shelfIcon='defaultTwoStackedLayout',
                            readUI_toArgs={'weight':'ml_breakdown_value_floatSlider'})
        win.ButtonWithPopup(label='>>', command=weightNext, annotation='Weight toward the next frame.', shelfLabel='>', shelfIcon='defaultTwoStackedLayout',
                            readUI_toArgs={'weight':'ml_breakdown_value_floatSlider'})


def quickBreakDownUI():
    winName = 'ml_quickBreakdownWin'
    if mc.window(winName, exists=True):
        mc.deleteUI(winName)

    mc.window(winName, title='ml :: QBD', iconName='Quick Breakdown', width=100, height=500)

    mc.columnLayout(adj=True)

    mc.paneLayout(configuration='vertical2', separatorThickness=1)
    mc.text('<<')
    mc.text('>>')
    mc.setParent('..')

    for v in (10,20,50,80,90,100,110,120,150):
        mc.paneLayout(configuration='vertical2',separatorThickness=1)

        mc.button(label=str(v)+' %', command=partial(weightPrevious,v/100.0))
        mc.button(label=str(v)+' %', command=partial(weightNext,v/100.0))
        mc.setParent('..')

    mc.showWindow(winName)

    mc.window(winName, edit=True, width=100, height=250)


def drag(*args):
    '''The primary command to run the tool'''
    BreakdownDragger()


def weightPrevious(weight=0.2, *args):
    weightBreakdownStep(direction='previous', weight=weight)


def weightAverage(weight=0.2, *args):
    weightBreakdownStep(direction='average', weight=weight)


def weightNext(weight=0.2, *args):
    weightBreakdownStep(direction='next', weight=weight)


def weightBreakdownStep(direction='next', weight=0.2):

    keySel = utl.KeySelection()
    if keySel.selectedKeys():
        pass
    elif keySel.visibleInGraphEditor():
        keySel.setKeyframe()
    elif keySel.keyedChannels():
        keySel.setKeyframe()

    if not keySel.curves:
        return

    times = list()
    values = list()

    data = list()

    for curve in keySel.curves:
        if keySel.selected:
            times = mc.keyframe(curve, query=True, timeChange=True, sl=True)
            values = mc.keyframe(curve, query=True, valueChange=True, sl=True)
        else:
            times = [keySel.time]
            values = mc.keyframe(curve, time=keySel.time, query=True, valueChange=True)

        for i,v in zip(times,values):
            nextTime = mc.findKeyframe(curve, time=(i,), which='next')
            n = mc.keyframe(curve, time=(nextTime,), query=True, valueChange=True)[0]
            prevTime = mc.findKeyframe(curve, time=(i,), which='previous')
            p = mc.keyframe(curve, time=(prevTime,), query=True, valueChange=True)[0]

            data.append([curve,i,v,n,p])

    for d in data:

        value = None
        if direction == 'next':
            value = d[2]+((d[3]-d[2])*weight)
        elif direction == 'previous':
            value = d[2]+((d[4]-d[2])*weight)
        elif direction == 'average':
            value = d[2]+(((d[3]+d[4])/2-d[2])*weight)
        else: break

        mc.keyframe(d[0], time=(d[1],), valueChange=value)


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


if __name__ == '__main__':
    quickBreakDownUI()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2015-05-13 : First publish.
#
# Revision 2: 2015-05-13 : Documentation updates.
#
# Revision 3: 2018-02-17 : Updating license to MIT.
#
# Revision 4: 2018-05-13 : shelf support