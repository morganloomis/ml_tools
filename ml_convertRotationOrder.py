# -= ml_convertRotationOrder.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 5
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_convertRotationOrder.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_convertRotationOrder
#     ml_convertRotationOrder.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Change the rotation order of an object while preserving animation. When you
# want to change the rotation order of a control after you've already animated, or
# don't want to alter the pose of an object.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI. Select the objects with rotation orders you want to change, and
# press the button for the desired rotation order.
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
__revision__ = 5


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

ROTATE_ORDERS = ['xyz', 'yzx','zxy','xzy','yxz','zyx']
_BUTTON = dict()

def ui():
    '''
    User interface for convert rotation order
    '''

    with utl.MlUi('ml_convertRotationOrder', 'Convert Rotation Order', width=400, height=140, info='''Select objects to convert and press button for desired rotation order.
Use the "Get Tips" button to see suggestions for a single object on the current frame.''') as win:


        mc.button(label='Get tips for selection', command=loadTips, annotation='')
        mc.scrollField('ml_convertRotationOrder_nodeInfo_scrollField', editable=False, wordWrap=True, height=60)

        mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,100), (2,400)], columnAttach=[2,'both',1])
        for each in ROTATE_ORDERS:
            _BUTTON[each] = win.buttonWithPopup(label=each, command=globals()[each], annotation='Convert selected object rotate order to '+each+'.', shelfLabel=each)
            mc.textField('ml_convertRotationOrder_'+each+'_textField', editable=False)

    resetTips()



def loadTips(*args):

    sel = mc.ls(sl=True)

    if not len(sel) == 1:
        OpenMaya.MGlobal.displayWarning('Please select a single object.')
        return

    resetTips()

    ro = ROTATE_ORDERS[mc.getAttr(sel[0]+'.rotateOrder')]

    nodeName = mc.ls(sl=True, shortNames=True)[0]

    infoText = 'This object is '
    tol = gimbalTolerence(sel[0])
    if tol < 0.1:
        infoText += 'not currently gimballing'
    else:
        if tol < 0.5:
            infoText += 'only '
        infoText += str(int(tol*100))
        infoText+='% gimballed'


    #test all rotation orders and find the lowest value
    rotOrderTests = testAllRotateOrdersForGimbal(sel[0])
    lowest = sorted(rotOrderTests)[0]
    #find the lower of the two worldspace options
    lowestWS = 1
    for each in rotOrderTests[2:4]:
        if each < lowestWS:
            lowestWS = each

    #determine if it's a worldspace control
    ws = isWorldSpaceControl(sel[0])
    if ws:
        infoText += ", and it looks like it's a worldspace control."
    else:
        infoText+='.'

    for t, r in zip(rotOrderTests, ROTATE_ORDERS):
        if r == ro:
            continue

        text = str(int(t*100)) + '% Gimballed. '

        if ws:
            if r.endswith('y') and t == lowestWS: #lowest worldspace option is reccomended
                text += '<-- [RECOMMENDED]'
            elif lowest<lowestWS and t==lowest: #if there's a lower non-worldspace option, reccomend that also
                text += '<-- [NON-WORLDSPACE RECOMMENDATION]'
        else:
            if t == lowest: #lowest test value is reccomended.
                text += '<-- [RECOMMENDED]'
            elif lowest<lowestWS and t==lowestWS and t < 0.3: #if there's a
                text += '<-- [RECOMMENDED FOR WORLDSPACE CONTROLS]'

        mc.textField('ml_convertRotationOrder_'+r+'_textField', edit=True, text=text)

    mc.button(_BUTTON[ro], edit=True, enable=False)
    mc.textField('ml_convertRotationOrder_'+ro+'_textField', edit=True, text='-- Current rotate order --')

    mc.scrollField('ml_convertRotationOrder_nodeInfo_scrollField', edit=True, text=infoText)

    mc.select(sel)


def resetTips():

    #clear the tips
    for each in ROTATE_ORDERS:
        mc.button(_BUTTON[each], edit=True, enable=True)
        mc.textField('ml_convertRotationOrder_'+each+'_textField', edit=True, text='')

    #set default tips
    mc.textField('ml_convertRotationOrder_xyz_textField', edit=True, text='Default Maya rotation order, for x-oriented joints.')
    mc.textField('ml_convertRotationOrder_zxy_textField', edit=True, text='Ideal for worldspace controls.')
    mc.textField('ml_convertRotationOrder_xzy_textField', edit=True, text='Ideal for worldspace controls.')


def testAllRotateOrdersForGimbal(obj):

    #duplicate node without children
    dup = mc.duplicate(obj, name='temp#', parentOnly=True)[0]

    tolerences = list()
    for roo in ROTATE_ORDERS:
        mc.xform(dup, preserve=True, rotateOrder=roo)
        tolerences.append(gimbalTolerence(dup))

    #delete node
    mc.delete(dup)

    return tolerences


def gimbalTolerence(obj):

    rotateOrder = ROTATE_ORDERS[mc.getAttr(obj+'.rotateOrder')]

    #get the value of the rotate order's central attribute
    midValue = mc.getAttr(obj+'.r'+rotateOrder[1])

    #as this number gets close to 1, we're getting close to gimbal
    gimbalTest = abs(((midValue+90) % 180) - 90) / 90

    return gimbalTest


def isWorldSpaceControl(obj):

    #first, if the object itself doesn't inherit transforms, it's a world space node.
    if not mc.getAttr(obj+'.inheritsTransform'):
        return True

    #walk up the hierarchy testing for any rotation value on x or z, or inherit transform
    parent = mc.listRelatives(obj, parent=True)
    while(parent):
        if not mc.getAttr(parent[0]+'.inheritsTransform'):
            return True
        for attr in ('.rx','.rz'):
            if mc.getAttr(parent[0]+attr) != 0:
                return False
        parent = mc.listRelatives(parent, parent=True)
    return True


def readUI(*args):
    pass

def xyz(*args):
    convertTo(roo='xyz')

def yzx(*args):
    convertTo(roo='yzx')

def zxy(*args):
    convertTo(roo='zxy')

def xzy(*args):
    convertTo(roo='xzy')

def yxz(*args):
    convertTo(roo='yxz')

def zyx(*args):
    convertTo(roo='zyx')


def convertTo(roo='zxy'):

    if not roo in ROTATE_ORDERS:
        OpenMaya.MGlobal.displayWarning('Not a proper rotation order: '+str(roo))
        return

    sel = mc.ls(sl=True)

    if not sel:
        OpenMaya.MGlobal.displayWarning('Please make a selection.')
        return


    time = mc.currentTime(query=True)

    #check that all rot channels have keys, or no keys
    keytimes = dict()
    prevRoo = dict()
    allKeytimes = list()
    keyedObjs = list()
    unkeyedObjs = list()

    for obj in sel:
        rotKeys = mc.keyframe(obj, attribute='rotate', query=True, timeChange=True)
        if rotKeys:
            keytimes[obj] = list(set(rotKeys))
            prevRoo[obj] = ROTATE_ORDERS[mc.getAttr(obj+'.rotateOrder')]
            allKeytimes.extend(rotKeys)
            keyedObjs.append(obj)
        else:
            unkeyedObjs.append(obj)

    with utl.UndoChunk():
        #change rotation order for keyed objects
        if keyedObjs:

            allKeytimes = list(set(allKeytimes))
            allKeytimes.sort()

            with utl.IsolateViews():
                #set keyframes first, so that frames that aren't keyed on all channels are
                for frame in allKeytimes:
                    mc.currentTime(frame, edit=True)
                    for obj in keyedObjs:
                        if frame in keytimes[obj]:
                            #set keyframe to make sure every channel has a key
                            mc.setKeyframe(obj, attribute='rotate')

                for frame in allKeytimes:
                    mc.currentTime(frame, edit=True)
                    for obj in keyedObjs:
                        if frame in keytimes[obj]:
                            #change the rotation order to the new value
                            mc.xform(obj, preserve=True, rotateOrder=roo)
                            #set a keyframe with the new rotation order
                            mc.setKeyframe(obj, attribute='rotate')
                            #change rotation order back without preserving, so that the next value is correct
                            mc.xform(obj, preserve=False, rotateOrder=prevRoo[obj])

                #reset current time while still isolated, for speed.
                mc.currentTime(time, edit=True)

                #set the final rotate order for keyed objects
                for each in keyedObjs:
                    mc.xform(each, preserve=False, rotateOrder=roo)
                    mc.filterCurve(each)

        #for unkeyed objects, rotation order just needs to be changed with xform
        if unkeyedObjs:
            for obj in unkeyedObjs:
                mc.xform(obj, preserve=True, rotateOrder=roo)

    #reset selection
    mc.select(sel)

if __name__ == '__main__': ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2011-10-08 : First publish.
#
# Revision 2: 2012-03-12 : Updated to work with non-keyed objects, added the tips button.
#
# Revision 3: 2012-08-04 : Fixing bug with potential duplicate temp name.
#
# Revision 4: 2014-03-01 : adding category
#
# Revision 5: 2018-02-17 : Updating license to MIT.