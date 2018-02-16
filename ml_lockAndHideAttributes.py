# -= ml_lockAndHideAttributes.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 3
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_lockAndHideAttributes.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_lockAndHideAttributes
#     ml_lockAndHideAttributes.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly set the locked and keyable state of attributes in the channel box. This
# tool is designed to be used as hotkeys for quickly locking and hiding
# attributes. It will operate on all visible attributes, unless specific channels
# are selected. When using to unhide attributes, it will unhide all standard
# transform attributes, and all user defined attributes.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, select channels in the channel box, and hit the appropriate button
# to lock, hide, unlock or unhide channels. Right click the buttons to create
# hotkeys or shelf buttons.
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Lock] : Lock selected attributes.
# [Hide] : Hide selected attributes.
# [Lock and Hide] : Lock and hide selected attributes.
# [Unlock] : Unlock selected attributes.
# [Unhide] : Unhide all core attributes.
# [Unlock and Unhide] : Unlock and unhide selected attributes.
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
__revision__ = 3

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
    User interface for ml_lockAndHideAttributes
    '''

    with utl.MlUi('ml_lockAndHideAttributes', 'Lock and Hide', width=400, height=140, info='''Select channels in the channel box to be locked or hidden.
then hit the appropriate button.''') as win:

        form = mc.formLayout()
        b11 = win.buttonWithPopup(label='Lock', command=lock, annotation='Lock selected attributes.')
        b12 = win.buttonWithPopup(label='Hide', command=hide, annotation='Hide selected attributes.')
        b13 = win.buttonWithPopup(label='Lock and Hide', command=lockAndHide, annotation='Lock and hide selected attributes.')
        b21 = win.buttonWithPopup(label='Unlock', command=unlock, annotation='Unlock selected attributes.')
        b22 = win.buttonWithPopup(label='Unhide', command=unhide, annotation='Unhide all core attributes.')
        b23 = win.buttonWithPopup(label='Unlock and Unhide', command=unlockAndUnhide, annotation='Unlock and unhide selected attributes.')

        utl.formLayoutGrid(form, (
            (b11,b21),
            (b12,b22),
            (b13,b23)
            ))


def lock(*args):
    setAttributeState(lock=True)


def hide(*args):
    setAttributeState(hide=True)


def unlock(*args):
    setAttributeState(lock=False)


def unhide(*args):
    setAttributeState(hide=False)


def lockAndHide(*args):
    setAttributeState(lock=True, hide=True)


def unlockAndUnhide(*args):
    setAttributeState(lock=False, hide=False)


def setAttributeState(lock=None, hide=None):

    sel = mc.ls(sl=True)
    if not sel:
        OpenMaya.MGlobal.displayWarning('Please make a selection.')
        return

    channels = utl.getSelectedChannels()
    doAll = not bool(channels)

    kwargs = dict()

    for obj in sel:
        attrs = channels[:]
        #we unhide first, so hidden attributes can get unlocked.
        if hide is False and doAll:
            attrs = ['tx','ty','tz','rx','ry','rz','sx','sy','sz','v']
            ud = mc.listAttr(obj, userDefined=True)
            if ud:
                attrs+=ud

        elif doAll:
            attrs = mc.listAttr(obj, keyable=True)

        if lock is not None:
            kwargs['lock'] = lock
        if hide is not None:
            kwargs['keyable'] = not hide

        if attrs:
            for attr in attrs:
                try:
                    mc.setAttr(obj+'.'+attr, **kwargs)
                except StandardError: pass

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2011-10-08 : First publish.
#
# Revision 2: 2014-03-01 : adding category
#
# Revision 3: 2018-02-17 : Updating license to MIT.