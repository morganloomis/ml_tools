import math
import maya.cmds as mc
import maya.api.OpenMaya as om
import ml_utilities as utl
import ml_puppet as pup

uiUnit = om.MTime.uiUnit()

def get_matrix_data(matrices, start=None, end=None):
    '''
    Should hopefully get matrix values for every frame quickly.
    '''

    data = {}
    start, end = utl.frameRange(start=start, end=end)

    plugs = []
    for matrix in matrices:
        obj, attr = matrix.split('.')
        data[matrix] = {}
        obj = om.MGlobal.getSelectionListByName(obj).getDependNode(0)
        objMfn = om.MFnDependencyNode(obj)
        plug = objMfn.findPlug(attr, False)
        plugs.append(plug)

    values = []
    for f in range(start, end+1):
        mdg = om.MDGContext(om.MTime(f, uiUnit))
        for plug in plugs:
            values.append(plug.asDouble(mdg))

    return data


def get_local_delta(node, targetMatrix):
    
    nodeWM = om.MMatrix(mc.getAttr(node+'.worldMatrix[0]'))
    inv = om.MMatrix(targetMatrix).inverse()
    delta = nodeWM * inv
    return delta


def match_transform(node, transform):
    pass


def match_matrix(node, matrix):
    '''
    match a transform to a given world matrix.
    '''

    nodeWM = om.MMatrix(mc.getAttr(node+'.worldMatrix[0]'))
    inv = om.MMatrix(matrix).inverse()
    delta = nodeWM * inv
    xform = om.MTransformationMatrix(delta)

    values = {}
    values['t'] = xform.translation(om.MSpace.kObject)
    values['r'] = [math.degrees(x) for x in xform.rotation()]
    values['s'] = xform.scale()

    for a in 'trs':
        for i,b in enumerate('xyz'):
            try:
                mc.setAttr(f'{node}.{a}{b}', values[a][i])
            except:
                pass


def match_matrix_iterate(node, matrix):
    pass


class RetargetSkeleton(object):
    '''
    Determine landmarks from a mocap skeleton.
    '''

    def __init__(self, origin):
        self.origin = origin
        self.data = {}
                

    def child_joints(self, joint):
        return mc.ls(mc.listRelatives(joint, pa=True), type='joint')

    def position(self, node):
        return mc.xform(node, )

    def first_branching_joint(self, root, limit=2):
        joint = root
        kids = self.child_joints(joint)
        while kids:
            if len(kids) >= limit:
                return joint
            joint = kids[0]
            kids = self.child_joints(joint)
        return None

    def leaf_joint(self, root):
        kids = [root]
        while True:
            joint = kids[0]
            kids = self.child_joints(joint)
            if not kids:
                return joint

    @property
    def hips(self):
        if not 'hips' in self.data.keys():
            hips = self.first_branching_joint(self.origin)
            if not hips:
                raise RuntimeError('Could not determine hips.')
            self.data['hips'] = hips
        return self.data['hips']


    @property
    def chest(self):
        if not 'chest' in self.data.keys():
            kids = self.child_joints(self.hips)
            #get the highest one?
            highestValue = float('-inf')
            highestJoint = None
            for kid in kids:
                value = self.position(kid)[1]
                if value > highestValue:
                    highestValue = value
                    highestJoint = kid
            joint = highestJoint
            kids = self.child_joints(joint)
            while kids:
                if len(kids) > 1:
                    #when we find a branch, that's the chest
                    self.data['chest'] = joint
                    break
                joint = kids[0]
                kids = self.child_joints(joint)
            if not 'chest' in self.data.keys():
                raise RuntimeError('Could not determine chest.')
        return self.data['chest']


    @property
    def head(self):
        if not 'head' in self.data.keys():
            kids = self.child_joints(self.chest)
            #get the chain that's the shortest?

            shortestChain = 99999999999
            joint = None
            for kid in kids:
                chain = mc.listRelatives(kid, ad=True, pa=True)
                if len(chain) == 0:
                    #early out, if there's no kids it has to be the head.
                    self.data['head'] = kid
                    return self.data['head']

                if len(chain) < shortestChain:
                    shortestChain = len(chain)
                    joint = chain[0]
            self.data['head'] = mc.listRelatives(joint, ad=True, pa=True)[-1]
        return self.data['head']

    @property
    def LfClav(self):
        if not 'LfClavicle' in self.data.keys():
            kids = self.child_joints(self.chest)
            #get the chain that's the shortest?

            shortestChain = 99999999999
            joint = None
            for kid in kids:
                chain = mc.listRelatives(kid, ad=True, pa=True)
                if len(chain) == 0:
                    #early out, if there's no kids it has to be the head.
                    self.data['head'] = kid
                    return self.data['head']

                if len(chain) < shortestChain:
                    shortestChain = len(chain)
                    joint = chain[0]
            self.data['head'] = mc.listRelatives(joint, ad=True, pa=True)[-1]
        return self.data['head']

    @property
    def LfShoulder(self):
        if not 'LfShoulder' in self.data.keys():
            self.data['LfShoulder'] = self.child_joints(self.LfClavicle)[0]
        return self.data['LfShoulder']

    @property
    def RtShoulder(self):
        if not 'RtShoulder' in self.data.keys():
            self.data['RtShoulder'] = self.child_joints(self.RtClavicle)[0]
        return self.data['RtShoulder']

    @property
    def LfHand(self):
        if not 'LfHand' in self.data.keys():
            hand = self.first_branching_joint(self.LfShoulder)
            if hand == None:
                hand = self.leaf_joint(self.LfShoulder)
            self.data['LfHand'] = hand
        return self.data['LfHand']

    @property
    def RtHand(self):
        if not 'LfHand' in self.data.keys():
            hand = self.first_branching_joint(self.RtShoulder)
            if hand == None:
                hand = self.leaf_joint(self.RtShoulder)
            self.data['RtHand'] = hand
        return self.data['RtHand']

    @property
    def LfElbow(self):
        #walk up from hand until you hit shoulder.
        pass



class Retarget(object):
    
    def __init__(self, fromSkeleton, toPuppet):
        
        #error checking
        if not mc.referenceQuery(toPuppet, isNodeReferenced=True):
            raise RuntimeError('It is required for the puppet to be referenced for retargeting to work. Create a reference and transfer animation.')
            
        self.skeleton = fromSkeleton
        self.puppet = toPuppet
        self.namespace = self.get_namespace(self.puppet)
        self.skeleton_namespace = self.get_namespace(self.skeleton)
        refNode = mc.referenceQuery(self.puppet, referenceNode=True)
        self.referenceFile = mc.referenceQuery(refNode, filename=True)
        self.intermediatePuppet = None
        self.intermediateNamespace = 'RETARGET'
        
        
        #get skeleton frame range
        allJoints = mc.listRelatives(self.skeleton, type='joint', ad=True, pa=True)
        keyTimes = mc.keyframe(allJoints, query=True, timeChange=True)
        if not keyTimes:
            raise RuntimeError('Source skeleton has no animation.')
        keyTimes = sorted(list(set(keyTimes)))
        start = mc.playbackOptions(query=True, ast=True)
        end = mc.playbackOptions(query=True, aet=True)
        self.frame_range = (start, end)      
        
        if not refNode:
            raise RuntimeError('The puppet must be referenced.')
        if not self.namespace:
            raise RuntimeError('The puppet requires a namespace.')
        if not self.skeleton_namespace:
            raise RuntimeError('The imported FBX requires a namespace. Please re-import, or else create a namespace and add all FBX nodes to it.')
    
    def initialize_t_pose(self, frame=None):
        '''
        if the skeleton orientation is not aligned with the puppet, determine offsets here.
        '''
        if frame:
            mc.currentTime(frame)
        
        
    def reference_duplicate(self):
        
        pre = mc.ls(assemblies=True)
        mc.file(self.referenceFile, reference=True, namespace=self.intermediateNamespace)
        post = mc.ls(assemblies=True)
        self.intermediatePuppet = [x for x in post if x not in pre][0]
        
        #parent
        parent = mc.listRelatives(self.puppet, parent=True)
        if parent:
            self.intermediatePuppet = mc.parent(self.intermediatePuppet, parent[0])[0]
        
        source = mc.listRelatives(self.puppet, parent=True)
        destination = mc.listRelatives(self.intermediatePuppet, pa=True, ad=True)
        
        for src in self.all_controls(self.puppet):
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
    
    
    def all_controls(self, puppet):
        nodes = mc.listRelatives(puppet, pa=True, ad=True)
        controls = [x for x in nodes if x.endswith('_Ctrl')]
        additional = ['controls_god_C']
        for each in additional:
            controls.append(self.get_namespace(puppet)+':'+each)
        if not controls:
            raise RuntimeError('No controls found in puppet: {}'.format(puppet))
        return controls
    
    def get_node(self, node, puppet):
        return '{}:{}'.format(self.get_namespace(puppet), node)
        
    def mapped_controls(self, puppet):
        return [self.get_namespace(puppet)+':'+x for x in MAP.keys()]
    
    
    def retarget_controls(self):
        for control in MAP.keys():
            self.process_control(control)
        
            
    def process_control(self, control):
        
        retargCtrl = 'RETARGET:' + control
        data = MAP[control]
        
        if 'constrain' in data.keys():
            if 'rotateOrder' in data.keys():
                ros = ['xyz', 'yzx','zxy','xzy','yxz','zyx']
                if data['rotateOrder'] not in ros:
                    raise RuntimeError('Invalid rotate order data.')
                try:
                    rotInd = ros.index(data['rotateOrder'])
                    mc.setAttr('{}.rotateOrder'.format(retargCtrl), rotInd)
                    mc.setAttr('{}.rotateOrder'.format(self.get_node(control, self.puppet)), rotInd)
                except:
                    pass
            #error check target, this should be fixed so there's no name issues in the puppet
            resolved = self.skeleton_namespace + ':' + data['constrain']
            
            transAttr = mc.listAttr(retargCtrl, keyable=True, unlocked=True, string='translate*') or []
            rotAttr = mc.listAttr(retargCtrl, keyable=True, unlocked=True, string='rotate*') or []
            scaleAttr = mc.listAttr(retargCtrl, keyable=True, unlocked=True, string='scale*') or []
        
            rotSkip = []
            transSkip = []
            for axis in ['x','y','z']:
                if not 'translate'+axis.upper() in transAttr:
                    transSkip.append(axis)
                if not 'rotate'+axis.upper() in rotAttr:
                    rotSkip.append(axis)
            
            #add skip attrs from data
            if 'skip' in data.keys():
                for attr in data['skip']:
                    if len(attr) != 2:
                        raise RuntimeError('Retarget data problem. Skip attrs should be in format "tx"')
                    if attr[0] == 't':
                        if not attr[1] in transSkip:
                            transSkip.append(attr[1])
                    if attr[0] == 'r':
                        if not attr[1] in rotSkip:
                            rotSkip.append(attr[1])
                
        
            if not transSkip:
                transSkip = 'none'
            if not rotSkip:
                rotSkip = 'none'
            
            print('constrain {} {}'.format(retargCtrl, resolved))
            
            constraint = mc.parentConstraint(resolved, retargCtrl, skipTranslate=transSkip, skipRotate=rotSkip)[0]
            
            if 'offset' in data.keys():
                offsetAttrs = []
                for a in ['Translate','Rotate']:
                    for b in 'XYZ':
                        offsetAttrs.append('{}.target[0].targetOffset{}{}'.format(constraint,a,b))
                
                for i, attr in enumerate(offsetAttrs):
                    mc.setAttr(attr, data['offset'][i])
                    
        if 'pv' in data.keys():
            a,b,c = data['pv']
            loc = mc.spaceLocator(name = CLEANUP_PREFIX+'_PV#')[0]
            
            #temp expression to place the polevectors during playback
            expression = '''
vector $a = `xform -q -ws -rp {ns}:{a}`;
vector $b = `xform -q -ws -rp {ns}:{b}`;
vector $c = `xform -q -ws -rp {ns}:{c}`;
float $len = mag($a-$b) + mag($b-$c);
vector $mid = $a * 0.5 + $c * 0.5;
vector $pv = (unit($b - $mid) * $len * 0.8) + $mid;
{loc}.tx = $pv.x;
{loc}.ty = $pv.y;
{loc}.tz = $pv.z;
'''.format(a=a, b=b, c=c, loc=loc, ns=self.skeleton_namespace)
            mc.expression( s=expression, name=CLEANUP_PREFIX + '_EXPRESSION' )
            mc.pointConstraint(loc, retargCtrl)
        
        
    def bake(self):
        controls = self.mapped_controls(self.intermediatePuppet)
        
        with ml_utilities.IsolateViews():
            mc.bakeResults(controls, time=(self.frame_range[0],self.frame_range[1]), sampleBy=1, preserveOutsideKeys=False, simulation=True)        
        
        #delete constraints
        for control in controls:
            cons = mc.listRelatives(control, type='constraint')
            if not cons:
                continue
            for con in cons:
                if not mc.referenceQuery(con, isNodeReferenced=True):
                    mc.delete(con)
                    
    def adjust_root(self, puppet):
        '''
        bake root into each fk foot space.
        transform fk foot position to ik foot position
        blend root
        '''
        
        l_root = mc.createNode('transform', name=CLEANUP_PREFIX+'l_root')
        l_foot = mc.createNode('transform', name=CLEANUP_PREFIX+'l_foot')
        r_root = mc.createNode('transform', name=CLEANUP_PREFIX+'r_root')
        r_foot = mc.createNode('transform', name=CLEANUP_PREFIX+'r_foot')
        root = mc.createNode('transform', name=CLEANUP_PREFIX+'root')
        
        l_root = mc.parent(l_root, l_foot)[0]
        r_root = mc.parent(r_root, r_foot)[0]
        
        pup_root = self.get_node('C_spine01_Ctrl', puppet)
        
        cons = []
        
        cons.extend(mc.pointConstraint(self.get_node('lf_fk_ankle_01_Ctrl', puppet), l_foot))
        cons.extend(mc.pointConstraint(self.get_node('rt_fk_ankle_01_Ctrl', puppet), r_foot))
        cons.extend(mc.pointConstraint(pup_root, l_root))
        cons.extend(mc.pointConstraint(pup_root, r_root))
        
        mc.pointConstraint(l_root, r_root, root)

      
        with ml_utilities.IsolateViews():
            mc.bakeResults([l_root, r_root], time=(self.frame_range[0],self.frame_range[1]), sampleBy=1, preserveOutsideKeys=False, simulation=True)        

        
        mc.delete(cons)
        
        cons.extend(mc.pointConstraint(self.get_node('foot_l', self.skeleton), l_foot))
        cons.extend(mc.pointConstraint(self.get_node('foot_r', self.skeleton), r_foot))
        
        cons = mc.pointConstraint(root, pup_root)

        with ml_utilities.IsolateViews():
            mc.bakeResults([pup_root], time=(self.frame_range[0],self.frame_range[1]), sampleBy=1, preserveOutsideKeys=False, simulation=True)        

        
        mc.delete(cons)
        mc.delete(l_foot, r_foot)
        
    
    def copy_animation(self):
        
        keyed = self.mapped_controls(self.intermediatePuppet)
    
        #get a list of all nodes under the destination
        allDestNodes = self.mapped_controls(self.puppet)
    
        destNodeMap = {}
        duplicate = []
        for each in allDestNodes:
            name = each.rsplit('|')[-1].rsplit(':')[-1]
            if name in duplicate:
                continue
            if name in destNodeMap.keys():
                duplicate.append(name)
                continue
            destNodeMap[name] = each
    
        for node in keyed:
            #strip name
            nodeName = node.rsplit('|')[-1].rsplit(':')[-1]
    
            if nodeName in duplicate:
                print 'WARNING: Two or more destination nodes have the same name: '+destNS+nodeName
                continue
            if nodeName not in destNodeMap.keys():
                print 'WARNING: Cannot find destination node: '+destNS+nodeName
                continue
    
            ml_utilities.minimizeRotationCurves(node)
            mc.copyKey(node)
            mc.pasteKey(destNodeMap[nodeName], option='replaceCompletely')

    
    def cleanup(self):
        refNode = mc.referenceQuery(self.intermediatePuppet, referenceNode=True)
        refFile = mc.referenceQuery(refNode, filename=True)
        mc.file(refFile, removeReference=True)
        remove = mc.ls(CLEANUP_PREFIX+'*')
        for each in remove:
            try:
                mc.delete(each)
            except:
                pass
            
    def get_namespace(self, node):
        if not ':' in str(node):
            return ''
        return node.rsplit('|',1)[-1].rsplit(':',1)[0]
    
    def get_joint(self, control):
        joint = self.get_data(control, 'target')
        if not joint:
            return None
        target = self.skeleton_namespace+joint
        #this might not be needed if data is clean
        if not mc.nodeType(target) == 'joint':
            target = self.skeleton_namespace+joint+'1'
            
        return target
    