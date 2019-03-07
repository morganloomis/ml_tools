# -= ml_ballisticAnimation.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_ballisticAnimation.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_ballisticAnimation
#     ml_ballisticAnimation.main()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Runs very simple gravity physics on the translation of an object, taking into
# account initial velocity.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Simply select a static or animated object, highlight or set your frame range,
# and run the script. If your object is already animated, the initial velocity
# will be calculated based on the position one frame before the frirst frame of
# the frame range.
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
__revision__ = 2
__category__ = 'animation'


import maya.cmds as mc
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

    if not sel:
        raise RuntimeError('Please select an object.')

    if [x for x in sel if not mc.attributeQuery('translate', exists=True, node=x)]:
        raise RuntimeError('Only works on transform nodes, please adjust your selection.')

    frameRate = utl.getFrameRate()
    timeFactor = 1.0/frameRate

    unit = mc.currentUnit(query=True, linear=True)

    #default is meters
    distFactor = 1

    if unit == 'mm':
        distFactor = 1000
    elif unit == 'cm':
        distFactor = 100
    elif unit == 'km':
        distFactor = 0.001
    elif unit == 'in':
        distFactor = 39.3701
    elif unit == 'ft':
        distFactor = 3.28084
    elif unit == 'yd':
        distFactor = 1.09361
    elif unit == 'mi':
        distFactor = 0.000621371

    g = 9.8 * distFactor

    start, end = utl.frameRange()
    start = int(start)
    end = int(end)

    mc.currentTime(start)

    for each in sel:

        mc.setKeyframe(each+'.translate')
        startTrans = mc.getAttr(each+'.translate')[0]
        prevTrans = [mc.keyframe(each, query=True, attribute=x, eval=True, time=(start-1,))[0] for x in ('tx','ty','tz')]

        xInit = startTrans[0]-prevTrans[0]
        yInit = startTrans[1]-prevTrans[1]
        zInit = startTrans[2]-prevTrans[2]

        mc.cutKey(each, attribute='translate', time=(start+0.1,end+0.5))
        mc.setKeyframe(each, attribute='translateX', time=start+1, value=startTrans[0]+xInit)
        mc.setKeyframe(each, attribute='translateZ', time=start+1, value=startTrans[2]+zInit)
        mc.setKeyframe(each, attribute='translateX', time=end-1, value=startTrans[0]+(xInit*(end-start-1)))
        mc.setKeyframe(each, attribute='translateZ', time=end-1, value=startTrans[2]+(zInit*(end-start-1)))
        mc.setKeyframe(each, attribute='translateX', time=end, value=startTrans[0]+(xInit*(end-start)))
        mc.setKeyframe(each, attribute='translateZ', time=end, value=startTrans[2]+(zInit*(end-start)))

        for i,f in enumerate(range(start,end+1)):
            t = i * timeFactor
            y = startTrans[1] + (i * yInit) - (g * t * t)/2

            mc.setKeyframe(each, attribute='translateY', time=f, value=y)


if __name__ == '__main__':
    main()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-10-01 : First publish.
#
# Revision 2: 2018-02-17 : Updating license to MIT.