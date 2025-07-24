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

SKELETON_LOOKUP = {'Hip':['Hips'],
                    'Chest':['Spine1'],
                    'Neck':['Neck'],
                    'Head':['Head'],
                    'LeftShoulder':['LeftArm'],
                    'RightShoulder':['RightArm'],
                    'LeftElbow':['LeftForeArm'],
                    'RightElbow':['RightForeArm'],
                    'LeftHand':['LeftHand'],
                    'RightHand':['RightHand'],
                    'LeftHip':['LeftUpLeg'],
                    'RightHip':['RightUpLeg'],
                    'LeftKnee':['LeftLeg'],
                    'RightKnee':['RightLeg'],
                    'LeftFoot':['LeftFoot'],
                    'RightFoot':['RightFoot']
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


def tag_joint(joint, side, label, offset=[0,0,0]):
    print(f'{side} {label}: {joint}')
    if not mc.nodeType(joint) == 'joint':
        raise RuntimeError(f'{joint} is not a joint.')
    mc.setAttr(joint+'.side', SIDE_LOOKUP.index(side))
    mc.setAttr(joint+'.type', LABEL_LOOKUP.index(label))

    try:
        mc.addAttr(joint, ln='offset', at='double3', keyable=True)
        for x in 'XYZ':
            mc.addAttr(joint, ln='offset'+x, at='doubleAngle', parent='offset', keyable=True)
    except:
        pass

    mc.setAttr(joint+'.offset', *offset)


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

    def child_joints(joint):
        return mc.ls(mc.listRelatives(joint, f=True), type='joint')

    def position(node):
        return ml_snap.get_worldPosition(node)
    
    def child_chains_by_length(node):
        kids = child_joints(node)
        lengths = []
        for kid in kids:
            lengths.append(len(mc.listRelatives(kid, ad=True, type='joint')))
        return [x for _,x in sorted(zip(lengths,kids))]
    
    def shortest_child_chain(node):
        return child_chains_by_length(node)[0]
    
    def longest_child_chain(node):
        return child_chains_by_length(node)[-1]

    def first_branching_joint(root, limit=2, depth=2):
        joint = root
        kids = child_joints(joint)
        while kids:
            if len(kids) >= limit:
                return joint
            joint = kids[0]
            kids = child_joints(joint)
        return None

    def leaf_joint(root, keyed=False):
        kids = [root]
        prev = root
        joint = root

        while True:
            prev = joint
            joint = kids[0]
            kids = child_joints(joint)
            if not kids:
                if keyed and not mc.keyframe(joint, time=(':',), query=True, keyframeCount=True):
                    return prev
                else:
                    return joint
            
    def bone_length(end):
        parent = mc.listRelatives(end, parent=True, f=True)
        p1 = utl.Vector(*position(end))
        if not parent:
            return p1.magnitude()
        p2 =  utl.Vector(*position(parent[0]))
        vec = p1 - p2
        return vec.magnitude()
    
    def chain_length(root, end):
        totalLength = bone_length(end)
        parent = mc.listRelatives(end, parent=True, f=True)
        while parent and not utl.sameNode(root, parent[0]):
            totalLength += bone_length(parent[0])
            parent = mc.listRelatives(parent[0], parent=True, f=True)
        return totalLength
    
    def outlier_child(root):
        #get the mean of all child positions. The one that's farthest away from mean is thumb.
        points = {}
        kids = mc.listRelatives(root, type='joint', pa=True)
        count = len(kids)
        for kid in kids:
            points[kid] = utl.Vector(*mc.getAttr(kid+'.translate')[0])
        
        mean = utl.Vector(0,0,0)
        for point in points.values():
            mean+=point
        mean = mean/count

        outlier = kids[0]
        maxDist = 0
        for kid, point in points.items():
            dist = (mean-point).magnitude()
            if dist > maxDist:
                outlier = kid
                maxDist = dist

        return outlier
    
    def order_by_distance(list, target):
        result = []
        pass
          
    hip = first_branching_joint(root)

    #go to start frame, best chance of being a t pose.

    keyTimes = mc.keyframe(hip, query=True, timeChange=True)
    if not keyTimes:
        raise RuntimeError('No animation on skeleton?')
    keyTimes = sorted(list(set(keyTimes)))
    mc.currentTime(int(keyTimes[0]))
    mc.refresh()

    #assume we're at bind pose.
    #get the offset between this and our default spine control (world oriented)
    #assume this same offset is continued through the spine, neck and head
    matrix = ml_snap.get_worldMatrix(hip)
    r = om.MTransformationMatrix(om.MMatrix(matrix[:12]+[0,0,0,1])).rotation(asQuaternion=False)
    offset = [math.degrees(x) for x in r]

    tag_joint(hip, 'Center', 'Hip', offset=offset)
    

    hipChains = child_chains_by_length(hip)
    chest = first_branching_joint(hipChains[-1])
    tag_joint(chest, 'Center', 'Spine', offset=offset)

    #get the position of all chest child joints, the 
    chestChains = child_joints(chest)
    if len(chestChains) != 3:
        raise RuntimeError(f'Chest "{chest}" has more or less than 3 children, cannot determine biped hierarchy.')
    chestData = []
    for c in chestChains:
        chestData.append(sum([abs(mc.getAttr(f'{c}.t{x}')) for x in 'xyz']))
    neck = None
    if isclose(chestData[0], chestData[1], abs_tol=0.01):
        neck = chestChains[2]
    elif isclose(chestData[0], chestData[2], abs_tol=0.01):
        neck = chestChains[1]
    elif isclose(chestData[1], chestData[2], abs_tol=0.01):
        neck = chestChains[0]
    else:
        raise RuntimeError('Could not determine neck joint')

    tag_joint(neck, 'Center', 'Neck', offset=offset)

    head = None
    if neck:
        head = leaf_joint(neck, keyed=True)
    else:
        head = shortest_child_chain(chest)
    tag_joint(head, 'Center', 'Head', offset=offset)

    LfClav = None
    RtClav = None
    chestChains.remove(neck)

    #left clav will be one of these, based which side of the chest its on?
    chest_pos = ml_snap.get_worldPosition(chest)
    for clav in chestChains:
        kid = child_joints(clav)[0]
        position = ml_snap.get_worldPosition(kid)
        vect = [a-b for a,b in zip(position,chest_pos)]
        vect = utl.Vector(*position) - utl.Vector(*chest_pos)
        vect.normalize()
        if vect.dot(utl.Vector(1,0,0)) > 0:
            LfClav = clav
            break
    
    if LfClav == chestChains[-1]:
        RtClav = chestChains[-2]
    else:
        RtClav = chestChains[-1]

    tag_joint(LfClav, 'Left', 'Collar')
    tag_joint(RtClav, 'Right', 'Collar')

    for clav, side in zip([LfClav, RtClav],['Left','Right']):
        shoulder = child_joints(clav)[0]
        tag_joint(shoulder, side, 'Shoulder')

        hand = first_branching_joint(shoulder)
        tag_joint(hand, side, 'Hand')

        elbow = child_joints(shoulder)[0]
        tag_joint(elbow, side, 'Elbow')

        if not hand:
            hand = leaf_joint(shoulder, keyed=True)
        else:
            #do fingers
            thumb = outlier_child(hand)
            tag_joint(thumb, side, 'Thumb')

    LfHip = None
    RtHip = None

    #left clav will be one of these, based which side of the chest its on?
    hip_pos = ml_snap.get_worldPosition(hip)
    for each in hipChains[:2]:
        position = ml_snap.get_worldPosition(each)
        vect = [a-b for a,b in zip(position,hip_pos)]
        vect = utl.Vector(*position) - utl.Vector(*hip_pos)
        vect.normalize()
        if vect.dot(utl.Vector(1,0,0)) > 0:
            LfHip = each
            break
    
    if LfHip == hipChains[0]:
        RtHip = hipChains[1]
    else:
        RtHip = hipChains[0]

    tag_joint(LfHip, 'Left', 'Hip')
    tag_joint(RtHip, 'Right', 'Hip')

    for each, side in zip([LfHip, RtHip],['Left','Right']):
        knee = child_joints(each)[0]
        tag_joint(knee, side, 'Knee')

        foot = child_joints(knee)[0]
        tag_joint(foot, side, 'Foot')

        toe = child_joints(foot)[0]
        tag_joint(toe, side, 'Toe')


    mc.select(hip)
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
        return

    import_fbx_as_target(filename[0])

def import_mocap():
    sel = mc.ls(sl=True)
    if not len(sel) == 1:
        raise RuntimeError('Please select a puppet')

    #some validation
    import_retarget()
    constrain_puppet_to_retarget(puppet, retarget)


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

    