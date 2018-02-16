# -= ml_frameGraphEditor.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_frameGraphEditor.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_frameGraphEditor
#     ml_frameGraphEditor.main()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Frame the graph editor nicely based on the time slider range or the selected
# keys.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Alternately, if you want the result to be centered on the current time, use the
# command:   ml_frameGraphEditor.main(centerCurrentTime=True) For best results,
# assign this command to a hotkey. The main() function is a replacement for
# fitPanel -selected, so it can be used to replace the standard "f" hotkey. It
# frames the graph editor if the graph editor is in focus, otherwise it falls back
# to the default MEL framing command. If you want a command that just frames the
# graph editor and nothing else, use the frameGraphEditor() function.
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
import maya.mel as mm

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
#
# Revision 5: 2018-02-17 : Updating license to MIT.