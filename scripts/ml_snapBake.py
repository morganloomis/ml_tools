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

ml_skinConstraint = None
try:
    import ml_skinConstraint
except ImportError:
    pass

SNAP_BAKE_ATTR = 'ml_snapBake'
FOLLOW_ATTR = 'followSnap'
DESTINATION_ATTR = 'ml_snapDestination'


def ui():
    '''
    User interface for snap bake.
    '''
    with utl.MlUi('ml_snapBake', 'Snap Bake', width=400, height=200, info='''Create a locator that follows the first selection (transform or vertex).
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
            label='Create World Pin',
            command=create_world_pin_sel,
            name='ml_snapBake',
            annotation='Create a snap locator at the control\'s current world pose. It stays fixed until you move it or bake; no live follow graph.')

        win.ButtonWithPopup(
            label='Select Snap Locators',
            command=select_snap_locators_for_selection,
            name='ml_snapBake',
            annotation='Scene-wide: select every snap locator whose destination message points at one of the selected transforms.')

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


def _is_geometry_component_path(node):
    '''True if path looks like a mesh/CV/point component (not a transform plug).'''
    if not isinstance(node, str) or '.' not in node:
        return False
    tail = node.split('.')[-1]
    if tail.startswith('vtx[') and tail.endswith(']'):
        return True
    if tail.startswith('cv[') and tail.endswith(']'):
        return True
    if tail.startswith('pt[') and tail.endswith(']'):
        return True
    return False


def _transform_long_from_dag_path(path):
    '''
    Given a DAG path (transform, shape, or component), return parent transform long name or None.
    '''
    if not path or not isinstance(path, str):
        return None
    head = path.split('.')[0]
    if not mc.objExists(head):
        return None
    if mc.objectType(head, isType='transform'):
        return mc.ls(head, long=True)[0]
    parents = mc.listRelatives(head, parent=True, type='transform', fullPath=True)
    if parents:
        return parents[0]
    return None


def _add_snap_locator_metadata(locator, dst):
    '''Locked ml_snapBake, keyable followSnap, message ml_snapDestination from dst.'''
    mc.addAttr(locator, longName=SNAP_BAKE_ATTR, attributeType='bool', defaultValue=True)
    mc.setAttr(locator + '.' + SNAP_BAKE_ATTR, lock=True)
    mc.addAttr(locator, longName=FOLLOW_ATTR, attributeType='bool', defaultValue=True, keyable=True)
    mc.addAttr(locator, longName=DESTINATION_ATTR, attributeType='message')
    mc.connectAttr(dst + '.message', locator + '.' + DESTINATION_ATTR)


def collect_driven_transforms_long_from_selection():
    '''
    Unique transform long names for current selection (strip components to driving transforms).
    Returns empty list if none.
    '''
    sel = mc.ls(sl=True, long=True, flatten=True)
    if not sel:
        return []
    seen = []
    done = set()
    for s in sel:
        tf = _transform_long_from_dag_path(s)
        if tf and tf not in done:
            done.add(tf)
            seen.append(tf)
    return seen


def create_world_pin(dst):
    '''
    Snap locator at dst's current world pose: no multMatrix, offsetParentMatrix drivers, or constraints.
    '''
    if not mc.objExists(dst):
        utl.warning('Destination does not exist.')
        return None
    dst = mc.ls(dst, long=True)[0]
    if not mc.objectType(dst, isType='transform'):
        utl.warning('Destination must be a transform.')
        return None

    name = mc.ls(dst, shortNames=True)[0]
    if ':' in name:
        name = name.rpartition(':')[-1]
    locator = mc.spaceLocator(name='snapBake_{}_#'.format(name))[0]
    locator = mc.ls(locator, long=True)[0]
    mc.setAttr(locator + '.rotateOrder', 3)

    _add_snap_locator_metadata(locator, dst)

    mc.currentTime(mc.currentTime(query=True))
    dst_world = mc.getAttr(dst + '.worldMatrix[0]')
    ml_snap.set_worldMatrix(locator, list(dst_world))

    mc.select(locator, replace=True)
    return locator


def create_world_pin_sel():
    '''
    Exactly one transform (or mixed selection whose resolved transforms collapse to one),
    but not a pure-component-only selection.
    '''
    sel = mc.ls(sl=True, long=True, flatten=True)
    if not sel:
        utl.warning('Select exactly one transform for Create World Pin.')
        return
    if all(_is_geometry_component_path(s) for s in sel):
        utl.warning('Select a transform, not a component.')
        return

    tfs = collect_driven_transforms_long_from_selection()
    if not tfs:
        utl.warning('Select exactly one transform for Create World Pin.')
        return
    if len(tfs) > 1:
        utl.warning('Select exactly one transform for Create World Pin.')
        return

    create_world_pin(tfs[0])


def select_snap_locators_for_selection():
    '''
    Select all scene snap locators whose ml_snapDestination points at any selected transform.
    '''
    controls = collect_driven_transforms_long_from_selection()
    if not controls:
        utl.warning('Select one or more transforms (driven controls) to search for snap locators.')
        return
    control_set = set(controls)

    matches = []
    for loc in _get_snap_locators(None):
        dest_plugs = mc.listConnections(
            loc + '.' + DESTINATION_ATTR, source=True, destination=False, plugs=True)
        if not dest_plugs:
            continue
        dst_node = dest_plugs[0].split('.')[0]
        if not mc.objExists(dst_node):
            continue
        dst_long = mc.ls(dst_node, long=True)
        if not dst_long:
            continue
        if dst_long[0] in control_set:
            matches.append(loc)

    if not matches:
        utl.warning('No snap locators in the scene target the selected controls.')
        return
    mc.select(matches, replace=True)


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

    _add_snap_locator_metadata(locator, dst)

    if src_is_vertex:
        if ml_skinConstraint is None:
            utl.warning('Cannot follow a vertex without ml_skinConstraint.')
            mc.delete(locator)
            return
        driver = mc.spaceLocator(name='snapBake_driver_#')[0]
        mc.setAttr(driver + '.visibility', 0)
        ml_skinConstraint.skinned_vertex_constraint(src, driver)
        
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
    if not allFrames:
        utl.warning(
            'No frames to bake: every snap locator has Follow off for the timeline range, '
            'or the playback range is empty. Enable Follow (or key it on) where you want a bake.'
        )
        return

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

