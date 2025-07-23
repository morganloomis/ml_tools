import math, warnings, os
import maya.cmds as mc
import maya.mel as mm
import maya.api.OpenMaya as om
import ml_utilities as utl
import ml_snap, ml_copyAnim
from math import isclose
import time

uiUnit = om.MTime.uiUnit()

from importlib import reload

SKELETON_LOOKUP = {'Hip':['hips'],
                    'Chest':['spine1'],
                    'Neck':['neck'],
                    'Head':['head'],
                    'LeftShoulder':['leftarm'],
                    'RightShoulder':['rightarm'],
                    'LeftElbow':['leftforearm'],
                    'RightElbow':['rightforearm'],
                    'LeftHand':['lefthand'],
                    'RightHand':['righthand'],
                    'LeftHip':['leftuppleg'],
                    'RightHip':['rightupleg'],
                    'LeftKnee':['leftleg'],
                    'RightKnee':['rightleg'],
                    'LeftFoot':['leftfoot'],
                    'RightFoot':['rightfoot']
                    }



SIDE_LOOKUP = ['Center','Left','Right']
LABEL_LOOKUP = ['None',
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


#######################################################
## RETARGETTING
#######################################################

def get_orientation_offset(joint, relativeMatrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]):
    relativeMatrix = relativeMatrix[:12]+[0,0,0,1]
    inverseMatrix = om.MMatrix(relativeMatrix).inverse()

    jointMatrix = ml_snap.get_worldMatrix(joint)
    jointMatrix = om.MMatrix(jointMatrix[:12]+[0,0,0,1])

    matrix = jointMatrix * inverseMatrix

    r = om.MTransformationMatrix(matrix).rotation(asQuaternion=False)
    offset = [math.degrees(x) for x in r]


def tag_joint(key):

    joint = None
    joints = mc.ls(type='joint')
    
    side = 'Center'
    label = key
    for each in SIDE_LOOKUP:
        if key.startswith(each):
            label = key.replace(each, '')
            side = each
            break

    for each in SKELETON_LOOKUP[key]:
        for j in joints:
            if j.endswith(each):
                joint = j
                break
        if joint:
            break
    if not joint:
        print(f'Joint not found: {side} {label}')
        return

    print(f'{side} {label}: {joint}')
    mc.setAttr(joint+'.side', SIDE_LOOKUP.index(side))
    mc.setAttr(joint+'.type', LABEL_LOOKUP.index(label))
    return joint


def joint_from_label(side, label, root=None):
    joints = []
    if root and mc.objExists(root):
        joints = mc.listRelatives(root, ad=True, pa=True, type='joint')
    else:
        joints = mc.ls(type='joint')
    for joint in joints:
        sideIdx = mc.getAttr(joint+'.side')
        if side == SIDE_LOOKUP[sideIDx]:
            typeIdx = mc.getAttr(joint+'.type')
            if label == LABEL_LOOKUP[typeIDx]:
                return joint



def tag_skeleton(root):
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


def connect_skeleton_to_retarget_node(retarget, root=None):

    shape = mc.listRelatives(retarget, shapes=True)[0]
    joints = []
    if root and mc.objExists(root):
        joints = mc.listRelatives(root, ad=True, pa=True, type='joint')
        joints.append(root)
    else:
        joints = mc.ls(type='joint')

    for joint in joints:
        side = SIDE_LOOKUP[mc.getAttr(joint+'.side')]
        label = LABEL_LOOKUP[mc.getAttr(joint+'.type')]
        attr = f'{side}_{label}'
        if not mc.attributeQuery(attr, exists=True, node=shape):
            continue
        
        pmm = mc.createNode('pointMatrixMult', name=attr+'_Point')
        mc.connectAttr(joint+'.worldMatrix[0]', pmm+'.inMatrix')
        mc.connectAttr(pmm+'.output', f'{shape}.{attr}')

        for a in 'XYZ':
            aa = f'{attr}_{a}'
            if mc.attributeQuery(aa, exists=True, node=shape):
                pick = attr+'_Ori'
                if not mc.objExists(pick):
                    pick = mc.createNode('pickMatrix', name=attr+'_Ori')
                    mc.setAttr(f'{pick}.useTranslate', 0)
                    mc.setAttr(f'{pick}.useScale', 0)
                    mc.setAttr(f'{pick}.useShear', 0)
                    mc.connectAttr(joint+'.worldMatrix[0]', pick+'.inputMatrix')
                
                pmm = mc.createNode('pointMatrixMult', name='{attr}_{a}_Vector')
                mc.setAttr(f'{pmm}.inPoint{a}', 1)
                mc.connectAttr(f'{pick}.outputMatrix', f'{pmm}.inMatrix')
                mc.connectAttr(pmm+'.output', f'{shape}.{aa}')

def constrain_puppet_to_retarget(puppet, retarget, layer=None):

    def _distance(a,b):
        pa = utl.Vector(ml_snap.get_worldPosition(a))
        pb = utl.Vector(ml_snap.get_worldPosition(a))
        v = pa-pb
        return v.mag()
        
    pup_ns = puppet.rsplit(':',1)[0]
    if pup_ns:
        pup_ns = pup_ns+':'


    #set settings
    thigh = _distance(pup_ns+'Lf_leg_fk1_ctrl',pup_ns+'Lf_leg_fk2_ctrl')
    shin = _distance(pup_ns+'Lf_leg_fk2_ctrl',pup_ns+'Lf_leg_fk3_ctrl')
    hips = _distance(pup_ns+'Lf_leg_fk1_ctrl',pup_ns+'Rt_leg_fk1_ctrl')

    mc.setAttr('settings.thighLength', thigh)
    mc.setAttr('settings.shinLength', shin)
    mc.setAttr('settings.hipWidth', hips)

    #strip namespaces?
    for ctrl in mc.listRelatives(retarget):
        pupctrl = pup_ns+ctrl.split('|')[0]
        if mc.objExists(pupctrl):
            mc.orientConstraint(ctrl, pupctrl)

def import_retarget():
    
    filename = mc.fileDialog2(caption='Import FBX', 
                              fileFilter='FBX Files (*.fbx)', 
                              fileMode=1,
                              dialogStyle=1)
    if not os.path.exists(filename[0]):
        return None

    return import_fbx_as_target(filename[0])

def import_mocap():
    sel = mc.ls(sl=True)
    if not len(sel) == 1:
        raise RuntimeError('Please select a puppet')

    #some validation
    retarget = import_retarget()
    constrain_puppet_to_retarget(sel[0], retarget)


def import_fbx_as_target(fbxFile, name=None):
    
    if not name:
        name = os.path.basename(fbxFile)
        name = os.path.splitext(name)[0]
        name = name.replace('-','')

    a = mc.ls(assemblies=True)
    mc.file(fbxFile, i=True)
    ass = [x for x in mc.ls(assemblies=True) if x not in a]
    if not ass:
        raise RuntimeError('Import Failed.')
    root = None
    for a in ass:
        if mc.nodeType(a) == 'joint':
            root = a
            break
    if not root:
        for a in ass:
            x = mc.listRelatives(a, type='joint', pa=True)
            if x:
                root = x
                break

    if not root:
        raise RuntimeError('Could not determine root joint.')
        
    tag_skeleton(root)

    times = mc.keyframe(root, query=True, timeChange=True)
    start = times[0]
    end = times[-1]

    #import retarget node
    from puppeteer.snip import snip
    retarg = snip.snip('retarget', prefix=name)

    connect_skeleton_to_retarget_node(retarg.node.retarget, ass[0])

    #bake
    mc.bakeResults(retarg.node.retarget, 
                   simulation=True, 
                   time=(start,end), 
                   sampleBy=1, 
                   disableImplicitControl=True)

    mc.delete(ass)

    return retarg

if __name__ == '__main__':
    import_mocap()