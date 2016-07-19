# 
#   -= ml_tangentWeight.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 3, 2016-05-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_tangentWeight.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_tangentWeight
#     ml_tangentWeight.ui()
# From MEL, this looks like:
#     python("import ml_tangentWeight;ml_tangentWeight.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Scale keyframe tangents up or down incrementally without changing their angle.
# The result is basically increasing or decreasing the influence of a keyframe on the animCurve.
# Can also weight tangents toward the left or right, which increases influence
# on one side of the keyframe while reducing it on the other.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select Keyframes to affect, and press the desired button. To further affect the
# tangents, continue pressing the button to increment the weight until the desired
# weight is attained. This works well as a hotkey.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [-] : Scale tangent down.
# [+] : Scale tangent up.
# [<] : Weight tangent toward the left.
# [>] : Weight tangent toward the right.
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
__revision__ = 3

import maya.cmds as mc
from maya import OpenMaya

try:
    import ml_utilities as utl
    utl.upToDateCheck(17)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
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

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-03-25 : First publish.
#
# Revision 2: 2016-03-27 : Fixed command name typo
#
# Revision 3: 2016-05-01 : fixed error when nothing is selected.
