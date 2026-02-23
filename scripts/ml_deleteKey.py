# -= ml_deleteKey.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 9
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_deleteKey.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_deleteKey
#     ml_deleteKey.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# A more robust tool for deleting keyframes in Maya, including deleting keys on
# the current frame and which are visible in the graph editor. Alternately, delete
# selected channels.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool, select the options, and press the Delete Key button. Set the
# options and right click the button to create a hotkey or shelf button. If
# selected keys is unchecked, it will delete keys on the current frame regardless
# of key selection. Delete sub-frames will include keys which fall within half a
# frame of the current time. The second button operates on entire channels, and it
# will delete the channels that are selected, or all the channels on an object.
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [] Selected Keys : Delete the keys selected in the graph editor.
# [] Selected Channels : Delete all the keys on selected channels. (Unless overridden above)
# [] Visible in Graph Editor : Only delete keys that are visible in the graph editor. (Unless overridden above)
# [] Current Frame : Delete the keys on the current frame. (Unless overridden above)
# [] Delete Sub-Frames : Delete sub-frame keys surrounding the current frame.
# [Delete Keys] : Delete Keyframe.
# [Delete Channels] : Delete selected channels, or all keys on selected nodes.
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
__revision__ = 9
__category__ = 'animation'

hotkey = {'d':'deleteKey(selectedKeys=True, deleteSubFrames=True, visibleInGraphEditor=True)'}

shelfButton = {'annotation': 'Click to delete selected keys, double click to delete selected channels. Right click for more options.',
               'command': 'import ml_deleteKey;ml_deleteKey.deleteKey(deleteSubFrames=True, visibleInGraphEditor=True, selectedKeys=True)',
               'doubleClickCommand': 'import ml_deleteKey;ml_deleteKey.deleteChannels()',
               'imageOverlayLabel': 'del',
               'menuItem': [['Delete Key UI', 'import ml_deleteKey;ml_deleteKey.ui()'],
                            ['Delete Selected Channels', 'import ml_deleteKey;ml_deleteKey.deleteChannels()']],
               'order': 6}

import maya.cmds as mc
import maya.mel as mm
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
    User interface for ml_deleteKey
    '''

    with utl.MlUi('ml_deleteKey', 'deleteKey', width=400, height=220, info='''Press Delete Key to delete keyframes using the selected settings.
Right click the button to create a hotkey or shelf button with the current settings.
Options are evaluated in top to bottom order.''') as win:

        mc.checkBoxGrp('ml_deleteKey_selectedKey_checkBox', label='Selected Keys', annotation='Delete the keys selected in the graph editor.')
        #mc.checkBoxGrp('ml_deleteKey_chanBox_checkBox', label='Selected Channels', annotation='Delete all the keys on selected channels. (Unless overridden above)')
        mc.checkBoxGrp('ml_deleteKey_graphVis_checkBox', label='Visible in Graph Editor', annotation='Only delete keys that are visible in the graph editor. (Unless overridden above)')
        #mc.checkBoxGrp('ml_deleteKey_currentFrame_checkBox', label='Current Frame', annotation='Delete the keys on the current frame. (Unless overridden above)')

        mc.checkBoxGrp('ml_deleteKey_subFrames_checkBox', label='Delete Sub-Frames', annotation='Delete sub-frame keys surrounding the current frame.')

        win.ButtonWithPopup(label='Delete Keys', name=win.name, command=deleteKey, annotation='Delete Keyframe.',
            readUI_toArgs={
                #'selectedChannels':'ml_deleteKey_chanBox_checkBox',
                'visibleInGraphEditor':'ml_deleteKey_graphVis_checkBox',
                'selectedKeys':'ml_deleteKey_selectedKey_checkBox',
                'deleteSubFrames':'ml_deleteKey_subFrames_checkBox',
                #'currentFrame':'ml_deleteKey_currentFrame_checkBox',
                })

        win.ButtonWithPopup(label='Delete Channels', name=win.name, command=deleteChannels, annotation='Delete selected channels, or all keys on selected nodes.')


def deleteKey(deleteSubFrames=False, selectedKeys=False, selectedChannels=False, visibleInGraphEditor=False, currentFrame=False):
    '''
    The main function arguments:

        selectedKeys:           Delete the keys selected in the graph editor
        selectedChannels:       Delete all the keys on selected channels
        visibleInGraphEditor:   Only delete keys that are visible in the graph editor
        currentFrame:           Delete the keys on the current frame
        deleteSubFrames:        Delete sub-frame keys surrounding the current frame
    '''

    if selectedChannels:
        print('selectedChannels flag is deprecated, please use the deleteChannels() function instead')

    keySel = utl.KeySelection()

    if selectedKeys and keySel.selectedKeys():
        pass
    elif visibleInGraphEditor and keySel.visibleInGraphEditor():
        keySel.currentFrame()
    elif keySel.selectedObjects():
        keySel.currentFrame()

    if not keySel.curves:
        return

    keySel.cutKey(includeSubFrames=deleteSubFrames)


def deleteChannels():
    '''
    Deletes selected channels, otherwise all keys on the selected objects.
    '''

    keySel = utl.KeySelection()

    if keySel.selectedChannels():
        pass
    elif keySel.visibleInGraphEditor():
        pass
    elif keySel.selectedObjects():
        pass

    if not keySel.initialized:
        return

    keySel.cutKey()


if __name__ == '__main__': ui()

