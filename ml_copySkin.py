# 
#   -= ml_copySkin.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 1, 2016-10-31
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_copySkin.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_copySkin
#     ml_copySkin.ui()
# From MEL, this looks like:
#     python("import ml_copySkin;ml_copySkin.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copy a skinCluster from one mesh to another, or to a selection of vertices.
# If no skin exists on the destination, one will be created with the same influences.
# Otherwise any missing influences will be added in order to copy accurate weights.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Input a source mesh into the "Source Mesh" field by selecting a mesh and pressing the
# "Set Selected" button.
# Select destination meshes or vertices, and press the "Copy Skin" button.
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Copy Skin] : Copy the Source Skin to selection.
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'riggingScripts'
__revision__ = 1

import maya.cmds as mc

try:
    import ml_utilities as utl
    utl.upToDateCheck(24)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    

def ui():
    '''
    User interface for copy skin
    '''
    
    CopySkinUI()


class CopySkinUI(utl.MlUi):
    '''Inherited from MlUi
    '''

    def __init__(self):

        super(CopySkinUI, self).__init__('ml_copySkin', 'Copy SkinClusters', width=400, height=180, 
                                         info='''Select a skinned mesh to add to the Source Mesh field below.
Select a destination mesh, or vertices to copy the skin to.
Press the button to copy the skin weights.''')
        
        self.buildWindow()
        
        self.srcMeshField = self.selectionField(label='Source Mesh', 
                                                annotation='Select the mesh to be used as the source skin.', 
                                                channel=False, 
                                                text='')
        
        mc.button(label='Copy Skin', command=self.copySkin, annotation='Copy the Source Skin to selection.')
        
        self.finish()
        
        
    def copySkin(self,*args):
        
        sourceMesh = mc.textFieldButtonGrp(self.srcMeshField, query=True, text=True)
        
        if not mc.objExists(sourceMesh):
            raise RuntimeError('Input a source mesh into the UI to copy skin from.')
        
        sel = mc.ls(sl=True, fl=True)
        
        if not sel:
            raise RuntimeError('Select a mesh or vertices to copy the skin to.')
        
        meshSel = []
        vtxSel = []
        for each in sel:
            if '.vtx[' in each:
                vtxSel.append(each)
            else:
                meshSel.append(each)
                
        if vtxSel:
            copySkinComponents(sourceMesh, vtxSel)
        
        if meshSel:
            for each in meshSel:
                copySkinCluster(sourceMesh, each)


def getSkinCluster(mesh):
    
    shapes = mc.listRelatives(mesh, shapes=True, path=True)

    for shape in shapes:
        history = mc.listHistory(shape, groupLevels=True, pruneDagObjects=True)
        if not history:
            continue
        skins = mc.ls(history, type='skinCluster')
        if skins:
            return skins[0]
    
    return None
    
    
def copySkinInfluences(source, dest):

    sourceSkin = getSkinCluster(source)
    if not sourceSkin:
        return False
    
    joints = mc.skinCluster(sourceSkin, query=True, influence=True)
    
    destSkin = getSkinCluster(dest)
    
    if not destSkin:
        destSkin = mc.skinCluster(joints, dest, toSelectedBones=True)[0]
    else:
        destJoints = mc.skinCluster(destSkin, query=True, influence=True)
        for joint in [x for x in joints if x not in destJoints]:
            mc.skinCluster(destSkin, edit=True, addInfluence=joint, lockWeights=False, weight=0)
    
    return destSkin


def copySkinComponents(source, destinationVerts):
    
    if not mc.listRelatives(source, shapes=True):
        raise RuntimeError('Source object must be geometry.')

    sourceSkin = getSkinCluster(source)
    
    if not sourceSkin:
        raise RuntimeError("Source mesh doesn't have a skinCluster to copy from.")
    
    destMesh = mc.ls(destinationVerts[0], o=True)[0]
    destMesh = mc.listRelatives(destMesh, parent=True)[0]
    destSkin = copySkinInfluences(source, destMesh)
    
    tempSet = mc.sets(destinationVerts)
    
    mc.select(source, tempSet)
    
    mc.copySkinWeights(noMirror=True,
                       surfaceAssociation='closestPoint', 
                       influenceAssociation='closestJoint', 
                       normalize=True)    
    
    mc.delete(tempSet)
    mc.select(destinationVerts)


def copySkinCluster(source, destination):
    
    sourceSkin = getSkinCluster(source)
    if not sourceSkin:
        raise RuntimeError("Source mesh doesn't have a skinCluster to copy from.")
    
    destSkin = copySkinInfluences(source, destination)

    mc.copySkinWeights(sourceSkin=sourceSkin, destinationSkin=destSkin, noMirror=True,
                       surfaceAssociation='closestPoint', 
                       influenceAssociation='closestJoint', normalize=True)
    
    return destSkin



if __name__ == '__main__':
    ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-10-31 : First publish.
