
import pymel.core as pm
import maya.cmds as mc
import ml_utilities as utl
import sys, inspect
import importlib

def main():
    Ui()

class Ui():
    
    def __init__(self, prefix=None):
        
        with utl.MlUi('cleanSceneWindow', 'Clean Scene', width=200, height=400, 
                      info='''Clean Scene. 
.''', 
                      menu=False) as win:
            
            self.window = win
    
            thisModule = sys.modules[__name__]
            allFunctions = inspect.getmembers(thisModule, inspect.isfunction)
            
            self.checkBoxes = list()
            
            self.functions = list()

            for pair in allFunctions:
                name = pair[0]
                func = pair[1]
                
                #isChecked = int(preset == 'all' or (bool(functions) and name in functions))
                isChecked = bool(prefix) and name.startswith(prefix)
                
                #skip these:
                if name in ['ui', 'selectFileNodesWithBadPaths', 'main']:
                    continue
                
                self.checkBoxes.append(mc.checkBox(label=name, value=isChecked))
                self.functions.append(func)
                    
            mc.button(label='Clean Scene', command=self.readUI)
        
        
    def readUI(self, *args):
        
        for cb, func in zip(self.checkBoxes, self.functions):
            if pm.checkBox(cb, query=True, value=True):
                func()

class Cleaner(object):
    
    def __init__(self):
        self.collect()
        
    def collect(self):
        pass
    
    def clean(self):
        raise NotImplementedError()
        

#delete stuff
def deleteOrphanedAnimationCurves():
    curves = mc.ls(type='animCurve')
    deleteCurves = []
    for curve in curves:
        if not mc.listConnections(curve, source=False, destination=True):
            deleteCurves.append(curve)
    mc.delete(deleteCurves)


def deleteGarbage():
    
    #delete rubbish groups
    rubbishes = pm.ls('rubbish')
    rubbishes.extend(pm.ls('garbage'))
    if rubbishes:
        pm.delete(rubbishes)


def deleteLayers():
    #delete layers
    layers = pm.ls(type='displayLayer')
    for layer in layers:
        if layer.name() == 'defaultLayer':
            continue
        pm.delete(layer)


def deleteSets():
    pass
    #delete selection sets?


def deleteUnusedShaders():
    #delete unconnected shaders
    #for now it's just lamberts, make more general eventually
    #this is mostly to get rid of lowres geo shaders
    shaders = pm.ls(type='lambert')
    if shaders:
        for shad in shaders:
            if shad.hasAttr('joint'):
                pm.delete(shad)
    try:
        pm.mel.MLdeleteUnused()
    except:pass    


def deleteIntermediateGeo():
    
    for each in pm.ls(type='mesh'):
        if each.intermediateObject.get():
            print('Deleting intermediate geo:',each.nodeName())
            pm.delete()


def modelFreezeTransforms():
    models = pm.ls(type='mesh')
    if models:
        for model in models:
            parent = model.getParent()
            pm.makeIdentity(parent, apply=True)


def modelPivotsToOrigin():
    models = pm.ls(type='mesh')
    if models:
        for model in models:
            parent = model.getParent()
            pm.xform(parent, zeroTransformPivots=True)            
            
            
def modelUnlockNormals():
    pass


def flattenReferences():
    
    referenceNodes = mc.ls(type='reference')
    ns = list()
    for each in referenceNodes:
        if each == 'sharedReferenceNode':
            continue
        #if there's no file associated, delete it
        try:
            refFile = mc.referenceQuery(each, filename=True)
        except Exception:
            mc.lockNode(each, lock=False)
            mc.delete(each)
            continue
        
        #import the reference
        mc.file(refFile, importReference=True)
    
    #get rid of namespaces
    for ns in mc.namespaceInfo(listOnlyNamespaces=True):
        if ns != 'UI' and ns != 'shared':
            mc.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)


def selectFileNodesWithBadPaths():
    
    #copy texture files
    fileNodes = pm.ls(type='file')
    
    if not fileNodes:
        return
    
    badFileNodes = list()
    for f in fileNodes:
        filePath = f.fileTextureName.get()
        if not os.path.exists(filePath):
            print('Texture File Not Found:',filePath)
            badFileNodes.append(f)
        else:
            print(filePath)
    if badFileNodes:
        pm.select(badFileNodes)


def removeUnusedInfluences():
    
    skinClusters = pm.ls(type='skinCluster')
    print('MAKE IT WORK!')
    

def renameDuplicateNames():
    import pymel.core as pm
    dups = [x for x in mc.ls(dagObjects=True) if '|' in x]
    dups = [pm.PyNode(x) for x in dups]

    for dup in dups:
        oldName = dup.nodeName()
        if len(mc.ls(oldName)) < 2:
            #one has already been renamed
            continue

        name = oldName.strip('0123456789')
        name+='#'
        newName = pm.rename(dup, name)


def deleteUnusedNodes():
    
    def _allNodes():
        allNodes = []
        nodeTypes = ['decomposeMatrix',
                     'composeMatrix',
                     'multMatrix',
                     'network',
                     'holdMatrix',
                     'blendMatrix',
                     'multiplyDivide',
                     'addDoubleLinear',
                     'multDoubleLinear',
                     'plusMinusAverage',
                     'pointMatrixMult',
                     'expression',
                     'animBlendNodeAdditiveRotation',
                     'blendColors',
                     'condition',
                     'distanceBetween',
                     'pointOnCurveInfo',
                     'pointOnSurfaceInfo',
                     'remapValue',
                     'reverse',
                     'inverseMatrix'
                     ]   
        for each in nodeTypes:
            allNodes.extend(mc.ls(type=each))
        return allNodes
    
    allNodes = _allNodes()
    if not allNodes:
        return
    
    firstCount = len(allNodes)
    count = len(allNodes)
    while True:
        for node in allNodes:
            if not mc.objExists(node):
                continue
            connections = mc.listConnections(node, source=False, destination=True)
            try:
                connections.remove('defaultRenderUtilityList1')
            except: pass
            if not connections:
                mc.delete(node)
        
        allNodes = _allNodes()
        if len(allNodes) == count:
            break
        count = len(allNodes)
        
    print(firstCount - count)
    

if __name__ == '__main__':
    import ml_cleanScene
    importlib.reload(ml_cleanScene)
    ml_cleanScene.Ui()