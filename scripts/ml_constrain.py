from signal import CTRL_BREAK_EVENT
import logging
import puppeteer.cmds as pc
import maya.cmds as mc
import puppeteer.skinCluster as sk
import puppeteer.model as mdl
from puppeteer.snip import snip, hierarchy, appendage
from puppeteer.puppet import skeleton
import maya.OpenMaya as om1
import maya.api.OpenMaya as om
import ml_utilities as utl

LOG = logging.getLogger('puppeteer')


def selected_vertex():

    vertex = mc.ls(sl=True,fl=True)
    if not vertex or not '.vtx' in vertex[0]:
        raise RuntimeError('Please select vertices.')
    
    mesh = vertex[0].split('.')[0]
    shape = mc.listRelatives(mesh, shapes=True)[0]
    if not mc.nodeType(shape) == 'mesh':
        raise RuntimeError('Please select a mesh vertex.')
    
    vertex_transform(vertex[0])

def constrain_to_vertex(vertex, node, addToLayer=False):
    '''
    '''
    
    kwargs = {}
    if addToLayer:
        kwargs['layer'] = utl.createAnimLayer(node, namePrefix='vert')

    null = vertex_transform(vertex)
    mc.parentConstraint(null, node, maintainOffset=True, **kwargs)


def vertex_transform(vertex):
    mesh = vertex.split('.')[0]
    vtxIndex = int(vertex.split('[')[-1].strip(']'))
    #get skincluster
    skin = sk.getSkinCluster(mesh)
    if not skin:
        raise RuntimeError('Please select a mesh with a skincluster.')

    mesh = mdl.Mesh(mesh)
    
    pnt = utl.Vector(0,0,0)

    vertPositions = []
    vertPosition = mesh.vertexPosition(vtxIndex)
    
    jointWeight = {}
    vtxWeight = skin.getVertexWeights(vertex, tolerence=0.1)
    for k,v in vtxWeight.items():
        jointWeight[k] = v

    #find the largest weight, that will become the main input.
    largestInfluence = sorted(jointWeight, key=jointWeight.get)[-1]

    largestInfluence = pc.node(largestInfluence)
    
    #figure out the default world matrix for this control
    #do better next time

    tmp = pc.createNode('transform')
    tmp.snap(largestInfluence)
    tmp.t.set(*pnt)
    defaultMatrix = om.MMatrix(tmp.worldMatrix[0].get())
    mc.delete(tmp)

    blend = pc.createNode('blendMatrix')

    #output matrix of each joint
    i = 0
    for joint, weight in list(jointWeight.items()):
        joint = pc.node(joint)
        #get an offset matrix for each joint
        jointInverse = om.MMatrix(joint.worldInverseMatrix[0].get())
        localMatrix = defaultMatrix * jointInverse
        offset = [x for x in localMatrix]
        offsetMatrix = pc.createNode('holdMatrix', name='{}_offsetMatrix'.format(joint.shortName))
        offsetMatrix.inMatrix.set(offset)
        
        mult = pc.createNode('multMatrix', name='{}_mult'.format(joint.shortName))
        
        offsetMatrix.outMatrix.connect(mult.matrixIn[0])
        joint.worldMatrix[0].connect(mult.matrixIn[1])
        
        if joint == largestInfluence:
            mult.matrixSum.connect(blend.inputMatrix)
        else:
            mult.matrixSum.connect(blend.target[i].targetMatrix)
            blend.target[i].weight.set(weight)
            blend.target[i].useScale.set(False)
            blend.target[i].useShear.set(False)
            i+=1
    null = pc.createNode('transform')
    blend.outputMatrix.connect(null.offsetParentMatrix)

    return null
    

def main():
    sel = mc.ls(sl=True, fl=True)
    for vertex in sel:
        loc = mc.spaceLocator(name='{}_vtx_{}'.format(vertex.split('.')[0], vertex.split('[')[-1].strip(']')))
        mc.select(vertex, loc[0])
        mm.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')


def puppeteer_vertex(vertex, node):

    point = mc.pointPosition(vertex)
    model = vertex.split('.')[0]

    vertID = int(vertex.split('[')[-1].strip(']'))

    skin = sk.getSkinCluster(model)
    if not skin:
        raise RuntimeError('Vertex is not skinned: {}'.format(vertex))

    jointWeight = skin.getVertexWeights(vertex)

    #need to add threshold to getVertexWeights
    culledJointWeights = {}
    for k, v in list(jointWeight.items()):
        if v > 0.01:
            culledJointWeights[k] = v

    if not culledJointWeights:
        raise RuntimeError('vertex {} has no weights'.format(vertex))

    jointWeight = culledJointWeights

    #find the largest weight, that will become the main input.
    largestInfluence = sorted(jointWeight, key=jointWeight.get)[-1]

    largestInfluence = pc.node(largestInfluence)
    
    #figure out the default world matrix for this control
    #do better next time
    tmp = pc.createNode('transform')
    tmp.snap(largestInfluence)
    tmp.t.set(*point)
    defaultMatrix = om.MMatrix(tmp.worldMatrix[0].get())
    mc.delete(tmp)
    
    #output matrix of each joint
    i = 0
    blend = pc.createNode('blendMatrix', name=str(node).rsplit('|',1)[-1]+'_blend')
    for joint, weight in list(jointWeight.items()):
        joint = pc.node(joint)
        #get an offset matrix for each joint
        jointInverse = om.MMatrix(joint.worldInverseMatrix[0].get())
        localMatrix = defaultMatrix * jointInverse
        offset = [x for x in localMatrix]
        offsetMatrix = pc.createNode('holdMatrix', name='{}_offsetMatrix'.format(joint.shortName))
        offsetMatrix.inMatrix.set(offset)
        
        mult = pc.createNode('multMatrix', name='{}_mult'.format(joint.shortName))
        
        offsetMatrix.outMatrix.connect(mult.matrixIn[0])
        if joint.hasAttr('skinCluster_worldMatrix'):
            matrix = joint.skinCluster_worldMatrix.sourceConnection()
            matrix.connect(mult.matrixIn[1])
        else:
            joint.worldMatrix[0].connect(mult.matrixIn[1])
        
        if joint == largestInfluence:
            mult.matrixSum.connect(blend.inputMatrix)
        else:
            mult.matrixSum.connect(blend.target[i].targetMatrix)
            blend.target[i].weight.set(weight)
            blend.target[i].useScale.set(False)
            blend.target[i].useShear.set(False)
            i+=1
    
    blend.outputMatrix.connect(node.offsetParentMatrix)

if __name__ == '__main__':
    main()
