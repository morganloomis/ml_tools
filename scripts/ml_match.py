import math, warnings
import maya.cmds as mc
import maya.mel as mm
import maya.api.OpenMaya as om
import ml_utilities as utl
import ml_snap, ml_copyAnim
from math import isclose
import time

uiUnit = om.MTime.uiUnit()

TARGET_ATTR = 'pup_matchTarget'
TAG_ATTR = 'pup_matchTag'
OFFSET_ATTR = 'pup_matchOffset'

from importlib import reload
reload(ml_snap)

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


def get_matrix_data(matrices, start=None, end=None):
    '''
    Should hopefully get matrix values for every frame quickly.
    '''
    data = {}
    start, end = utl.frameRange(start=start, end=end)

    if not isinstance(matrices, (list, tuple)):
        matrices = [matrices]

    plugs = {}
    for matrix in matrices:
        obj, attr = matrix.split('.')

        index = None

        if '[' in attr:
            attr, x = attr.split('[')
            index = int(x.split(']')[0])

        data[matrix] = {}

        mSel = om.MSelectionList()
        mSel.add(obj)
        node = om.MFnDependencyNode(mSel.getDependNode(0))
        plug = node.findPlug(attr, False)

        if index is not None:
            plug.evaluateNumElements()
            plug = plug.elementByPhysicalIndex(index)

        plugs[matrix] = plug

    for f in range(int(start), int(end+1)):
        timeContext = om.MDGContext(om.MTime(f, uiUnit))
        for matrix, plug in plugs.items():
            matrixMObj = plug.asMObject(timeContext)
            matrixData = om.MFnMatrixData(matrixMObj)
            matrixValue = matrixData.matrix()
            data[matrix][f] = matrixValue

    return data


def test_matrix_data(nodes):

    start, end = utl.frameRange()

    data = get_matrix_data(nodes)

    locators = [mc.spaceLocator(name='test_{}'.format(x))[0] for x in nodes]

    for f in range(int(start), int(end+1)):
        mc.currentTime(f)
        for control, target in zip(locators, nodes):
            ml_snap.set_worldMatrix(control, data[target][f])
            mc.setKeyframe(control)


def compare_matrix(m1, m2, tol=0.001):
    return [isclose(x1, x2, abs_tol=tol) for x1, x2 in zip(m1, m2)] == ([True] * 16)


def get_local_delta(node, targetMatrix):
    
    nodeWM = om.MMatrix(mc.getAttr(node+'.worldMatrix[0]'))
    inv = om.MMatrix(targetMatrix).inverse()
    return nodeWM * inv


def get_control_label(node):
    label = mc.listConnections(node+'.message', type='controller', source=False, destination=True)
    if not label:
        return None
    return label[0]


def get_systems(controls):
    '''
    Returns the match system for the given node.
    '''

    systems = []
    for ctrl in controls:
        cons = mc.listConnections(ctrl+'.message', source=False, destination=True, type='network') or []
        for con in cons:
            if con not in systems and mc.attributeQuery('puppeteerDataMatch', exists=True, node=con):
                systems.append(con)
    
    return [MatchSystem(x) for x in systems]


class MatchSystem(object):
    '''
    Manages matching for a system embedded in a puppet.
    '''

    def __init__(self, matchNode):

        self.system = matchNode
        self.driver = mc.listConnections(self.system+'.driver', source=True, destination=False, plugs=True)[0]
        if not self.driver:
            raise RuntimeError('No driver found for match system: {}'.format(self.system))

        self._offset = []

    def set_frozen(self, value):
        mc.setAttr(self.system+'.freeze', value)
        if not value:
            #refresh the current frame to run the match expression
            mc.currentTime(mc.currentTime(query=True))

    @property
    def dynamic(self):
        if mc.attributeQuery('dynamic', exists=True, node=self.system):
            return mc.getAttr(self.system+'.dynamic')
        return False

    @property
    def controls(self):
        return mc.listConnections(self.system+'.control', source=True, destination=False)

    @property
    def targets(self):
        '''return all targets in the system'''
        targets = []
        for i in range(mc.getAttr(self.system+'.target', size=True)):
            targets.append(mc.connectionInfo('{}.target[{}]'.format(self.system, i), sourceFromDestination=True))
        return targets
    
    @property
    def offsets(self):
        '''return offsets for all targets in the system'''
        if not self._offset:
            size = mc.getAttr(self.system+'.offset', size=True)
            for i,x in enumerate(self.targets):
                if i >= size:
                    self._offset.append([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])
                else:
                    self._offset.append(mc.getAttr(self.system+'.offset[{}]'.format(i)))
        return self._offset

    def match_current(self, newValue):
        '''
        Run a match on the current frame.
        '''
        self.set_frozen(0)
        matrices = [mc.getAttr(x) for x in self.targets]
        mc.setAttr(self.driver, newValue)
        for control, matrix, offset in zip(self.controls, matrices, self.offsets):
            ml_snap.set_worldMatrix(control, matrix, offsetMatrix=offset)

        self.set_frozen(1)
        
    def match_range(self, newValue, start=None, end=None):
        '''
        Match a frame range by stepping through time.
        '''
        
        current = mc.currentTime(query=True)
        start, end = utl.frameRange(start=start, end=end)

        #get all the matrices for the targets in its current state
        self.set_frozen(0)
        matrix_data = get_matrix_data(self.targets, start=start, end=end)

        #then change to the new state.
        mc.cutKey(self.driver, time=(start, end), includeUpperBound=False)
        mc.setKeyframe(self.driver, time=(start,end), value=newValue)

        #and snap
        resetAutoKey = mc.autoKeyframe(query=True, state=True)
        mc.autoKeyframe(state=False)
        if not self.dynamic and not mc.ogs(query=True, pause=True):
            mc.ogs(pause=True)
        
        for f in range(int(start), int(end+1)):
            mc.currentTime(f)
            for control, target, offset in zip(self.controls, self.targets, self.offsets):
                ml_snap.set_worldMatrix(control, matrix_data[target][f], offsetMatrix=offset)
                mc.setKeyframe(control)

        if mc.ogs(query=True, pause=True):
            mc.ogs(pause=True)

        self.set_frozen(1)
        mc.currentTime(current)
        mc.autoKeyframe(state=resetAutoKey)

    def match_range_fast(self, start=None, end=None):
        '''Match a frame range by determining keys.
        Get matrices and determine local key values for each level of order.'''
        pass

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

    def first_branching_joint(root, limit=2):
        joint = root
        kids = child_joints(joint)
        while kids:
            if len(kids) >= limit:
                return joint
            joint = kids[0]
            kids = child_joints(joint)
        return None

    def leaf_joint(root):
        kids = [root]
        while True:
            joint = kids[0]
            kids = child_joints(joint)
            if not kids:
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

    chestChains = child_chains_by_length(chest)

    neck = chestChains[0]
    tag_joint(neck, 'Center', 'Neck', offset=offset)

    head = None
    if neck:
        head = leaf_joint(neck)
    else:
        head = shortest_child_chain(chest)
    tag_joint(head, 'Center', 'Head', offset=offset)

    LfClav = None
    RtClav = None

    #left clav will be one of these, based which side of the chest its on?
    chest_pos = ml_snap.get_worldPosition(chest)
    for clav in chestChains[-2:]:
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


class MatchSkeleton(object):
    '''
    Skeleton representation, no puppet.
    Relies on pre-tagged joints, using the standard .type and .side attributes of joints
    '''
    sides = ['','Right','Left']

    def __init__(self, origin):

        #check that skeleton is tagged, and tag if not.

        self.origin = origin
        self.namespace = utl.getNamespace(origin)

        #data is formatted like this:
        self.data = {} 
        self._joints = []
        self._targets = {}
        self._matrixData = {}
        self._startFrame = None
        self._endFrame = None
        self._targets = []
        self._tags = {}

    @property
    def joints(self):
        if not self._joints:
            self._joints = mc.ls(mc.listRelatives(self.origin, f=True, ad=True), type='joint')
            self._joints.append(self.origin)
        return self._joints
    
    def get_joint(self, name):
        if self.namespace:
            name = self.namespace+':'+name
        joint = mc.ls(name)
        if joint:
            return joint[0]
    
    def find_joint(self, label, side):
        key = (label, side)
        if key in self._tags.keys():
            return self._tags[key]
        
        for joint in self.joints:
            t = mc.getAttr(f'{joint}.type')
            if t == 0:
                continue
            s = mc.getAttr(f'{joint}.side')
            self._tags[(LABEL_LOOKUP[t], SIDE_LOOKUP[s])] = joint
            if t == label and s == side:
                return joint

    def get_target(self, label, side):
        '''
        This is the main method for getting a target joint in a skeleton
        '''
        joint = self.find_joint(label, side)

        if not joint:
            return None
        #need to determine orientation offset?
        return TargetTransform(node=joint)
    
    @property
    def target_nodes(self):
        return [x.node for x in self._targets.values()]

    def matrix_data(self):
        return get_matrix_data(self.target_nodes, start=self.start_frame, end=self.end_frame)

    def frame_range(self):
        if not self._startFrame:
            keyTimes = mc.keyframe(self.joints, query=True, timeChange=True)
            if not keyTimes:
                return None
            keyTimes = sorted(list(set(keyTimes)))
            self._startFrame = int(keyTimes[0])
            self._endFrame = int(keyTimes[-1])
        return self._startFrame, self._endFrame

    def start_frame(self):
        return self.frame_range()[0]
    
    def end_frame(self):
        return self.frame_range()[1]
    


class MatchPuppet(object):

    def __init__(self, namespace):
        self.namespace = namespace
        self._refNode = None
        self._topNode = None
        self._controls = None
        self._appendages = None
        self._ordered_controls = None
        self._matchable_controls = None
        self._systems = None
        
    @property
    def controls(self):
        #this is yanked from ml_puppet (cyclical import otherwise)
        if not self._controls:
            self._controls = mc.ls('{}:*.pupID_control'.format(self.namespace), o=True)
        return self._controls
    
    @property
    def appendages(self):
        #this is yanked from ml_puppet (cyclical import otherwise)
        if not self._appendages:
            self._appendages = mc.ls('{}:*.puppeteer_appendage'.format(self.namespace), o=True, long=True)
        return self._appendages
    
    @property
    def topNode(self):
        if not self._topNode:
            pups = mc.ls('{}:*.pupID_puppet'.format(self.namespace), o=True)
            if not pups:
                warnings.warn('No top node attribute detected in namespace, or namespace is incorrect.')
            else:
                self._topNode = pups[0]
        return self._topNode
                
    @property
    def refNode(self):
        if not self._refNode:
            self._refNode = mc.referenceQuery(self.controls[0], referenceNode=True)
        return self._refNode
    
    @property
    def refFile(self):
        return mc.referenceQuery(self.refNode, filename=True)
    
    @property
    def root(self):
        return self.control('root_ctrl')
    
    @property
    def systems(self):
        if not self._systems:
            self._systems = get_systems(self.controls)
        return self._systems
    
    @property
    def fk_ik_systems(self):
        return [s for s in self.systems if s.driver.endswith('.fk_ik')]

    def control(self, name):
        return self.namespace+':'+name
    
    def swap_reference(self, newFile):
        mc.file(newFile, loadReference=self.refNode)

    def remove_reference(self):
        refNode = self.refNode
        mc.file(removeReference=True, referenceNode=refNode)
        if mc.objExists(refNode):
            mc.lockNode(refNode, lock=False)
            mc.delete(refNode)

    def upstream_appendage(self, appendage):
        
        opm = mc.listConnections(f'{appendage}.offsetParentMatrix', source=True, destination=False)
        if not opm:
            parent =  mc.listRelatives(appendage, parent=True)
            if parent:
                return parent[0]
            return None
        
        upstream = None
        history = mc.ls(mc.listHistory(opm, breadthFirst=True), type='transform', long=True)
        history_control = None
        for each in history:
            if each == appendage:
                continue
            if mc.attributeQuery('puppeteer_appendage', node=each, exists=True):
                upstream = each
                break
            if not history_control and mc.attributeQuery('pupID_control', node=each, exists=True):
                history_control = each

        if not upstream and history_control:
            #get appendage above this control.
            while history_control:
                if not '|' in history_control:
                    break
                history_control = history_control.rsplit('|',1)[0]
                if not mc.objExists(history_control):
                    break
                if mc.attributeQuery('puppeteer_appendage', node=history_control, exists=True):
                    upstream = history_control
                    break
        return upstream
    
    def ordered_appendages(self):
        '''
        All appendages in order of execution.
        '''
        ordered_appendages = self.appendages[:]
        for appendage in self.appendages:
            ordered_appendages.remove(appendage)
            upstream = self.upstream_appendage(appendage)
            if not upstream or upstream not in ordered_appendages:
                ordered_appendages.insert(0, appendage)
            else:
                ordered_appendages.insert(ordered_appendages.index(upstream)+1, appendage)
        return ordered_appendages
    
    def ordered_controls(self):
        '''
        get all controls in estimated evaluation order.
        Top node is top, followed by controls directly underneath (root)
        Then order appendages based on their skeletal connections.
        Then order controls under each appendage based on if they have other 
        local controls in their upstream history.
        '''

        if self._ordered_controls:
            return self._ordered_controls

        def controls_below(node, nodeList=[]):
            '''
            '''
            kids = mc.listRelatives(node, f=True) or []
            for kid in kids:
                if not mc.listAttr(kid, keyable=True):
                    break
                if mc.attributeQuery('puppeteer_appendage', node=kid, exists=True):
                    break
                if mc.attributeQuery('pupID_control', node=kid, exists=True):
                    nodeList.append(kid)
                nodeList = controls_below(kid, nodeList)
            return nodeList
        
        #first ordred controls are always topnode and anything directly under it (root)
        ordered_controls = [self.topNode]
        ordered_controls.extend(controls_below(self.topNode, []))
        
        #now order controls in appendages
        for appendage in self.ordered_appendages():
            ordered = controls_below(appendage, [])
            if not ordered:
                continue
            if len(ordered) == 1:
                ordered_controls.append(ordered[0])
                continue

            for control in ordered[:]:
                opm = mc.listConnections(f'{control}.offsetParentMatrix', source=True, destination=False)
                if not opm:
                    continue

                for each in mc.ls(mc.listHistory(opm, breadthFirst=True), type='transform', long=True):
                    if each == control:
                        continue
                    if each in ordered:
                        ordered.remove(control)
                        ordered.insert(ordered.index(each)+1, control)
                        break

            ordered_controls.extend(ordered)
        
        self._ordered_controls = ordered_controls
        return self._ordered_controls

    def matchable_controls(self):

        if self._matchable_controls:
            return self._matchable_controls
        
        controls = []
        for control in self.ordered_controls():
            if not mc.attributeQuery('pup_matchLabel', node=control, exists=True):
                continue
            label = mc.getAttr(f'{control}.pup_matchLabel')
            if not label:
                continue
            side = mc.getAttr(f'{control}.pup_matchSide')
            aim = 'y'
            #making orientation assumption here, because it's our puppet.
            if side == -1:
                aim = '-y'
            mt = MatchTransform(control)
            controls.append(mt)
        self._matchable_controls = controls
        return self._matchable_controls
    
        
    def reference_duplicate(self):
        
        pre = mc.ls(assemblies=True)
        mc.file(self.refFile, reference=True, namespace=self.intermediateNamespace)
        post = mc.ls(assemblies=True)
        self.intermediatePuppet = [x for x in post if x not in pre][0]
        
        #parent
        parent = mc.listRelatives(self.puppet, parent=True)
        if parent:
            self.intermediatePuppet = mc.parent(self.intermediatePuppet, parent[0])[0]
        
        for src in self.all_controls():
            dst = src.replace(self.namespace, self.intermediateNamespace)
            if not mc.objExists(dst):
                warnings.warn('Warning! Puppets do not match. Control not found: {}'.format(dst))
                continue
            for attr in mc.listAttr(src, keyable=True) or []:
                if mc.getAttr('{}.{}'.format(dst, attr), lock=True):
                    continue
                    
                value = mc.getAttr('{}.{}'.format(src, attr))
                if isinstance(value, list):                
                    mc.setAttr('{}.{}'.format(dst, attr), *value[0])
                else:
                    mc.setAttr('{}.{}'.format(dst, attr), value)


class TargetTransform(object):
    '''
    A maya transform with methods for determining orientation and comparing with others
    '''
    sides = ['','Left','Right']
    
    def __init__(self, node):
        if not node:
            raise RuntimeError('No node')
        self.node = node
        self.target = None
        
    @property
    def name(self):
        return self.node.split('|')[-1].split(':')[-1]
    
    @property
    def label(self):
        try:
            return mc.getAttr(f'{self.node}.pup_matchLabel')
        except: pass
        if mc.nodeType(self.node) == 'joint':
            return mc.getAttr(f'{self.node}.type', asString=True)

    @property
    def side(self):
        try:
            return SIDE_LOOKUP[mc.getAttr(f'{self.node}.pup_matchSide')]
        except: pass
        if mc.nodeType(self.node) == 'joint':
            return mc.getAttr(f'{self.node}.side', asString=True)
        
    def worldMatrix(self):
        return ml_snap.get_worldMatrix(self.node)
    
    def worldPosition(self):
        return ml_snap.get_worldPosition(self.node)

    @property
    def aim_axis(self):
        if self._aim_axis:
            return self._aim_axis
        
        compare = mc.listRelatives(self.node) or []
        invert = -1
        if not compare:
            compare.extend(mc.listRelatives(self.node, parent=True) or [])
            invert = 1

        if not compare:
            self._aim_axis = utl.Vector(0,1,0)
            return self._aim_axis
        
        matrix = self.matrix()
        nodeWM = om.MMatrix(matrix)
        
        allAxis = [utl.Vector(1,0,0),utl.Vector(0,1,0),utl.Vector(0,0,1)]
        allAxis = allAxis + [x*-1 for x in allAxis]

        highestDot = -2
        for each in compare:
            inv = om.MMatrix(ml_snap.get_worldMatrix(each)).inverse()
            localMatrix = nodeWM * inv
            localPoint = utl.Vector(localMatrix[12],localMatrix[13],localMatrix[14])
            if localPoint.magnitude == 0:
                continue
            localPoint.normalize()
            localPoint = localPoint * invert
            
            for a in allAxis:
                dot = localPoint.dot(a)
                if dot > highestDot:
                    highestDot = dot
                    self._aim_axis = a
                if dot == 1:
                    break

        return self._aim_axis


class MatchTransform(TargetTransform):
    '''
    A maya transform with methods for determining orientation and comparing with others
    '''
    sides = ['','Left','Right']
    
    def __init__(self, node):
        super(MatchTransform, self).__init__(node)
        
    def get_target(self, targetSystem):

        if not isinstance(targetSystem, MatchSkeleton):
            raise RuntimeError(f'{type(targetSystem)} not supported, no target found.')

        joint = None
        #look for a target in three ways. First based on explicit connection
        if mc.attributeQuery('pup_matchTarget', node=self.node, exists=True):
            targetName = mc.getAttr(f'{self.node}.pup_matchTarget')
            if targetName:
                joint = targetSystem.get_joint(targetName)

        if not joint and self.name.endswith('_ctrl'):
            # second based on name, assuming the same skeleton
            #basically if we ditch the _ctrl suffix and there's a joint with the same name.
            joint = mc.ls(self.name.replace('_ctrl',''), type='joint')
        if joint:
            if len(joint) > 1:
                raise RuntimeError(f'More than one joint matches name: {self.name}')
            self.target = joint[0]
            return True

        self.target = targetSystem.get_target(self.label, self.side)
        return bool(self.target)

    def match(self):
        if not self.target:
            raise RuntimeError(f'{self.node} has no target')
        
        ml_snap.snap(self.node, self.target.node, offset=self.target_delta, position=False, iterationMax=1)


    def constrain(self, orient=True, point=False, maintainOffset=False, layer=None):
        if not self.target:
            raise RuntimeError(f'{self.node} has no target')
        
        #get the offset
        if orient:
            mc.orientConstraint(self.target.node, self.node, maintainOffset=maintainOffset)

    
    def delta_matrix(self, other):

        if not isinstance(other, MatchTransform):
            raise TypeError('Must align to another MatchTransform object.')
        #build an offset matrix based on the difference between the two vectors

        angle = math.acos(self.aim_axis.dot(other.aim_axis)) * -1
        axis = self.aim_axis.cross(other.aim_axis).normalized()

        # Step 2: Compute the components of the rotation matrix
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        one_minus_cos = 1 - cos_theta

        # Construct the rotation matrix
        rot_matrix = [
            cos_theta + axis[0] ** 2 * one_minus_cos,
            axis[0] * axis[1] * one_minus_cos - axis[2] * sin_theta,
            axis[0] * axis[2] * one_minus_cos + axis[1] * sin_theta,
            0,

            axis[0] * axis[1] * one_minus_cos + axis[2] * sin_theta,
            cos_theta + axis[1] ** 2 * one_minus_cos,
            axis[1] * axis[2] * one_minus_cos - axis[0] * sin_theta,
            0,

            axis[0] * axis[2] * one_minus_cos - axis[1] * sin_theta,
            axis[1] * axis[2] * one_minus_cos + axis[0] * sin_theta,
            cos_theta + axis[2] ** 2 * one_minus_cos,
            0,

            0,0,0,1
        ]

        return rot_matrix

    @property
    def target_delta(self):
        if not self._target_delta:
            if not self.target:
                raise RuntimeError('No target set yet.')
            matrix = om.MMatrix(self.orientationMatrix).inverse() * om.MMatrix(self.target.orientationMatrix)
            self._target_delta = [x for x in matrix]
        return self._target_delta

    def axis(self, a):
        result = [0,0,0]
        for i,x in enumerate('xyz'):
            if x in a:
                result[i] = -1 if a.startswith('-') else 1
        return utl.Vector(*result)
    
    @property
    def orientationMatrix(self):
        # we're only using this matrix to get a difference between two orientations. 
        # It's meaningless by itself, just an abstract representation of orientation.
        # aim aligns to the x axis, up aligns to the y axis.
        
        aim = self.axis(self.aim)
        up = self.axis(self.up)
        c = aim.cross(up)

        return [aim[0], aim[1], aim[2], 0,
                up[0],  up[1],  up[2], 0,
                c[0],   c[1],   c[2], 0,
                0,0,0,1]
                
    def offset(self, other):
        return self.orientationMatrix * other.orientationMatrix.inverse()

    def initialize_delta(self, position=False):
        '''
        Set an arbitrary offset between this control and the target on the current frame.
        '''
        if not self.target:
            raise RuntimeError('No target set yet.')
        mc.refresh()
        matrix = om.MMatrix(self.worldMatrix()).inverse() * om.MMatrix(self.target.worldMatrix()).inverse()
        matrix = [x for x in matrix]
        if not position:
            matrix[12] = 0
            matrix[13] = 0
            matrix[14] = 0
            matrix[15] = 1

        self._target_delta = matrix
    
    
def joint_axis(joint):
    kids = mc.listRelatives(joint, type='joint', f=True)
    for kid in kids:
        translate = mc.getAttr(kid+'.translate')[0]

        if abs(sum(translate)) < 0.01:
            continue

        absTrans = [abs(x) for x in translate]
        index = absTrans.index(max(absTrans))

        axis = [0,0,0]
        axis[index] = 1 if translate[index] > 0 else -1


def reference_swap_match(namespace, newPath, skipMatch=[], debug=False):
    #create a duplicate of the reference.
    #match all controls to new, higher version puppet, baked on ones
    #update old reference to new reference.
    #compare all controls hierarchically, starting at top node.
    #    if match, skip
    #    if constrained or connected, skip
    #    if in a layer, add a new offset layer? (skip for starters)
    #    if not match, transfer anim. Check match again.
    #       if not match again, do a per-frame snap

    #get the reference path of the existing puppet
    pup = MatchPuppet(namespace)
    
    #reference the new path.
    temp = 'TEMP'
    namespaces = mc.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    i = 1
    while temp in namespaces:
        temp = '{}{}'.format(temp,i)
        i+=1
    mc.file(newPath, r=True, namespace=temp, mergeNamespacesOnClash=True)
    tempPup = MatchPuppet(temp)

    match_puppet_to_puppet(namespace, temp, skipMatch=skipMatch)

    if not debug:
        #update the first puppet to the same file.
        pup.swap_reference(newPath)

        #copy animation to first puppet
        ml_copyAnim.copyHierarchy(tempPup.topNode, pup.topNode, rotateOrder=True)

        tempPup.remove_reference()
    

def match_puppet_to_puppet(sourceNS, destinationNS, skipMatch=[]):
    '''
    Match a puppet to another puppet of the same kind, accounting for minor differences.
    '''
    #compare all controls hierarchically, starting at top node.
    #    if match, skip
    #    if constrained or connected, skip
    #    if in a layer, add a new offset layer? (skip for starters)
    #    if not match, transfer anim. Check match again.
    #       if not match again, do a per-frame snap

    result = []

    if not isinstance(skipMatch, (list,tuple)):
        skipMatch = [skipMatch]

    src_pup = MatchPuppet(sourceNS)
    dst_pup = MatchPuppet(destinationNS)

    controls = dst_pup.ordered_controls()

    #copy pose
    for control in controls:
        controlName = control.rsplit(':', 1)[-1]
        srcControl = sourceNS+':'+controlName
        if not mc.objExists(srcControl):
            continue
        ml_snap.copy_values(srcControl, control)

    #copy animation
    ml_copyAnim.copyHierarchy(src_pup.topNode, dst_pup.topNode, rotateOrder=False)

    #now check for mismatches after copying
    match_controls = []
    for dest_ctrl in controls:
        shortName = dest_ctrl.rsplit(':',1)[-1]

        if shortName in skipMatch:
            result.append(f'Skipping: {shortName}')
            continue

        src_ctrl = mc.ls(f'{sourceNS}:{shortName}', long=True)
        
        if not src_ctrl:
            result.append(f'No Match: {shortName}')
            continue

        src_ctrl = src_ctrl[0]

        #is this a transformable control:
        attrs = mc.listAttr(dest_ctrl, keyable=True)
        if not [x for x in attrs if 'translate' in x or 'rotate' in x]:
            continue

        #check worldspace position
        src_ws = ml_snap.get_worldMatrix(src_ctrl)
        dest_ws = ml_snap.get_worldMatrix(dest_ctrl)

        if compare_matrix(src_ws, dest_ws):
            continue
        
        match_controls.append([src_ctrl, dest_ctrl])

    if not match_controls:
        return
    
    #now walk through the frame range to do the match for anything that didn't transfer

    current = mc.currentTime(query=True)
    start = current
    end = current
    keyTimes = mc.keyframe([x[0] for x in match_controls], query=True, timeChange=True)
    if keyTimes:
        keyTimes = sorted(list(set(keyTimes)))
        start = int(keyTimes[0]-0.5)
        end = int(keyTimes[-1]+1)

    #match everything on the first frame to pare down the list again.
    mc.currentTime(start)
    final_match = []
    for src_ctrl, dest_ctrl in match_controls:
        
        src_ws = ml_snap.get_worldMatrix(src_ctrl)
        dest_ws = ml_snap.get_worldMatrix(dest_ctrl)
        if compare_matrix(src_ws, dest_ws):
            continue
        ml_snap.set_worldMatrix(dest_ctrl, src_ws)
        mc.setKeyframe(dest_ctrl)
        final_match.append([src_ctrl, dest_ctrl])

    for each in final_match:
        result.append('Force Match: {}'.format(each[1]))
        for a in 'tr':
            for b in 'xyz':
                try:
                    mc.cutKey('{}.{}{}'.format(each[1], a, b))
                except:
                    pass

    for f in range(start+1, end):
        mc.currentTime(f)
        for src_ctrl, dest_ctrl in final_match:
            src_ws = ml_snap.get_worldMatrix(src_ctrl)
            ml_snap.set_worldMatrix(dest_ctrl, src_ws)
            mc.setKeyframe(dest_ctrl)

    mc.currentTime(current)
    print('== RESULT ====================')
    for line in result:
        print(line)


def retarget_puppet_to_puppet():
    pass

def match_puppet_to_skeleton():
    pass

def retarget_puppet_to_skeleton(namespace, skeleton, startFrame=None, endFrame=None, constrain=False):
    
    puppet = MatchPuppet(namespace)
    skeleton = MatchSkeleton(skeleton)

    for control in puppet.matchable_controls():
        control.get_target(skeleton)

    for system in puppet.fk_ik_systems:
        mc.setAttr(system.driver, 0)

    mc.currentTime(skeleton.start_frame())
    for control in puppet.matchable_controls():
        if control.label == 'Foot':
            control.initialize_delta()

    startFrame = startFrame or skeleton.start_frame()
    endFrame = endFrame or skeleton.end_frame()

    with utl.IsolateViews():
        for f in range(startFrame, endFrame):
            mc.currentTime(f)

            #do the root control orientation first. Only RY
            lf_hip = utl.Vector(*ml_snap.get_worldPosition(skeleton.LeftHip))
            rt_hip = utl.Vector(*ml_snap.get_worldPosition(skeleton.RightHip))
            p = (lf_hip + rt_hip) / 2
            x = lf_hip - rt_hip
            x.normalize()
            z = x.cross(utl.Vector(0,1,0))
            root_matrix = [x[0],x[1],x[2],0, 
                            0,1,0,0, 
                            z[0],z[1],z[2],0, 
                            p[0],p[1],p[2],1 ]
            ml_snap.set_worldMatrix(puppet.root, root_matrix)
            mc.setKeyframe(puppet.root)

            lowestY = float('inf')
            lowestTarget = None
            lowestControl = None
            for control in puppet.matchable_controls():
                if not control.target:
                    continue
                
                control.match()
                mc.setKeyframe(control.node+'.rotate')
                    

def constrain_puppet_to_skeleton(namespace, skeleton, startFrame=None, endFrame=None, constrain=False):
    
    puppet = MatchPuppet(namespace)
    skeleton = MatchSkeleton(skeleton)

    for system in puppet.fk_ik_systems:
        mc.setAttr(system.driver, 0)

    mc.currentTime(skeleton.start_frame())
    startFrame = startFrame or skeleton.start_frame()
    endFrame = endFrame or skeleton.end_frame()
    
    for control in puppet.matchable_controls():
        target = control.get_target(skeleton)
        if target:
            print(f'{control.node.split("|")[-1]} \t-> {control.target.node}')
            control.constrain()
