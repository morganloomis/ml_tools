# 
#   -= ml_resetBind.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_resetBind.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_resetBind
#     ml_resetBind.main()
# From MEL, this looks like:
#     python("import ml_resetBind;ml_resetBind.main()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly remove and recreate a skinCluster while maintaining history.
# Essentially this allows you to "reset" the skin cluster after you've 
# moved some joints. It also deletes the original bindPose node.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select the skinned meshes you'd like to reset, and run the command. 
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'riggingScripts'
__revision__ = 1

import maya.cmds as mc
from maya import OpenMaya


def main():
    
    sel = mc.ls(sl=True)
    
    for each in sel:
        shapes = mc.listRelatives(each, shapes=True)
        
        for shape in shapes:
            #get skin cluster
            history = mc.listHistory(shape, groupLevels=True, pruneDagObjects=True)
            skins = mc.ls(history, type='skinCluster')
            
            for skin in skins:
                joints = mc.skinCluster(skin, query=True, influence=True)
                
                mc.setAttr(skin+'.envelope', 0)
                mc.skinCluster(skin, edit=True, unbindKeepHistory=True)
                
                #delete bindPose
                dagPose = mc.dagPose(each, query=True, bindPose=True)
                if dagPose:
                    mc.delete(dagPose)
                dagPose = mc.listConnections(skin+'.bindPose', d=False, type='dagPose')
                if dagPose:
                    mc.delete(dagPose)
                
                mc.skinCluster(joints, shape, toSelectedBones=True)
                mc.setAttr(skin+'.envelope', 1)
    if sel:
        mc.select(sel)


if __name__ == '__main__': main()


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2014-03-02 : First publish.
