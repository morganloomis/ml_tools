# -= ml_resetBind.py =-
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_resetBind.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_resetBind
#     ml_resetBind.main()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Quickly remove and recreate a skinCluster while maintaining history.
# Essentially this allows you to "reset" the skin cluster after you've moved some
# joints. It also deletes the original bindPose node.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Select the skinned meshes you'd like to reset, and run the command.
# 
# 
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -

__author__ = 'Morgan Loomis'
__license__ = 'MIT'
__category__ = 'None'
__revision__ = 2

import maya.cmds as mc
from maya import OpenMaya


def main():

    sel = mc.ls(sl=True, long=True)

    for each in sel:
        shapes = mc.listRelatives(each, shapes=True, pa=True)

        for shape in shapes or []:
            #get skin cluster
            history = mc.listHistory(shape, groupLevels=True, pruneDagObjects=True)
            skins = mc.ls(history, type='skinCluster')

            for skin in skins:
                joints = mc.skinCluster(skin, query=True, influence=True)

                mc.setAttr(skin+'.envelope', 0)

                #need to temporarily disconnect anything that might be connected to prebind matrix
                bindPreConnections = mc.listConnections(f'{skin}.bindPreMatrix', source=True, destination=False, connections=True, plugs=True)
                bindPreValues = {}
                if bindPreConnections:
                    for s,d in zip(bindPreConnections[1::2], bindPreConnections[::2]):
                        value = mc.getAttr(d)
                        mc.disconnectAttr(s,d)
                        #mc.setAttr(d, value, type='matrix')
                    mc.refresh()
                    
                mc.skinCluster(skin, edit=True, unbindKeepHistory=True)

                #delete bindPose
                dagPose = mc.dagPose(each, query=True, bindPose=True)
                if dagPose:
                    mc.delete(dagPose)
                dagPose = mc.listConnections(skin+'.bindPose', d=False, type='dagPose')
                if dagPose:
                    mc.delete(dagPose)

                mc.skinCluster(joints, shape, toSelectedBones=True)
                
                # if bindPreConnections:
                #     mc.refresh()
                #     for s,d in zip(bindPreConnections[1::2], bindPreConnections[::2]):
                #         mc.connectAttr(s,d, f=True)

                mc.setAttr(skin+'.envelope', 1)
    if sel:
        mc.select(sel)


if __name__ == '__main__': main()

