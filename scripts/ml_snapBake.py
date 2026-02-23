# -= ml_snapBake.py =-
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
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Create a locator constrained to a node or surface that acts as a target for
# another node. Used to get one transform to follow another without a live
# connection (baking on demand). Avoids cycles when constraining e.g. a hand
# to its own mesh.
#
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Select source (transform or mesh vertex) then destination. Create Snap Locator.
# Key the locator's "Follow" attribute on/off for frames to bake. Press Bake
# Snap Locators to snap the destination to the locator on those frames.
#
#     ___________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - -
#
# This script requires the ml_utilities module.
#
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -

__author__ = 'Morgan Loomis'
__license__ = 'MIT'
__revision__ = 1
__category__ = 'animation'

import maya.cmds as mc
from maya.api.OpenMaya import MMatrix

try:
    import ml_utilities as utl
    utl.upToDateCheck(32)
except ImportError:
    result = mc.confirmDialog(
        title='Module Not Found',
        message='This tool requires the ml_utilities module. Once downloaded you need to restart Maya.',
        button=['Download Module', 'Cancel'],
        defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel')
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/tool/ml_utilities/', absolute=True)

import ml_snap, ml_match

SNAP_BAKE_ATTR = 'ml_snapBake'
FOLLOW_ATTR = 'followSnap'
DESTINATION_ATTR = 'ml_snapDestination'


def ui():
    '''
    User interface for snap bake.
    '''
    with utl.MlUi('ml_snapBake', 'Snap Bake', width=400, height=120, info='''Create a locator that follows the first selection (transform or vertex).
Key the locator's Follow attribute on frames to bake. Bake Snap Locators
snaps the destination to the locator on those frames.''') as win:

        mc.checkBoxGrp('ml_snapBake_maintainOffset_checkBox', label='Maintain Offset',
                       value1=True,
                       annotation='Keep the offset between source and destination at creation.')

        win.ButtonWithPopup(
            label='Create Snap Locator',
            command=create_snap_locator_sel,
            name='ml_snapBake',
            readUI_toArgs={
                'maintainOffset': 'ml_snapBake_maintainOffset_checkBox',
            },
            annotation='Create a locator that follows the first selection, targeting the second.')

        win.ButtonWithPopup(
            label='Bake Snap Locators',
            command=bake_snap_locators_sel,
            name='ml_snapBake',
            annotation='Snap destination nodes to their snap locators on frames where Follow is on.')


def create_snap_locator_sel(maintainOffset=True):
    '''
    Get selection, validate, and call create_snap_locator.
    First selection can be a transform or a mesh vertex component.
    '''
    sel = mc.ls(sl=True, fl=True)
    if not sel or len(sel) < 2:
        utl.warning('Select source (transform or vertex) then destination.')
        return

    src = sel[0]
    dst = sel[1]

    # Resolve destination to transform (strip components)
    if '.' in dst and ('vtx[' in dst or '.cv[' in dst or '.pt[' in dst):
        utl.warning('Destination must be a transform, not a component.')
        return
    dst_transform = dst.split('.')[0] if '.' in dst else dst
    if not mc.objExists(dst_transform):
        utl.warning('Destination does not exist.')
        return

    create_snap_locator(src, dst_transform, maintainOffset=maintainOffset)


def _is_vertex_component(node):
    '''Return True if node is a mesh vertex component (mesh.vtx[i]).'''
    if not isinstance(node, str) or '.' not in node:
        return False
    part = node.split('.')[-1]
    return part.startswith('vtx[') and part.endswith(']')


def _get_vertex_source_matrix_node(src_vertex):
    '''
    Create a hidden driver transform constrained to the vertex;
    return the driver transform name so we can use its worldMatrix.
    Uses pointOnPolyConstraint so the driver follows the vertex.
    '''
    mesh = src_vertex.split('.')[0]
    if not mc.objExists(mesh):
        raise RuntimeError('Mesh does not exist: {}'.format(mesh))
    driver = mc.spaceLocator(name='snapBake_driver_#')[0]
    mc.setAttr(driver + '.visibility', 0)
    mc.pointOnPolyConstraint(src_vertex, driver)
    return driver


def create_snap_locator(src, dst, maintainOffset=True):
    '''
    Create a locator that follows src (transform or vertex) and will drive dst when baked.
    If maintainOffset is True, the locator is positioned so that when baked, dst keeps
    its current offset from src. Otherwise the locator matches dst at creation.
    '''
    src_is_vertex = _is_vertex_component(src)
    src_transform = src.split('.')[0] if '.' in src else src

    if not mc.objExists(dst):
        utl.warning('Destination does not exist.')
        return

    name = mc.ls(dst, shortNames=True)[0]
    if ':' in name:
        name = name.rpartition(':')[-1]
    locator = mc.spaceLocator(name='snapBake_{}_#'.format(name))[0]
    mc.setAttr(locator + '.rotateOrder', 3)

    # Identifying attribute
    mc.addAttr(locator, longName=SNAP_BAKE_ATTR, attributeType='bool', defaultValue=True)
    mc.setAttr(locator + '.' + SNAP_BAKE_ATTR, lock=True)

    # Keyable follow attribute (which frames to bake)
    mc.addAttr(locator, longName=FOLLOW_ATTR, attributeType='bool', defaultValue=True, keyable=True)

    # Message to destination for tracking
    mc.addAttr(locator, longName=DESTINATION_ATTR, attributeType='message')
    mc.connectAttr(dst + '.message', locator + '.' + DESTINATION_ATTR)

    if src_is_vertex:
        driver = _get_vertex_source_matrix_node(src)
        src_matrix_plug = driver + '.worldMatrix[0]'
    else:
        driver = None
        if not mc.objExists(src_transform):
            utl.warning('Source does not exist.')
            mc.delete(locator)
            return
        src_matrix_plug = src_transform + '.worldMatrix[0]'

    # Offset: locator.offsetParentMatrix = offset * src_world.
    # If maintainOffset: offset = dst_world * inv(src_world) so locator world = dst (keep offset).
    # Otherwise: offset = identity so locator follows src exactly.
    mc.currentTime(mc.currentTime(query=True))
    src_world = mc.getAttr(src_matrix_plug)
    src_m = MMatrix(src_world)
    if maintainOffset:
        dst_world = mc.getAttr(dst + '.worldMatrix[0]')
        dst_m = MMatrix(dst_world)
        offset_m = dst_m * src_m.inverse()
        offset_list = [offset_m[k] for k in range(16)]
    else:
        offset_list = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    mult = mc.createNode('multMatrix', name='snapBake_offset_#')
    mc.setAttr(mult + '.matrixIn[0]', offset_list, type='matrix')
    mc.connectAttr(src_matrix_plug, mult + '.matrixIn[1]')
    mc.connectAttr(mult + '.matrixSum', locator + '.offsetParentMatrix')

    mc.select(locator, replace=True)


def _get_snap_locators(locators=None):
    '''Return list of nodes that have the snap bake attribute (are snap locators).'''
    if locators is not None:
        return [n for n in locators if mc.attributeQuery(SNAP_BAKE_ATTR, exists=True, node=n)]
    sel = mc.ls(sl=True)
    if sel:
        return [n for n in sel if mc.attributeQuery(SNAP_BAKE_ATTR, exists=True, node=n)]
    # Find all in scene
    all_transforms = mc.ls(type='transform')
    return [n for n in all_transforms if mc.attributeQuery(SNAP_BAKE_ATTR, exists=True, node=n)]


def _get_follow_on_frames(locator):
    '''
    Return sorted list of frames where the Follow attribute is on (True).
    If Follow has no keyframes, use the current value for the whole range.
    If keyed, query value at each frame with getAttr(..., time=t) so the
    playhead is not changed.
    '''
    plug = locator + '.' + FOLLOW_ATTR
    if not mc.objExists(plug):
        return []
    start, end = utl.frameRange()
    keytimes = mc.keyframe(locator, attribute=FOLLOW_ATTR, query=True, timeChange=True)
    if not keytimes:
        return list(range(int(start), int(end) + 1)) if mc.getAttr(plug) else []
    on_frames = [t for t in range(int(start), int(end) + 1) if mc.getAttr(plug, time=t)]
    return on_frames


def bake_snap_locators_sel():
    '''Bake from selection or all snap locators in scene.'''
    bake_snap_locators()


def bake_snap_locators(locators=None):
    '''
    For each snap locator, on every frame where Follow is on, snap the destination
    node to the locator and set a key.
    '''
    locs = _get_snap_locators(locators)
    if not locs:
        utl.warning('Select one or more snap locators, or run with none to use all in scene.')
        return
    start, end = utl.frameRange()
    reset_time = mc.currentTime(query=True)


    #locator connections
    driven = {}
    for loc in locs:
        dest_plugs = mc.listConnections(loc + '.' + DESTINATION_ATTR, source=True, destination=False, plugs=True)
        if not dest_plugs:
            utl.warning('Snap locator has no destination: {}'.format(loc))
            continue
        dst = dest_plugs[0].split('.')[0]
        driven[loc] = dst

    followFrames = {}
    for loc in locs:
        followFrames[loc] = _get_follow_on_frames(loc)
    allFrames = [num for numbers in followFrames.values() for num in numbers]
    allFrames = sorted(list(set(allFrames)))

    #need to go through and get all the matrix data first
    #this is a dict of all locators and their matrix data for every frame
    matrixData = ml_match.get_matrix_data([f'{x}.worldMatrix[0]' for x in locs], start=allFrames[0], end=allFrames[-1])

    #and snap
    resetAutoKey = mc.autoKeyframe(query=True, state=True)
    mc.autoKeyframe(state=False)
    # if not mc.ogs(query=True, pause=True):
    #     mc.ogs(pause=True)
    
    for f in allFrames:
        mc.currentTime(f)
        for loc in locs:
            if f not in followFrames[loc]:
                continue
            ml_snap.set_worldMatrix(driven[loc], matrixData[f'{loc}.worldMatrix[0]'][f])
            mc.setKeyframe(driven[loc])

    # if mc.ogs(query=True, pause=True):
    #     mc.ogs(pause=True)

    mc.currentTime(reset_time)
    mc.autoKeyframe(state=resetAutoKey)


if __name__ == '__main__':
    ui()

