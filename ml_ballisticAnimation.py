# 
#   -= ml_ballisticAnimation.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 1, 2016-10-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_ballisticAnimation.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_ballisticAnimation
#     ml_ballisticAnimation.main()
# From MEL, this looks like:
#     python("import ml_ballisticAnimation;ml_ballisticAnimation.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Runs very simple gravity physics on the translation of an object, taking into account 
# initial velocity.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Simply select a static or animated object, highlight or set your frame range, and run the script.
# If your object is already animated, the initial velocity will be calculated based
# on the position one frame before the frirst frame of the frame range.
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
try:
    import ml_utilities as utl
    utl.upToDateCheck(22)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    

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
