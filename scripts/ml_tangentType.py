# -= ml_tangentType.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 1
#   / / / / / / /  2019-10-10
#  /_/ /_/ /_/_/  _________
#               /_________/
# 
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copyright 2019 Morgan Loomis
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_tangentWeight.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_tangentType
#     ml_tangentType.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Scale keyframe tangents up or down incrementally without changing their angle.
# The result is basically increasing or decreasing the influence of a keyframe on
# the animCurve. Can also weight tangents toward the left or right, which
# increases influence on one side of the keyframe while reducing it on the other.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select Keyframes to affect, and press the desired button. To further affect the
# tangents, continue pressing the button to increment the weight until the desired
# weight is attained. This works well as a hotkey.
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [-] : Scale tangent down.
# [+] : Scale tangent up.
# [<] : Weight tangent toward the left.
# [>] : Weight tangent toward the right.
# 
#     ___________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
#     https://raw.githubusercontent.com/morganloomis/ml_tools/master/ml_utilities.py
# 
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -


shelfButton = {'annotation': 'Open a UI for setting keyframe tangent weight.',
               'menuItem': [['+ Plus', 'import ml_tangentWeight;ml_tangentWeight.plus()'],
                            ['- Minus', 'import ml_tangentWeight;ml_tangentWeight.minus()']],
               'order': 14}

import maya.cmds as mc
from maya import OpenMaya
import ml_utilities as utl

def ui():
    '''
    User interface for ml_tangentWeight
    '''

    with utl.MlUi('ml_tangentWeight', 'Weight Keyframe Tangents', width=400, height=140,
                  info='''Increase or decrease tangents length without affecting tangent angle.
Select keyframes and press buttons to weight their tangents.
If no keys are selected, the keys on the current frame will be affected.''') as win:

        form = mc.formLayout()
        b11 = win.buttonWithPopup(label='-', command=minus, annotation='Scale tangent down.')
        b12 = win.buttonWithPopup(label='+', command=plus, annotation='Scale tangent up.')
        b21 = win.buttonWithPopup(label='<', command=sharkFinLeft, annotation='Weight tangent toward the left.')
        b22 = win.buttonWithPopup(label='>', command=sharkFinRight, annotation='Weight tangent toward the right.')

        utl.formLayoutGrid(form, (
            (b11,b12),
            (b21,b22)
            ))



def tangentType(tangentType, deleteSubFrames=False, insert=False, selectedChannels=False, visibleInGraphEditor=False, keyKeyed=False, keyShapes=False):
    '''
    The main function arguments:

        selectedChannels:       Only key channels that are selected in the Channel Box
        visibleInGraphEditor:   Only key curves visible in Graph Editor
        keyKeyed:               Only set keys on channels that are already keyed
        keyShapes:              Set keyframes on shapes as well as transforms
    '''

    keySel = utl.KeySelection()

    if visibleInGraphEditor and keySel.visibleInGraphEditor():
        pass
    elif keyKeyed and keySel.keyedChannels(includeShapes=keyShapes):
        pass
    else:
        keySel.selectedObjects()

    if not keySel.initialized:
        return


    #set the actual keyframe
    keySel.setKeyframe(insert=insert, shape=keyShapes, deleteSubFrames=deleteSubFrames)


if __name__ == '__main__':ui()
