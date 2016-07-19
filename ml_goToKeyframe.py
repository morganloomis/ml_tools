# 
#   -= ml_goToKeyframe.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 3, 2014-03-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_goToKeyframe.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_goToKeyframe
#     ml_goToKeyframe.ui()
# From MEL, this looks like:
#     python("import ml_goToKeyframe;ml_goToKeyframe.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This is simply a more robust way to navigate to the next or previous keyframe.
# It recognizes only keys that are visible in the graph editor, and has options to
# only navigate through selected keys, and to round to the nearest
# whole frame, if you don't like editing on sub-frames. 
# Finally, it can look for keys in the whole hierarchy of the selected node,
# to help with keeping all a character's keys on the same frames.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, select next or previous to advance to the next or previous visible or
# selected key times. Right click the buttons to create hotkeys.
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
# Revision 3: 2014-03-01 : adding category
