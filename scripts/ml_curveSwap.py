# -= ml_curveSwap.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 8
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
# COPYRIGHT curveSwapERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#     ___________________
# - -/__ Installation __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_curveSwap.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_curveSwap
#     ml_curveSwap.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly create animation curveSwaps, either for individual poses or over a range of
# keys. Select a range of keys in the graph editor or the time slider, or match
# your current pose to the next or previous one.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI. Press Next and Previous to match keys to the value of next or
# previous keyframes. Press Current or Average to turn a frame range into a curveSwap.
# Current sets the curveSwap to be the current value, and average sets the value to the
# average of all keys across the range. The range is determined by one of 3
# things, in the following order: 1. Selected range in the time slider. 2. The
# highest and lowest selected keys in the graph editor. 3. If nothing is selected,
# the previous and next keys from the current time determine the range. If you
# have no keys selectd, all commands will operate only on curves that are visibile
# in the graph editor.
# 
#     ____________
# - -/__ Video __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# http://www.youtube.com/watch?v=fOeDwGbuHFE
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [curveSwap Current] : Creates a curveSwap for the selected range, or the surrounding keys, based on current frame.
# [curveSwap Average] : Creates a curveSwap for the selected range, or the surrounding keys, based on average of keys.
# [<< Previous] : Matches selected key or current frame to the previous keyframe value.
# [Next >>] : Matches selected key or current frame to the next keyframe value.
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

import maya.cmds as mc
import maya.mel as mm
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
    user interface for ml_curveSwap
    '''

    with utl.MlUi('ml_curveSwap', 'curveSwap Keys', width=400, height=150, info='''Press Next and Previous to match keys to the next or previous keyframes.
Press Current or Average to turn a frame range into a curveSwap.''') as win:

        #mc.paneLayout(configuration='vertical2',separatorThickness=1)
        #mc.columnLayout(adj=True)
        win.buttonWithPopup(label='x <> y', command=partial(swap, True,  True,  False))
        win.buttonWithPopup(label='x <> z', command=partial(swap, True,  False, True))
        win.buttonWithPopup(label='y <> z', command=partial(swap, False, True,  True))
        
        win.buttonWithPopup(label='flip x', command=previous, annotation='Matches selected key or current frame to the previous keyframe value.', shelfLabel='<_', shelfIcon='defaultTwoStackedLayout')
        win.buttonWithPopup(label='flip y', command=next, annotation='Matches selected key or current frame to the next keyframe value.', shelfLabel='_>', shelfIcon='defaultTwoStackedLayout')
        win.buttonWithPopup(label='flip z', command=next, annotation='Matches selected key or current frame to the next keyframe value.', shelfLabel='_>', shelfIcon='defaultTwoStackedLayout')
        
        
        #mc.setParent('..')

def swap(x=False, y=False, z=False):
    '''Swap rotation values between two selected axes on the current selection.'''
    axes = []
    if x:
        axes.append('rx')
    if y:
        axes.append('ry')
    if z:
        axes.append('rz')
    if len(axes) != 2:
        OpenMaya.MGlobal.displayWarning('Select exactly two axes to swap.')
        return

    sel = mc.ls(sl=True)
    if not sel:
        OpenMaya.MGlobal.displayWarning('Nothing selected.')
        return

    attr_a, attr_b = axes[0], axes[1]
    with utl.UndoChunk():
        for node in sel:
            plug_a = f'{node}.{attr_a}'
            plug_b = f'{node}.{attr_b}'
            val_a = mc.getAttr(plug_a)
            val_b = mc.getAttr(plug_b)
            mc.setAttr(plug_a, val_b)
            mc.setAttr(plug_b, val_a)
            if mc.keyframe(plug_a, query=True, keyframeCount=True):
                mc.setKeyframe(plug_a)
            if mc.keyframe(plug_b, query=True, keyframeCount=True):
                mc.setKeyframe(plug_b)


def swapFrame(next=False, previous=False):
    '''Match keys to the next or previous keyframe value on visible curves.'''
    if (next and previous) or (not next and not previous):
        OpenMaya.MGlobal.displayWarning('This function requires exactly one argument to be true.')
        return

    sel = mc.ls(sl=True)
    if not sel:
        OpenMaya.MGlobal.displayWarning('Nothing selected.')
        return

    currentTime = mc.currentTime(query=True)
    keySel = utl.KeySelection()
    if not (keySel.selectedKeys() or keySel.visibleInGraphEditor() or keySel.keyedChannels()):
        keySel.setKeyframe()

    with utl.UndoChunk():
        selected = mc.keyframe(query=True, name=True, selected=True)
        for curve in keySel.curves:
            start = currentTime
            end = currentTime
            findFrom = currentTime
            value = None
            if selected and curve in selected:
                keyTimes = mc.keyframe(curve, query=True, timeChange=True, selected=True)
                if keyTimes:
                    if next:
                        start = keyTimes[0]
                        findFrom = keyTimes[-1]
                    elif previous:
                        end = keyTimes[-1]
                        findFrom = keyTimes[0]
            if next:
                end = mc.findKeyframe(curve, time=(findFrom,), which='next')
                value = mc.keyframe(curve, time=(end,), query=True, valueChange=True)[0]
            elif previous:
                start = mc.findKeyframe(curve, time=(findFrom,), which='previous')
                value = mc.keyframe(curve, time=(start,), query=True, valueChange=True)[0]
            if start != end:
                if (end - start) > 1:
                    mc.cutKey(curve, time=(start + 0.1, end - 0.1))
                mc.keyframe(curve, time=(start, end), edit=True, valueChange=value)


def next(*args):
    '''Match selected key or current frame to the next keyframe value.'''
    swapFrame(next=True)


def previous(*args):
    '''Match selected key or current frame to the previous keyframe value.'''
    swapFrame(previous=True)