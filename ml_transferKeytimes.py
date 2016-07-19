# 
#   -= ml_transferKeytimes.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 1, 2014-03-02
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_transferKeytimes.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_transferKeytimes
#     ml_transferKeytimes.main()
# From MEL, this looks like:
#     python("import ml_transferKeytimes;ml_transferKeytimes.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copy keytimes from one node to another. Animation isn't fundamentally changed, but keys
# will be added or deleted.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select the source and destination nodes, keytimes will be transferred 
# from first to second selection. Run the command.
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
__revision__ = 1

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
