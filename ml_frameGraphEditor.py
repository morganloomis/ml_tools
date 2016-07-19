# 
#   -= ml_frameGraphEditor.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 4, 2016-05-10
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_frameGraphEditor.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_frameGraphEditor
#     ml_frameGraphEditor.main()
# From MEL, this looks like:
#     python("import ml_frameGraphEditor;ml_frameGraphEditor.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Frame the graph editor nicely based on the time slider range or the selected keys.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Alternately, if you want the result to be centered on the current time, use the command:
#     ml_frameGraphEditor.main(centerCurrentTime=True)
# For best results, assign this command to a hotkey. The main() function is a replacement for
# fitPanel -selected, so it can be used to replace the standard "f" hotkey. It frames the graph
# editor if the graph editor is in focus, otherwise it falls back to the default MEL framing command.
# If you want a command that just frames the graph editor and nothing else, use the frameGraphEditor() function.
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
__revision__ = 4

import maya.cmds as mc
import maya.mel as mm

try:
    import ml_utilities as utl
    utl.upToDateCheck(18)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
hotkey = {'f':'main()'}


def main(centerCurrentTime=False):
    '''
    Replacement command for "fitPanel -selected"
    If graph editor has focus, run frameGraphEditor, otherwise default to fitPanel -selected mel command.
    '''
    if not frameGraphEditor(centerCurrentTime=centerCurrentTime):
        mm.eval("fitPanel -selected") 


def frameGraphEditor(centerCurrentTime=False):
    '''
    If graph editor has focus, frame the selected or visible animation curves.
    '''
    
    panel = mc.getPanel(up=True)
    if not panel:
        panel = mc.getPanel(withFocus=True)
    if not panel:
        return False
    panelType = mc.getPanel(to=panel)
    if panelType != 'scriptedPanel':
        return False
    scriptedType = mc.scriptedPanel(panel, query=True, type=True)
    if scriptedType != 'graphEditor':
        return False
    
    graphEditor = panel+'GraphEd'
    
    keySel = utl.KeySelection()
    if keySel.selectedKeys():
        pass
    elif keySel.visibleInGraphEditor():
        pass
    
    if keySel.selected:
        times = keySel.getSortedKeyTimes()
        start = times[0]
        end = times[-1]
    else:
        keySel.frameRange()
        start = keySel._timeRangeStart
        end = keySel._timeRangeEnd
    
    values = sorted(keySel.keyframe(query=True, valueChange=True))
    minValue = values[0]
    maxValue = values[-1]
    
    if start == end:
        start = start-1
        end = end+1  
        
    if maxValue == minValue:
        minValue = minValue-0.5
        maxValue = maxValue+0.5
    
    #add a 10% padding 
    timePadding = (end-start)/10.0
    valuePadding = (maxValue-minValue)/10.0
    
    mc.animView(graphEditor, startTime=start-timePadding, endTime=end+timePadding, minValue=minValue-valuePadding, maxValue=maxValue+valuePadding)
    
    if centerCurrentTime:
        mc.animCurveEditor(graphEditor, edit=True, lookAt='currentTime')
    
    return True   


if __name__ == '__main__':
    main()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-05-07 : First publish.
#
# Revision 2: 2016-05-08 : Frame values correctly for given frame range, option to center on current time.
#
# Revision 3: 2016-05-09 : Updated to support graph editor visibility, now requires ml_utilities.
#
# Revision 4: 2016-05-10 : Wrapping fitPanel, updating header info.
