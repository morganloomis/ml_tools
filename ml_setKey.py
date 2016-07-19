# 
#   -= ml_setKey.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 9, 2014-03-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_setKey.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_setKey
#     ml_setKey.ui()
# From MEL, this looks like:
#     python("import ml_setKey;ml_setKey.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This is a more robust tool for setting keyframes in Maya, including
# setting keys on selected channels, keyed channels, and several other options.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool, select the options, and press the Set Key button.
# Alternately, set the options and press the "Create Hotkey" button to
# turn the current functionality into a hotkey.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [] Selected Channels : Only key channels that are selected in the Channel Box
# [] Visible in Graph Editor : Only key curves visible in Graph Editor
# [] Key Only Keyed Channels : Only set keys on channels that are already keyed
# [] Delete Sub-Frames : Delete sub-frame keys surrounding the current frame
# [] Insert Key : Insert key (preserve tangents)
# [] Key Shapes : Set keyframes on shapes
# [Set Key] : Set a keyframe.
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
__revision__ = 9

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya

try:
    import ml_utilities as utl
    utl.upToDateCheck(9)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
hotkey = {'S':'setKey(deleteSubFrames=True, insert=True, selectedChannels=True, visibleInGraphEditor=True, keyKeyed=True, keyShapes=True)'}


def ui():
    '''
    User interface for ml_setKey
    '''

    with utl.MlUi('ml_setKey', 'SetKey', width=400, height=220, info='''Press Set Key to set a keyframe with the current checkbox settings.
Right click the button to create a hotkey or shelf button 
with the currently selected settings.''') as win:
    
        mc.checkBoxGrp('ml_setKey_chanBox_checkBox', label='Selected Channels', annotation='Only key channels that are selected in the Channel Box')
        mc.checkBoxGrp('ml_setKey_graphVis_checkBox', label='Visible in Graph Editor', annotation='Only key curves visible in Graph Editor')
        mc.checkBoxGrp('ml_setKey_keyKeyed_checkBox', label='Key Only Keyed Channels', annotation='Only set keys on channels that are already keyed')
        mc.checkBoxGrp('ml_setKey_subFrames_checkBox', label='Delete Sub-Frames', annotation='Delete sub-frame keys surrounding the current frame')
        mc.checkBoxGrp('ml_setKey_insert_checkBox', label='Insert Key', annotation='Insert key (preserve tangents)')
        mc.checkBoxGrp('ml_setKey_shapes_checkBox', label='Key Shapes', annotation='Set keyframes on shapes')

        win.ButtonWithPopup(label='Set Key', name=win.name, command=setKey, annotation='Set a keyframe.', 
            readUI_toArgs={
                'selectedChannels':'ml_setKey_chanBox_checkBox',
                'visibleInGraphEditor':'ml_setKey_graphVis_checkBox',
                'keyKeyed':'ml_setKey_keyKeyed_checkBox',
                'deleteSubFrames':'ml_setKey_subFrames_checkBox',
                'insert':'ml_setKey_insert_checkBox',
                'keyShapes':'ml_setKey_shapes_checkBox',
                })


def setKey(deleteSubFrames=False, insert=False, selectedChannels=False, visibleInGraphEditor=False, keyKeyed=False, keyShapes=False):
    '''
    The main function arguments:
    
        deleteSubFrames:        Delete sub-frame keys surrounding the current frame
        insert:                 Insert key (preserve tangents)
        selectedChannels:       Only key channels that are selected in the Channel Box
        visibleInGraphEditor:   Only key curves visible in Graph Editor
        keyKeyed:               Only set keys on channels that are already keyed
        keyShapes:              Set keyframes on shapes as well as transforms
    '''
    
    keySel = utl.KeySelection()
    
    if selectedChannels and keySel.selectedChannels():
        pass
    elif visibleInGraphEditor and keySel.visibleInGraphEditor():
        pass
    elif keyKeyed and keySel.keyedChannels(includeShapes=keyShapes):
        pass
    else:
        keySel.selectedObjects()
    
    if not keySel.initialized:
        return

    #if the user has middle-mouse dragged, we don't want to insert
    #test this by comparing the current attribute value with the evaluated animation curve
    if keySel.curves and insert:
        #pretty sure curve and channel are linked properly, but this might be an issue.
        for curve, chan in zip(keySel.curves,keySel.channels):
            #chan = utl.getChannelFromAnimCurve(each)
            curveValue = mc.keyframe(curve, query=True, eval=True)
            if not curveValue:
                insert=False
                break
            if round(mc.getAttr(chan),3) != round(curveValue[0],3):
                insert=False
                break
                    
    #set the actual keyframe
    keySel.setKeyframe(insert=insert, shape=keyShapes, deleteSubFrames=deleteSubFrames)

         
if __name__ == '__main__': ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 4: 2012-03-11 : Added revision notes, updated to use ml_utilities, fixed a bug where tangents weren't being preserved, and fixed middle-mouse dragging.
#
# Revision 5: 2012-03-26 : Updated delete sub-frame option to work with other frame rates
#
# Revision 6: 2012-07-23 : Bug fixes.
#
# Revision 7: 2012-08-07 : Updating in parallel with ml_utilities to fix bug with keying keyed shapes.
#
# Revision 8: 2012-11-19 : updating to new KeySelection
#
# Revision 9: 2014-03-01 : adding category
