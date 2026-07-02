# -= ml_skinConstraint.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 1
#   / / / / / / /  2025-01-24
#  /_/ /_/ /_/_/  _________
#               /_________/
#
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Copyright 2026 Morgan Loomis
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_skinConstraint.py
#
# Run the tool in a python shell or shelf button by importing the module,
# and then calling the primary function:
#
#     import ml_skinConstraint
#     ml_skinConstraint.ui()
#
#
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Constrain a transform to follow a skinned vertex by blending influence matrices
# by vertex weights (API-based; works for joint- and matrix-driven skins). The node follows the vertex as the mesh deforms.
#
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Select the target transform first, then the skinned vertex (e.g. pCube1.vtx[0]).
# Run ml_skinConstraint.ui() or call skinned_vertex_constraint(vertex, node).
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
__revision__ = 1

import maya.cmds as mc
from maya.api.OpenMaya import MMatrix
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma

try:
    import ml_utilities as utl
except ImportError as exc:
    raise RuntimeError('ml_skinConstraint requires ml_utilities') from exc

WEIGHT_THRESHOLD = 0.01

def main():
    '''Run from selection: first select the transform to constrain, then the vertex.'''
    sel = mc.ls(sl=True, fl=True)
    if len(sel) == 1 and '[' in sel[0]:
        name = sel[0].replace('.','_').replace('[','_').strip(']')
        sel.append(mc.spaceLocator(name=name)[0])
    if not sel or len(sel) < 2:
        utl.warning('Select a skinned vertex, or else a vertex and a transform.')
        return
    vertex = sel[0]
    node = sel[1]
    if '.vtx[' not in vertex and '.cv[' not in vertex:
        utl.warning('First selection must be a mesh vertex (e.g. pCube1.vtx[0]).')
        return
    if mc.nodeType(node) != 'transform':
        utl.warning('First selection must be a transform.')
        return
    skinned_vertex_constraint(vertex, node)
    mc.select(node, replace=True)


def get_skin_cluster(mesh):
    '''Return the first skinCluster node affecting the mesh, or None.'''
    return utl.getSkinCluster(mesh)


def _skin_cluster_fn(skin):
    '''Return MFnSkinCluster for the given skinCluster node name.'''
    sel = om.MSelectionList()
    sel.add(skin)
    obj = sel.getDependNode(0)
    return oma.MFnSkinCluster(obj)


def get_vertex_weights_by_index(skin, vertex_index, tolerance=0.0):
    '''
    Return dict of influence_index -> weight for the given vertex using the API.
    Weights below tolerance are excluded. Works for all skinClusters (joint- or matrix-driven).
    '''
    skin_fn = _skin_cluster_fn(skin)
    wl_plug = skin_fn.findPlug('weightList', False)
    w_plug = skin_fn.findPlug('weights', False)
    wl_attr = wl_plug.attribute()
    w_attr = w_plug.attribute()
    if vertex_index < 0 or vertex_index >= wl_plug.numElements():
        return {}
    w_plug.selectAncestorLogicalIndex(vertex_index, wl_attr)
    inf_indices = w_plug.getExistingArrayAttributeIndices()
    result = {}
    for inf_id in inf_indices:
        w_plug.selectAncestorLogicalIndex(inf_id, w_attr)
        weight = w_plug.asDouble()
        if weight > tolerance:
            result[inf_id] = weight
    return result


def get_influence_matrix_plug(skin, influence_index):
    '''
    Return the plug (attr string) to connect for the world matrix of this influence.
    Uses the connection source of skinCluster.matrix[influence_index] when present;
    otherwise creates a holdMatrix with the current value and returns its outMatrix.
    '''
    matrix_plug = '{}.matrix[{}]'.format(skin, influence_index)
    conns = mc.listConnections(matrix_plug, source=True, destination=False, plugs=True)
    if conns:
        return conns[0]
    hold = mc.createNode('holdMatrix', name='skinInf_{}_matrix'.format(influence_index))
    mc.setAttr('{}.inMatrix'.format(hold), mc.getAttr(matrix_plug), type='matrix')
    return '{}.outMatrix'.format(hold)


def get_influence_bind_pre_matrix(skin, influence_index):
    '''Return bindPreMatrix for this influence as a flat list of 16 floats (row-major).'''
    return mc.getAttr('{}.bindPreMatrix[{}]'.format(skin, influence_index))


def _vertex_component_to_index(vertex):
    '''Extract vertex index from component string e.g. pCube1.vtx[0] -> 0.'''
    return int(vertex.split('[')[-1].rstrip(']'))


def _short_name(node):
    return mc.ls(node, shortNames=True)[0] if mc.objExists(node) else node.rsplit('|')[-1].split(':')[-1]


def skinned_vertex_constraint(vertex, node):
    '''
    Constrain a transform (node) to follow a skinned vertex. The node's
    offsetParentMatrix is driven by a blend of the influencing matrices
    weighted by the vertex's skin weights (API-based, works for joint- and matrix-driven skins).

    Args:
        vertex: Component string, e.g. 'pCube1.vtx[0]'
        node: Transform to constrain (name string)
    '''
    point = mc.pointPosition(vertex)
    model = vertex.split('.')[0]
    if mc.nodeType(model) != 'transform':
        model = mc.listRelatives(model, parent=True, path=True)[0]

    skin = get_skin_cluster(model)
    if not skin:
        raise RuntimeError('Vertex is not skinned: {}'.format(vertex))

    vertex_index = _vertex_component_to_index(vertex)
    inf_weights = get_vertex_weights_by_index(skin, vertex_index, tolerance=WEIGHT_THRESHOLD)
    if not inf_weights:
        raise RuntimeError('Vertex {} has no weights'.format(vertex))

    largest_inf = max(inf_weights, key=inf_weights.get)

    # Default world matrix: largest influence orientation with translation at vertex position
    world_mat = list(mc.getAttr('{}.matrix[{}]'.format(skin, largest_inf)))
    world_mat[12], world_mat[13], world_mat[14] = point[0], point[1], point[2]
    default_matrix = MMatrix(world_mat)

    node_short = _short_name(node)
    blend = mc.createNode('blendMatrix', name='{}_blend'.format(node_short))

    target_index = 0
    for inf_id, weight in inf_weights.items():
        # Use current influence matrix inverse at creation (same as original joint path):
        # offset * matrix = default at creation, so offset = default * inv(matrix_now)
        inf_world = MMatrix(mc.getAttr('{}.matrix[{}]'.format(skin, inf_id)))
        inf_world_inv = inf_world.inverse()
        local_matrix = default_matrix * inf_world_inv
        offset_list = [x for x in local_matrix]

        offset_node = mc.createNode('holdMatrix', name='{}_offsetMatrix_inf{}'.format(node_short, inf_id))
        mc.setAttr('{}.inMatrix'.format(offset_node), offset_list, type='matrix')

        mult = mc.createNode('multMatrix', name='{}_mult_inf{}'.format(node_short, inf_id))
        mc.connectAttr('{}.outMatrix'.format(offset_node), '{}.matrixIn[0]'.format(mult))
        mc.connectAttr(get_influence_matrix_plug(skin, inf_id), '{}.matrixIn[1]'.format(mult))

        if inf_id == largest_inf:
            mc.connectAttr('{}.matrixSum'.format(mult), '{}.inputMatrix'.format(blend))
        else:
            mc.connectAttr(
                '{}.matrixSum'.format(mult),
                '{}.target[{}].targetMatrix'.format(blend, target_index)
            )
            mc.setAttr('{}.target[{}].weight'.format(blend, target_index), weight)
            try:
                mc.setAttr('{}.target[{}].useShear'.format(blend, target_index), False)
            except Exception:
                mc.setAttr('{}.target[{}].shearWeight'.format(blend, target_index), 0)
            target_index += 1

    mc.connectAttr('{}.outputMatrix'.format(blend), '{}.offsetParentMatrix'.format(node))


if __name__ == '__main__':
    main()
