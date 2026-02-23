# -= ml_tangentWeight.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_tangentWeight.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_tangentWeight
#     ml_tangentWeight.ui()
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

__author__ = 'Morgan Loomis'
__license__ = 'MIT'
__revision__ = 5
__category__ = 'animation'

shelfButton = {'annotation': 'Open a UI for setting keyframe tangent weight.',
               'menuItem': [['+ Plus', 'import ml_tangentWeight;ml_tangentWeight.plus()'],
                            ['- Minus', 'import ml_tangentWeight;ml_tangentWeight.minus()']],
               'order': 14}

import maya.cmds as mc
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

hotkey = {'-':'minus()','=':'plus()',';':'sharkFinLeft()',"'":'sharkFinRight()'}

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


def plus(*args):
    tangentScale(1.25)


def minus(*args):
    tangentScale(0.8)


def sharkFinLeft(*args):
    tangentScale(1.2,0.8333)


def sharkFinRight(*args):
    tangentScale(0.8333,1.2)


def tangentScale(value, outValue=None):

    if outValue == None:
        outValue = value

    curves = None

    #order of operations:
    #selected keys, visible in graph editor on current frame
    selected = False
    time = mc.currentTime(query=True)
    curves = mc.keyframe(query=True, name=True, selected=True)
    if curves:
        #try selected keys first
        selected = True
    else:
        #then visible in graph editor
        graphVis = mc.selectionConnection('graphEditor1FromOutliner', query=True, obj=True)
        if graphVis:
            curves = mc.keyframe(graphVis, query=True, name=True)
        else:
            #otherwise try keyed channels.
            sel = mc.ls(sl=True)
            if not sel:
                return
            curves = mc.listConnections(sel, s=True, d=False, type='animCurve')
            if not curves:
                return

    for curve in curves:

        keyTimes = list()

        #set tangents weighted if they aren't already
        if mc.keyTangent(curve, query=True, weightedTangents=True):
            mc.keyTangent(curve, edit=True, weightedTangents=True)

        if selected:
            keyTimes = mc.keyframe(curve, query=True, timeChange=True, selected=True)
        else:
            keyTimes = [time]

        for t in keyTimes:

            weight = mc.keyTangent(curve, time=(t,), query=True, inWeight=True, outWeight=True)
            if not weight:
                continue

            inOut = list()

            for w,v in zip(weight,[value,outValue]):
                if v<1 and w < 0.1:
                    inOut.append(0)
                elif v>1 and w == 0:
                    inOut.append(0.1)
                else:
                    inOut.append(w*v)

            mc.keyTangent(curve, time=(t,), edit=True, absolute=True, inWeight=inOut[0], outWeight=inOut[1])


if __name__ == '__main__':ui()

