# 
#   -= ml_arcTracer.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 4, 2014-03-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_arcTracer.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_arcTracer
#     ml_arcTracer.ui()
# From MEL, this looks like:
#     python("import ml_arcTracer;ml_arcTracer.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This tool is a substitute for tracing arcs on your screen by hand with a marker.
# It creates a thick line to represent the path of an object, either as an overlay on your camera view,
# or in world space. It's a bake process; like a marker it doesn't update interactively.
# Lines are colored randomly, to distinguish between multiple traces.
# Frames are marked along the arc as black dots, with keyframes colored red, and
# the current frame is highlighted.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, and press the buttons to choose the action.
#      ____________________
# - -/__ Video Tutorial __/- - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# http://www.youtube.com/watch?v=xLA1aglvPYM
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Trace Camera] : Trace an arc as an overlay over the current camera.
# [Trace World] : Trace an arc in world space.
# [Retrace Previous] : Retrace the previously traced arc.
# [Clear Arcs] : Clear all arcs.
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the euclid module, which can be downloaded here:
# 	http://partiallydisassembled.net/euclid.html
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'animationScripts'
__revision__ = 4
import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya
import random

try:
    import euclid
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the euclid module, which can be downloaded for free from the internet. Once downloaded you will need to restart Maya.', 
                button=['Go To Website','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result != 'Cancel':
        mc.showHelp('http://partiallydisassembled.net/euclid.html',absolute=True)

try:
    import ml_utilities as utl
    utl.upToDateCheck(9)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    

def ui():
    '''
    User interface for world bake
    '''

    with utl.MlUi('ml_arcTracer', 'Arc Tracer', width=400, height=180, info='''Select objects to trace.
Choose camera space or worldspace arc.
Press clear to delete the arcs, or retrace to redo the last arc.''') as win:

        win.buttonWithPopup(label='Trace Camera', command=traceCamera, annotation='Trace an arc as an overlay over the current camera.', 
                            shelfLabel='cam', shelfIcon='flowPathObj')#motionTrail
        win.buttonWithPopup(label='Trace World', command=traceWorld, annotation='Trace an arc in world space.', 
                            shelfLabel='world', shelfIcon='flowPathObj')
        win.buttonWithPopup(label='Retrace Previous', command=retraceArc, annotation='Retrace the previously traced arc.', 
                            shelfLabel='retrace', shelfIcon='flowPathObj')
        win.buttonWithPopup(label='Clear Arcs', command=clearArcs, annotation='Clear all arcs.', 
                            shelfLabel='clear', shelfIcon='flowPathObj')


def traceCamera(*args):
    '''
    Wrapper for tracing in camera space
    '''
    traceArc(space='camera')


def traceWorld(*args):
    '''
    Wrapper for tracing in world space
    '''
    traceArc(space='world')


def traceArc(space='camera'):
    '''
    The main function for creating the arc.
    '''
    
    if space != 'world' and space != 'camera':
        OpenMaya.MGlobal.displayWarning('Improper space argument.')
        return
    
    global ML_TRACE_ARC_PREVIOUS_SELECTION
    global ML_TRACE_ARC_PREVIOUS_SPACE
    
    #save for reset:
    origTime = mc.currentTime(query=True)
    
    #frame range
    frameRange = utl.frameRange()
    start = frameRange[0]
    end = frameRange[1]
    
    #get neccesary nodes
    objs = mc.ls(sl=True, type='transform')
    if not objs:
        OpenMaya.MGlobal.displayWarning('Select objects to trace')
        return
    
    ML_TRACE_ARC_PREVIOUS_SELECTION = objs
    ML_TRACE_ARC_PREVIOUS_SPACE = space
    
    cam = None
    nearClipPlane = None
    shortCam = ''
    if space=='camera':
        cam = utl.getCurrentCamera()
    
        #the arc will be placed just past the clip plane distance, but no closer than 1 unit.
        nearClipPlane = max(mc.getAttr(cam+'.nearClipPlane'),1)
        
        shortCam = mc.ls(cam, shortNames=True)[0]
    
    topGroup = 'ml_arcGroup'
    worldGrp = 'ml_arcWorldGrp'
    localGrp = 'ml_localGrp_'+shortCam
    
    #create nodes
    if not mc.objExists(topGroup):
        topGroup = mc.group(empty=True, name=topGroup)
    
    parentGrp = topGroup
    if space=='world' and not mc.objExists(worldGrp):
        worldGrp = mc.group(empty=True, name=worldGrp)
        mc.setAttr(worldGrp+'.overrideEnabled',1)
        mc.setAttr(worldGrp+'.overrideDisplayType',2)
        mc.parent(worldGrp, topGroup)
        parentGrp = mc.ls(worldGrp)[0]
    
    if space == 'camera':
        camConnections = mc.listConnections(cam+'.message', plugs=True, source=False, destination=True)
        if camConnections:
            for cc in camConnections:
                if '.ml_parentCam' in cc:
                    localGrp = mc.ls(cc, o=True)[0]
        
        if not mc.objExists(localGrp):
            localGrp = mc.group(empty=True, name=localGrp)
            mc.parentConstraint(cam, localGrp)
            mc.setAttr(localGrp+'.overrideEnabled',1)
            mc.setAttr(localGrp+'.overrideDisplayType',2)
            mc.parent(localGrp, topGroup)
            
            mc.addAttr(localGrp, at='message', longName='ml_parentCam')
            mc.connectAttr(cam+'.message', localGrp+'.ml_parentCam')
            
        parentGrp = mc.ls(localGrp)[0]
    
    #group per object:
    group = list()
    points = list()
    
    for i,obj in enumerate(objs):
        sn = mc.ls(obj,shortNames=True)[0]
        name = sn.replace(':','_')
    
        points.append(list())
        groupName = 'ml_%s_arcGrp' % name
        if mc.objExists(groupName):
            mc.delete(groupName)
        
        group.append(mc.group(empty=True, name=groupName))
        
        group[i] = mc.parent(group[i],parentGrp)[0]
        mc.setAttr(group[i]+'.translate', 0,0,0)
        mc.setAttr(group[i]+'.rotate', 0,0,0)
    
    with utl.UndoChunk():
        with utl.IsolateViews():

            #helper locator
            loc = mc.spaceLocator()[0]
            mc.parent(loc,parentGrp)

            #frame loop:
            time = range(int(start),int(end+1))
            for t in time:
                mc.currentTime(t, edit=True)

                #object loop
                for i,obj in enumerate(objs):

                    objPnt = mc.xform(obj, query=True, worldSpace=True, rotatePivot=True)

                    if space=='camera':
                        camPnt = mc.xform(cam, query=True, worldSpace=True, rotatePivot=True)

                        objVec = euclid.Vector3(objPnt[0],objPnt[1],objPnt[2])
                        camVec = euclid.Vector3(camPnt[0],camPnt[1],camPnt[2])

                        vec = objVec-camVec
                        vec.normalize()
                        #multiply here to offset from camera
                        vec=vec*nearClipPlane*1.2
                        vec+=camVec

                        mc.xform(loc, worldSpace=True, translation=vec[:])

                        trans = mc.getAttr(loc+'.translate')
                        points[i].append(trans[0]) 

                    elif space=='world':
                        points[i].append(objPnt)

            mc.delete(loc)

            #create the curves and do paint effects
            mc.ResetTemplateBrush()
            brush = mc.getDefaultBrush()
            mc.setAttr(brush+'.screenspaceWidth',1)
            mc.setAttr(brush+'.distanceScaling',0)
            mc.setAttr(brush+'.brushWidth',0.005)

            for i,obj in enumerate(objs):

                #setup brush for path
                mc.setAttr(brush+'.screenspaceWidth',1)
                mc.setAttr(brush+'.distanceScaling',0)
                mc.setAttr(brush+'.brushWidth',0.003)

                #color
                for c in ('R','G','B'):
                    color = random.uniform(0.3,0.7)
                    mc.setAttr(brush+'.color1'+c,color)
                
                baseCurve = mc.curve(d=3,p=points[i])
                #fitBspline makes a curve that goes THROUGH the points, a more accurate path
                curve = mc.fitBspline(baseCurve, constructionHistory=False, tolerance=0.001)
                mc.delete(baseCurve)

                #paint fx
                mc.AttachBrushToCurves(curve)
                stroke = mc.ls(sl=True)[0]
                stroke = mc.parent(stroke,group[i])[0]

                mc.setAttr(stroke+'.overrideEnabled',1)
                mc.setAttr(stroke+'.overrideDisplayType',2)

                mc.setAttr(stroke+'.displayPercent',92)
                mc.setAttr(stroke+'.sampleDensity',0.5)
                mc.setAttr(stroke+'.inheritsTransform',0)
                mc.setAttr(stroke+'.translate',0,0,0)
                mc.setAttr(stroke+'.rotate',0,0,0)

                curve = mc.parent(curve,group[i])[0]
                mc.setAttr(curve+'.translate',0,0,0)
                mc.setAttr(curve+'.rotate',0,0,0)

                mc.hide(curve)

                #setup brush for tics
                if space=='camera':
                    mc.setAttr(brush+'.brushWidth',0.008)
                if space=='world':
                    mc.setAttr(brush+'.brushWidth',0.005)
                mc.setAttr(brush+'.color1G',0)
                mc.setAttr(brush+'.color1B',0)

                for t in range(len(points[i])):
                    frameCurve = None
                    if space=='camera':
                        vec = euclid.Vector3(points[i][t][0],points[i][t][1],points[i][t][2])
                        vec*=0.98
                        frameCurve = mc.curve(d=1,p=[points[i][t],vec[:]])

                    elif space=='world':
                        frameCurve = mc.circle(constructionHistory=False, radius=0.0001, sections=4)[0]
                        mc.setAttr(frameCurve+'.translate', points[i][t][0], points[i][t][1] ,points[i][t][2])
                        constraint = mc.tangentConstraint(curve, frameCurve, aimVector=(0,0,1), worldUpType='scene')
                        #mc.delete(constraint)

                    #check for keyframe
                    colorAttribute='color1G'
                    if mc.keyframe(obj, time=((t+start-0.5),(t+start+0.5)), query=True):
                        mc.setAttr(brush+'.color1R',1)
                    else:
                        mc.setAttr(brush+'.color1R',0)

                    mc.AttachBrushToCurves(curve)

                    stroke = mc.ls(sl=True)[0]
                    thisBrush = mc.listConnections(stroke+'.brush', destination=False)[0]

                    #setup keyframes for frame highlighting
                    mc.setKeyframe(thisBrush, attribute='color1G', value=0, time=(start+t-1, start+t+1))
                    mc.setKeyframe(thisBrush, attribute='color1G', value=1, time=(start+t,))

                    stroke = mc.parent(stroke,group[i])[0]

                    mc.hide(frameCurve)

                    mc.setAttr(stroke+'.displayPercent',92)
                    mc.setAttr(stroke+'.sampleDensity',0.5)

                    frameCurve = mc.parent(frameCurve,group[i])[0]

                    if space=='camera':
                        mc.setAttr(stroke+'.inheritsTransform',0)
                        mc.setAttr(stroke+'.pressureScale[1].pressureScale_Position', 1)
                        mc.setAttr(stroke+'.pressureScale[1].pressureScale_FloatValue', 0)
                        mc.setAttr(stroke+'.translate',0,0,0)
                        mc.setAttr(stroke+'.rotate',0,0,0)
                        mc.setAttr(frameCurve+'.translate',0,0,0)
                        mc.setAttr(frameCurve+'.rotate',0,0,0)

            mc.currentTime(origTime, edit=True)
            panel = mc.getPanel(withFocus=True)
            mc.modelEditor(panel, edit=True, strokes=True)
    
    mc.select(objs,replace=True)


def retraceArc(*args):
    '''
    Reads the global variables to trace the previous selection and settings.
    '''

    try:
        sel = mc.ls(sl=True)
        mc.select(ML_TRACE_ARC_PREVIOUS_SELECTION, replace=True)
        traceArc(space=ML_TRACE_ARC_PREVIOUS_SPACE)
        mc.select(sel,replace=True)
    except StandardError:
        pass


def clearArcs(*args):
    '''
    Simply deletes the arc group by name.
    '''

    try:
        mc.delete('ml_arcGroup')
    except StandardError:
        pass


def applyBrush(curve, parent):
    '''
    Simply applies the paint effects brush to the curve with the settings we want.
    '''
    
    mc.AttachBrushToCurves(curve)
    stroke = mc.ls(sl=True)[0]
    stroke = mc.parent(stroke,parent)[0]
    
    mc.setAttr(stroke+'.displayPercent',92)
    mc.setAttr(stroke+'.sampleDensity',0.5)
    mc.setAttr(stroke+'.inheritsTransform',0)
    mc.setAttr(stroke+'.translate',0,0,0)
    mc.setAttr(stroke+'.rotate',0,0,0)
    
    return stroke


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - - 
#
# Revision 1: 2011-05-01 : First publish
#
# Revision 2: 2011-05-14 : minor bug fix involving error with duplicate names
#
# Revision 3: 2011-05-14 : Revision notes update.
#
# Revision 4: 2014-03-01 : adding category
