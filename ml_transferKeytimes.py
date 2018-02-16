# -= ml_transferKeytimes.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 2
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_transferKeytimes.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_transferKeytimes
#     ml_transferKeytimes.main()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copy keytimes from one node to another. Animation isn't fundamentally changed,
# but keys will be added or deleted.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select the source and destination nodes, keytimes will be transferred from
# first to second selection. Run the command.
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
__revision__ = 2

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

def main():

    sel = mc.ls(sl=True)

    if len(sel) < 2:
        OpenMaya.MGlobal.displayWarning('Select 2 or more objects.')
        return

    transferKeytimes(sel[0], sel[1:])
    mc.select(sel)


def transferKeytimes(source, destinations):

    if not isinstance(destinations, (list, tuple)):
        destinations = [destinations]

    attributes = mc.listAttr(source, keyable=True, unlocked=True)

    keytimes = dict()
    start = None
    end = None

    for a in attributes:
        currKeytimes = mc.keyframe(source, attribute=a, query=True, timeChange=True)
        if not currKeytimes:
            continue

        if start == None or currKeytimes[0] < start:
            start = currKeytimes[0]

        if end == None or currKeytimes[-1] > end:
            end = currKeytimes[-1]

        keytimes[a] = currKeytimes
        #allKeyTimes.extend(currKeytimes)

    if not keytimes:
        return

    with utl.IsolateViews():
        mc.bakeResults(destinations, time=(start,end), sampleBy=1, preserveOutsideKeys=True, simulation=True)

        #euler filter
        mc.filterCurve(mc.listConnections(destinations,type='animCurve'))

        #go through all keys and delete
        for k in keytimes:
            for f in range(int(start), int(end)):
                if not f in keytimes[k]:
                    mc.cutKey(destinations, attribute=k, time=(f,))


if __name__ == '__main__': main()


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2014-03-02 : First publish.
#
# Revision 2: 2018-02-17 : Updating license to MIT.