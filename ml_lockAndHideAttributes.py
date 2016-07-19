# 
#   -= ml_lockAndHideAttributes.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 2, 2014-03-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_lockAndHideAttributes.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_lockAndHideAttributes
#     ml_lockAndHideAttributes.ui()
# From MEL, this looks like:
#     python("import ml_lockAndHideAttributes;ml_lockAndHideAttributes.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly set the locked and keyable state of attributes in the channel box. This tool
# is designed to be used as hotkeys for quickly locking and hiding attributes. It will operate
# on all visible attributes, unless specific channels are selected. When using to unhide attributes,
# it will unhide all standard transform attributes, and all user defined attributes.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, select channels in the channel box, and hit the appropriate button to
# lock, hide, unlock or unhide channels. Right click the buttons to create hotkeys
# or shelf buttons.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Lock] : Lock selected attributes.
# [Hide] : Hide selected attributes.
# [Lock and Hide] : Lock and hide selected attributes.
# [Unlock] : Unlock selected attributes.
# [Unhide] : Unhide all core attributes.
# [Unlock and Unhide] : Unlock and unhide selected attributes.
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'riggingScripts'
__revision__ = 2

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
