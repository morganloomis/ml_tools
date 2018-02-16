# -= ml_goToKeyframe.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_goToKeyframe.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_goToKeyframe
#     ml_goToKeyframe.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# A more robust tool for navigating to the next or previous keyframe. It
# recognizes only keys that are visible in the graph editor, and has options to
# only navigate through selected keys, and to round to the nearest whole frame, if
# you don't like editing on sub-frames. Finally, it can look for keys in the whole
# hierarchy of the selected node, to help with keeping all a character's keys on
# the same frames.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, select next or previous to advance to the next or previous visible
# or selected key times. Right click the buttons to create hotkeys.
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

def ui():
    '''
    user interface for ml_goToKeyframe
    '''

    with utl.MlUi('ml_goToKeyframe', 'Go To Keyframe', width=400, height=130, info='''Press Next and Previous to advance time to the next or previous keyframes
within the graph editor or your selection.
Check Round to Nearest Frame to avoid stopping time on non-whole frames.''') as win:

        mc.checkBoxGrp('ml_goToKeyframe_selected_checkBox',
                       label='Within Selection',
                       annotation='Only search for next and previous within the selected keys.',
                       changeCommand=uiSetCheckBox)
        mc.checkBoxGrp('ml_goToKeyframe_selectKeys_checkBox',
                       label='Select Keys',
                       annotation='Select the keyframe(s) on the frame navigated to.',
                       changeCommand=uiSetCheckBox)
        mc.checkBoxGrp('ml_goToKeyframe_round_checkBox',
                       label='Round to Nearest Frame',
                       annotation='Only go to whole-number frames, even if keys are on sub-frames.')
        mc.checkBoxGrp('ml_goToKeyframe_hierarchy_checkBox',
                       label='Search Hierarchy',
                       annotation='Go to the next or previous keyframe in the whole hierarchy.')

        mc.paneLayout(configuration='vertical2', separatorThickness=1)

        win.ButtonWithPopup(label='<< Previous', name=win.name, command=previous,
                            annotation='Go to previous keyframe.',
                            readUI_toArgs={'roundFrame':'ml_goToKeyframe_round_checkBox',
                                           'selected':'ml_goToKeyframe_selected_checkBox',
                                           'selectKeys':'ml_goToKeyframe_selectKeys_checkBox',
                                           'searchHierarchy':'ml_goToKeyframe_hierarchy_checkBox'})

        win.ButtonWithPopup(label='Next >>', name=win.name, command=next,
                            annotation='Go to next keyframe.',
                            readUI_toArgs={'roundFrame':'ml_goToKeyframe_round_checkBox',
                                           'selected':'ml_goToKeyframe_selected_checkBox',
                                           'selectKeys':'ml_goToKeyframe_selectKeys_checkBox',
                                           'searchHierarchy':'ml_goToKeyframe_hierarchy_checkBox'})
        mc.setParent('..')


def uiSetCheckBox(*args):

    if mc.checkBoxGrp('ml_goToKeyframe_selected_checkBox', query=True, value1=True):
        mc.checkBoxGrp('ml_goToKeyframe_selectKeys_checkBox', edit=True, value1=False, enable=False)
    elif mc.checkBoxGrp('ml_goToKeyframe_selectKeys_checkBox', query=True, value1=True):
        mc.checkBoxGrp('ml_goToKeyframe_selected_checkBox', edit=True, value1=False, enable=False)
    else:
        mc.checkBoxGrp('ml_goToKeyframe_selectKeys_checkBox', edit=True, enable=True)
        mc.checkBoxGrp('ml_goToKeyframe_selected_checkBox', edit=True, enable=True)


def next(roundFrame=False, selected=False, searchHierarchy=False, selectKeys=False, *args):
    '''
    Wrapper for next args
    '''
    goToKeyframe(option='next', roundFrame=roundFrame, selected=selected, selectKeys=selectKeys, searchHierarchy=searchHierarchy)


def previous(roundFrame=False, selected=False, searchHierarchy=False, selectKeys=False, *args):
    '''
    Wrapper for previous args
    '''
    goToKeyframe(option='previous', roundFrame=roundFrame, selected=selected, selectKeys=selectKeys, searchHierarchy=searchHierarchy)


def goToKeyframe(option='next', roundFrame=False, selected=False, selectKeys=False, searchHierarchy=False):
    '''

    '''

    if option != 'next' and option != 'previous':
        OpenMaya.MGlobal.displayWarning('Option argument should be "next" or "previous"')
        return

    if selected and selectKeys:
        OpenMaya.MGlobal.displayWarning('Cannot use selectKeys flag in conjunction with selected flag.')
        selectKeys = False

    sel = mc.ls(sl=True)
    currentTime = mc.currentTime(query=True)
    time = currentTime

    if not sel:
        if option == 'next':
            time+=1
        elif option == 'previous':
            time-=1
        else:
            return
        #if nothing is selected, just go to the next or previous keyframe
        with utl.SkipUndo():
            mc.currentTime(time)
        return

    keySel = utl.KeySelection()

    if searchHierarchy:
        #if we're looking through the hierarchy,
        keySel.keyedInHierarchy()

    else:
        #create the keySelection object.
        #all the heavy lifting is done in ml_utilities.
        if selected and keySel.selectedKeys():
            pass
        if keySel.visibleInGraphEditor():
            pass
        if keySel.selectedObjects():
            pass

    time = keySel.findKeyframe(which=option, roundFrame=roundFrame, loop=True)

    if selectKeys:
        mc.selectKey(keySel.curves, time=(time,))


    #finally, set the time without adding to the undo queue
    with utl.SkipUndo():
        mc.currentTime(time, edit=True)


if __name__ == '__main__':
    ui()


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2012-07-23 : First publish.
#
# Revision 2: 2013-10-29 : Added hierarchy search, select keyframes, and a couple more options.
#
# Revision 3: 2014-03-01 : adding category.
#
# Revision 4: 2018-02-17 : Updating license to MIT.