# -= ml_resetChannels.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 11
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_resetChannels.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_resetChannels
#     ml_resetChannels.main()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Set the selected channels in the channel box to their default values. If no
# channels are selected, resets all keyable channels.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select channels in the channel box, and run the command directly, as a hotkey
# or shelf button. Run command line to use the transformsOnly flag, in order to
# only reset transform attributes. The excludeChannels argument takes a list of
# channel names to exclude. The resetPuppetControl() command is a wrapper for
# resetting puppeteer controls by skipping certain settings attributes.
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
__revision__ = 11
__category__ = 'animation'

shelfButton = {'annotation': 'Reset the selected nodes or channels to their default values.',
               'command': 'import ml_resetChannels;ml_resetChannels.resetPuppetControl()',
               'imageOverlayLabel': 'reset',
               'menuItem': [['Reset Transforms Only','import ml_resetChannels;ml_resetChannels.main(transformsOnly=True)']],
               'order': 4}

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

def main(selectedChannels=True, transformsOnly=False, excludeChannels=None):
    '''
    Resets selected channels in the channel box to default, or if nothing's
    selected, resets all keyable channels to default.
    '''
    gChannelBoxName = mm.eval('$temp=$gChannelBoxName')

    sel = mc.ls(sl=True)
    if not sel:
        return

    if excludeChannels and not isinstance(excludeChannels, (list, tuple)):
        excludeChannels = [excludeChannels]

    chans = None
    if selectedChannels:
        chans = mc.channelBox(gChannelBoxName, query=True, sma=True)

    testList = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ',
                'tx','ty','yz','rx','ry','rz','sx','sy','sz']
    for obj in sel:
        attrs = chans
        if not chans:
            attrs = mc.listAttr(obj, keyable=True, unlocked=True)
            if excludeChannels:
                attrs = [x for x in attrs if x not in excludeChannels]
        if transformsOnly:
            attrs = [x for x in attrs if x in testList]
        if attrs:
            for attr in attrs:
                try:
                    default = mc.attributeQuery(attr, listDefault=True, node=obj)[0]
                    mc.setAttr(obj+'.'+attr, default)
                except StandardError:
                    pass

    utl.deselectChannels()


def resetPuppetControl(*args):
    main(excludeChannels=['rotateOrder', 'pivotPosition', 'spaceSwitch'])


if __name__ == '__main__':
    resetPuppetControl()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 5: 2012-05-27 : Added revision notes, updated to use ml_utilities, changed primary function to main() for consistency
#
# Revision 6: 2013-04-23 : added transformsOnly and selected flags to support cgMonks
#
# Revision 7: 2014-03-01 : adding category
#
# Revision 8: 2015-05-14 : Added excludeChannels argument.
#
# Revision 9: 2015-05-16 : argument update in order to be supported in puppet context menu.
#
# Revision 10: 2018-02-17 : Updating license to MIT.
#
# Revision 11: 2018-05-13 : shelf support