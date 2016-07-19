# 
#   -= ml_toggleVisibility.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 1, 2015-05-14
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_toggleVisibility.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_toggleVisibility
#     ml_toggleVisibility.main()
# From MEL, this looks like:
#     python("import ml_toggleVisibility;ml_toggleVisibility.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Toggle the visibility of an object off and on, regardless of the attribute's
# locked or keyable state.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select an object, and run the script. If the object is visible, it will be 
# hidden, and vice-versa. 
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'animationScripts'
__revision__ = 1

import maya.cmds as mc

def main():
    
    sel = mc.ls(sl=True)
    
    if not sel:
        return
    
    for each in sel:
        plug = each+'.v'
        try:
            locked = mc.getAttr(plug, lock=True)
            if locked:
                mc.setAttr(plug, lock=False)
            
            if mc.getAttr(plug):
                mc.setAttr(plug, 0)
            else:
                mc.setAttr(plug, 1)
                
            if locked:
                mc.setAttr(plug, lock=True)
        except:
            pass

if __name__ == '__main__':
    main()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2015-05-14 : Converted from mel.
