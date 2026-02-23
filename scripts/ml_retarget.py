import math, warnings, os
import maya.cmds as mc
import maya.mel as mm
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as omAnim
import ml_utilities as utl
import ml_snap, ml_puppet, ml_match
from math import isclose
import time

RETARGET_RIG_FILE = os.path.dirname(__file__)+'/ml_retarget.ma'

if not os.path.exists(RETARGET_RIG_FILE):
    raise ImportError(f'Retarget scene not found, please place in this same directory: {os.path.dirname(__file__)}')

uiUnit = om.MTime.uiUnit()

SKELETON_LOOKUP = {'Hip':['hips'],
                    'Spine':['spine7','spine2','spine1'],
                    'Neck':['neck'],
                    'Head':['head'],
                    'LeftCollar':['leftshoulder'],
                    'RightCollar':['rightshoulder'],
                    'LeftShoulder':['leftarm'],
                    'RightShoulder':['rightarm'],
                    'LeftElbow':['leftforearm'],
                    'RightElbow':['rightforearm'],
                    'LeftHand':['lefthand'],
                    'RightHand':['righthand'],
                    'LeftHip':['leftupleg'],
                    'RightHip':['rightupleg'],
                    'LeftKnee':['leftleg'],
                    'RightKnee':['rightleg'],
                    'LeftFoot':['leftfoot'],
                    'RightFoot':['rightfoot'],
                    'LeftToe':['lefttoebase'],
                    'RightToe':['righttoebase'],

                    'LeftThumb':['lefthandthumb1','lefthandthumb'],
                    'LeftIndex Finger':['lefthandindex1','lefthandindex'],
                    'LeftMiddle Finger':['lefthandmiddle1','lefthandmiddle'],
                    'LeftRing Finger':['lefthandring1','lefthandring'],
                    'LeftPinky Finger':['lefthandpinky1','lefthandpinky'],
                    'RightThumb':['righthandthumb1','righthandthumb'],
                    'RightIndex Finger':['righthandindex1','righthandindex'],
                    'RightMiddle Finger':['righthandmiddle1','righthandmiddle'],
                    'RightRing Finger':['righthandring1','righthandring'],
                    'RightPinky Finger':['righthandpinky1','righthandpinky']
                    }



SIDE_LIST = ['Center','Left','Right']
LABEL_LIST = ['None',
                'Root',
                'Hip',
                'Knee',
                'Foot',
                'Toe',
                'Spine',
                'Neck',
                'Head',
                'Collar',
                'Shoulder',
                'Elbow',
                'Hand',
                'Finger',
                'Thumb',
                'PropA',
                'PropB',
                'PropC',
                'Other',
                'Index Finger',
                'Middle Finger',
                'Ring Finger',
                'Pinky Finger',
                'Extra Finger',
                'Big Toe',
                'Index Toe',
                'Middle Toe',
                'Ring Toe',
                'Pinky Toe',
                'Foot Thumb']

def tag_skeleton():
    '''
    Evaluate a skeleton to apply side and type to all joints, in preparation for matching.
    The idea is that the data about the skeleton should be encoded in the scene, rather than
    on the fly. That allows for manual fixing of issues and support for odd skeletons.
    '''
    joint = None
    for key in SKELETON_LOOKUP.keys():
        j = tag_joint(key)
        if j and key == 'Hip':
            joint = j

    if joint:
        mc.select(joint)
        mm.eval('displayJointLabels 1;')


def tag_joint(key):

    if key not in SKELETON_LOOKUP.keys():
        raise ValueError(f'{key} not a valid key.')

    joint = None
    joints = mc.ls(type='joint')
    
    side = 'Center'
    label = key
    for each in SIDE_LIST:
        if key.startswith(each):
            label = key.replace(each, '')
            side = each
            break

    for each in SKELETON_LOOKUP[key]:
        for j in joints:
            if j.lower().endswith(each):
                joint = j
                break
        if joint:
            break
    if not joint:
        print(f'Joint not found: {side} {label}')
        return

    mc.setAttr(joint+'.side', SIDE_LIST.index(side))
    mc.setAttr(joint+'.type', LABEL_LIST.index(label))
    return joint


def joint_from_tag(side, label, root=None):
    joints = []
    if root and mc.objExists(root):
        joints = mc.listRelatives(root, ad=True, pa=True, type='joint')
    else:
        joints = mc.ls(type='joint')
    for joint in joints:
        sideIdx = mc.getAttr(joint+'.side')
        if side == SIDE_LIST[sideIdx]:
            typeIdx = mc.getAttr(joint+'.type')
            if label == LABEL_LIST[typeIdx]:
                return joint
            

def name_from_tag(side, label):
    if label == 'None':
        return None
    label = label.replace(' ','')
    if side in ['Center','None']:
        side = ''
    return f'{side}{label}'


def import_mocap(filename=None, puppet=None):

    sel = mc.ls(sl=True)
    if not sel and not puppet:
        raise RuntimeError('Please select a puppet')
    if not puppet:
        puppet = sel[0]

    if not filename:
        filename = mc.fileDialog2(caption='Import FBX', 
                                fileFilter='FBX Files (*.fbx)', 
                                fileMode=1,
                                dialogStyle=1)
        filename = filename[0]
    
    root, fbxNodes = import_and_tag_fbx(filename)
    namespace = puppet.split(':')[0]
    retarget = import_retarget_node(namespace)
    ns = retarget.split(':')[0]

    bake_skeleton_to_retarget_node(retarget, root)
    #mc.delete(fbxNodes)

    constrain_puppet_to_retarget(puppet, ns, layer=False)


def connect_skeleton_to_retarget_node(retarget, root=None):

    joints = []
    if root and mc.objExists(root):
        joints = mc.listRelatives(root, ad=True, pa=True, type='joint')
        joints.append(root)
    else:
        joints = mc.ls(type='joint')

    for joint in joints:
        connect_joint_to_retarget(joint, retarget)


def connect_joint_to_retarget(joint, retarget):

    side = SIDE_LIST[mc.getAttr(joint+'.side')]
    label = LABEL_LIST[mc.getAttr(joint+'.type')]
    name = name_from_tag(side,label)
    if not name:
        return
    
    if not mc.attributeQuery(name, exists=True, node=retarget):
        print(f'Warning: retarget attribute does not exist: {retarget}.{name}')
        return
    mc.connectAttr(f'{joint}.worldMatrix[0]', f'{retarget}.{name}', force=True)

    #look for XYZ attrs:
    for a in 'XYZ':
        if mc.attributeQuery(name+a, exists=True, node=retarget):
            mc.connectAttr(f'{joint}.worldMatrix[0]', f'{retarget}.{name}{a}', force=True)

    #check for fingers
    if 'Finger' not in label and 'Thumb' not in label:
        return
    i = 1
    while True:
        kids = mc.listRelatives(joint, type='joint')
        attr = f'{name}{i}'
        if not kids or not mc.attributeQuery(attr, exists=True, node=retarget):
            return
        mc.connectAttr(f'{kids[0]}.worldMatrix[0]', f'{retarget}.{attr}', force=True)
        joint=kids[0]
        i+=1
    

def bake_skeleton_to_retarget_node(retarget, root=None):

    retargNS = retarget.split(':')[0]
    joints = []
    if root and mc.objExists(root):
        joints = mc.listRelatives(root, ad=True, pa=True, type='joint')
        joints.append(root)
    else:
        joints = mc.ls(type='joint')

    start, end = _get_range(joints[-1])

    matrices = {}
    for joint in joints:
        side = SIDE_LIST[mc.getAttr(joint+'.side')]
        label = LABEL_LIST[mc.getAttr(joint+'.type')]
        name = name_from_tag(side,label)
        if not name:
            continue
        if not mc.attributeQuery(name, exists=True, node=retarget):
            print(f'Warning: retarget attribute does not exist: {retarget}.{name}')
            continue
        
        matrices[f'{joint}.worldMatrix[0]'] = name
        
        #check for fingers
        if 'Finger' not in name and 'Thumb' not in name:
            continue
        i = 1
        while True:
            kids = mc.listRelatives(joint, type='joint')
            attr = f'{name}{i}'
            if not kids or not mc.attributeQuery(attr, exists=True, node=retarget):
                break
            matrices[f'{kids[0]}.worldMatrix[0]'] = attr
            joint=kids[0]
            i+=1

    matrixData = ml_match.get_matrix_data(list(matrices.keys()), start=start, end=end)
    clip =  f'{retargNS}:clip'
    for plug,value in matrixData.items():
        name = matrices[plug]
        #build a keyframe
        times = sorted(value.keys())
        points = [[],[],[]]

        for t in times:
            flat = [y for y in value[t]]
            points[0].append(flat[12:15]) #position
            points[1].append(flat[:3]) #x
            points[2].append(flat[8:11]) #z

        for j,a in enumerate(['','_X','_Z']):
            for i,x in enumerate('XYZ'):
                attr = f'{name}{a}{x}'
                if not mc.attributeQuery(attr, exists=True, node=clip):
                    continue
                p = [y[i] for y in points[j]]
                set_keyframes_api(f'{clip}.{attr}', times, p)


def set_keyframes_api(node_attr, frames, values):
    
    #set an initial keyframe
    mc.setKeyframe(node_attr, value=0, time=frames[0])

    # Get the plug
    sel = om.MSelectionList()
    sel.add(node_attr)
    plug = sel.getPlug(0)
    
    # Create animCurve if it doesn't exist
    if not plug.isConnected:  
        animCurve = omAnim.MFnAnimCurve()
        animCurve.create(plug)
    else:
        animCurve = omAnim.MFnAnimCurve(plug.source().node())
    
    # Add keys
    time_array = om.MTimeArray()
    value_array = om.MDoubleArray()
    
    for frame, value in zip(frames, values):
        time_array.append(om.MTime(frame, om.MTime.uiUnit()))
        value_array.append(value)
    
    animCurve.addKeys(time_array, value_array)


def import_and_tag_fbx(fbxFile):

    # Save current frame rate
    current_frame_rate = mc.currentUnit(query=True, time=True)
    
    mm.eval('FBXResetImport')
    mm.eval('FBXImportShapes -v false')
    mm.eval('FBXImportSkins -v false')
    mm.eval('FBXImportConvertDeformingNullsToJoint -v true')
    mm.eval('FBXImportCacheFile -v false')
    mm.eval('FBXImportCameras -v false')
    
    a = mc.ls(assemblies=True)
    mm.eval(f'FBXImport -f "{fbxFile}";')
    
    # Restore frame rate
    mc.currentUnit(time=current_frame_rate)
    ass = [x for x in mc.ls(assemblies=True) if x not in a]
    if not ass:
        raise RuntimeError('Import Failed.')
    root = None
    for a in ass:
        if mc.nodeType(a) == 'joint':
            root = a
        else:
            mc.delete(a)

    if not root:
        for a in ass:
            x = mc.listRelatives(a, type='joint', pa=True)
            if x:
                root = x[0]
                break

    if not root:
        raise RuntimeError('Could not determine root joint.')
    start, end = _get_range(root)
    mc.playbackOptions(min=start, max=end)

    tag_skeleton()
    return root, ass


def import_retarget_node(namespace=None):
    if namespace:
        namespace = 'RETARGET_'+namespace
    else:
        namespace = 'RETARGET'
    mc.file(RETARGET_RIG_FILE, r=True, mergeNamespacesOnClash=True, namespace=namespace)
    return f'{namespace}:retarget'


def bake_retarget(clip, fbxNodes, deleteFBX=True):
    allFBX = mc.listRelatives(fbxNodes, ad=True, pa=True)
    allFBX = mc.ls(allFBX, type='joint')

    start, end = _get_range(allFBX)

    #bake
    mc.bakeResults(clip, 
                   simulation=True, 
                   time=(start,end), 
                   sampleBy=1, 
                   disableImplicitControl=True)
    
    if deleteFBX:
        mc.delete(fbxNodes)


def constrain_puppet_to_retarget(puppet, retargetNS, layer=False):

    def _distance(a,b):
        pa = None
        pb = None
        if '.' in a:
            #it's a matrix attr
            pa = utl.Vector(*ml_snap.matrix_to_position(a))
            pb = utl.Vector(*ml_snap.matrix_to_position(b))
        else:
            pa = utl.Vector(*ml_snap.get_worldPosition(a))
            pb = utl.Vector(*ml_snap.get_worldPosition(b))
        v = pa-pb
        return v.magnitude()
        
    pup_ns = puppet.rsplit(':',1)[0]
    if pup_ns:
        pup_ns = pup_ns+':'

    #set settings
    thigh = _distance(pup_ns+'Lf_leg_fk1_ctrl',pup_ns+'Lf_leg_fk2_ctrl')
    shin = _distance(pup_ns+'Lf_leg_fk2_ctrl',pup_ns+'Lf_leg_fk3_ctrl')
    hips = _distance(pup_ns+'Lf_leg_fk1_ctrl',pup_ns+'Rt_leg_fk1_ctrl')

    mc.setAttr(f'{retargetNS}:clip.thigh_length', thigh)
    mc.setAttr(f'{retargetNS}:clip.shin_length', shin)
    mc.setAttr(f'{retargetNS}:clip.hip_width', hips)

    #spine        
    mc.setAttr(f'{retargetNS}:clip.spine0_length', _distance(f'{pup_ns}pup_skeleton.chain[1].rest_matrix',f'{pup_ns}spine_skeleton.chain[1].rest_matrix'))

    for i in range(1,5):
        mc.setAttr(f'{retargetNS}:clip.spine{i}_length', _distance(f'{pup_ns}spine_skeleton.chain[{i}].rest_matrix',f'{pup_ns}spine_skeleton.chain[{i+1}].rest_matrix'))

    #spine pivot
    mc.connectAttr(pup_ns+'spine_hips_pivot_remap.color[0].color_Color',f'{retargetNS}:clip.hips_pivot_neg')
    mc.connectAttr(pup_ns+'spine_hips_pivot_remap.color[2].color_Color',f'{retargetNS}:clip.hips_pivot_pos')
    mc.connectAttr(pup_ns+'spine_chest_pivot_remap.color[0].color_Color',f'{retargetNS}:clip.chest_pivot_neg')
    mc.connectAttr(pup_ns+'spine_chest_pivot_remap.color[2].color_Color',f'{retargetNS}:clip.chest_pivot_pos')
    mc.connectAttr(pup_ns+'spine_hips_ctrl.pivot',f'{retargetNS}:clip.hip_pivot')
    mc.connectAttr(pup_ns+'spine_chest_ctrl.pivot',f'{retargetNS}:clip.chest_pivot')
    #strip namespaces?
    for ctrl in mc.listRelatives(f'{retargetNS}:retarget', pa=True, ad=True):
        ctrlname = ctrl.split(':')[-1]
        pupctrl = pup_ns+ctrlname
        if not mc.objExists(pupctrl):
            continue

        #get the position values of the target, if they're zeroed out, skip this one.
        opm = mc.listConnections(f'{ctrl}.offsetParentMatrix', source=True, destination=False)
        if not opm:
            continue
        if not mc.nodeType(opm[0]) == 'fourByFourMatrix':
            continue
        skipCount = 0
        for i in range(3):
            value = mc.getAttr(f'{opm[0]}.in3{i}')
            if isclose(value, 0):
                skipCount+=1
        if skipCount == 3:
            continue

        constraint_kwargs = {}
        if layer is True:
            layer_name = f'{retargetNS}_mocap'
            if not mc.objExists(layer_name):
                layer_name = utl.createAnimLayer(name=layer_name, override=True)
            constraint_kwargs['layer'] = layer_name
        
        if mc.getAttr(ctrl+'.constrain_rotate'):
            constraint = mc.orientConstraint(ctrl, pupctrl, **constraint_kwargs)
            mc.parent(constraint, f'{retargetNS}:constraints')
        if mc.getAttr(ctrl+'.constrain_translate'):
            constraint.extend(mc.pointConstraint(ctrl, pupctrl, **constraint_kwargs))
            mc.parent(constraint, f'{retargetNS}:constraints')

        attrs = mc.listAttr(ctrl, keyable=True) or []
        for attr in attrs:
            if mc.attributeQuery(attr, exists=True, node=pupctrl) and not mc.listConnections(f'{pupctrl}.{attr}', source=True, destination=False):
                mc.connectAttr(f'{ctrl}.{attr}', f'{pupctrl}.{attr}')



def bake_puppet(retargetNS=None):

    if not retargetNS:
        sel = mc.ls(sl=True)
        if not sel:
            return
        if not ':' in sel[0]:
            return
        retargetNS = sel[0].split(':')[0]
        if not mc.objExists(retargetNS+':constraints'):
            return
        
    constraints = mc.listRelatives(retargetNS+':constraints', pa=True)
    ctrls = []
    for constraint in constraints:
        # Get the constrained objects (controls) from the constraint
        try:
            constrained = mc.listConnections(f'{constraint}.constraintRotateX', destination=True, source=False)
        except:
            pass
        if not constrained:
            constrained = mc.listConnections(f'{constraint}.constraintTranslateX', destination=True, source=False)
        if constrained:
            ctrl = constrained[0].split('.')[0]  # Get the node name without attribute
            if ctrl not in ctrls:
                ctrls.append(ctrl)

    
    start, end = _get_range(retargetNS+':clip')

    mc.bakeResults(ctrls, 
                   simulation=True, 
                   time=(start,end), 
                   sampleBy=1, 
                   disableImplicitControl=True)

    mc.delete(constraints)

    #do fk/ik matching

    pupNS = ctrls[0].split(':')[0]
    grps = []
    for a in ['Lf','Rt']:
        for b in ['arm','leg']:
            grps.append(f'{pupNS}:{a}_{b}_grp')
    
    systems = ml_match.get_systems(grps)
    for system in systems:
        if not system.driver.endswith('.fk_ik'):
            continue
        system.match_range(1)

def _get_range(node):
    while True:
        times = mc.keyframe(node, query=True, timeChange=True)
        if times:
            break
        node = mc.listRelatives(node, pa=True, shapes=False)
        if node:
            node = node[0]
        else:
            return None

    times = sorted(times)
    return times[0], times[-1]


if __name__ == '__main__':
    import_mocap()