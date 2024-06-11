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

    sel = mc.ls(sl=True)

    a = 'rx' if x else 'ry'
    b = 'rz' if z else 'ry'

    for each in sel:
        a = mc.listConnections()