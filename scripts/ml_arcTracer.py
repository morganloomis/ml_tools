# -= ml_arcTracer.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 11
#   / / / / / / /  2018-05-13
#  /_/ /_/ /_/_/  _________
#               /_________/
# 
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Copyright 2018 Morgan Loomis
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_arcTracer.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_arcTracer
#     ml_arcTracer.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Create a line on screen which traces the path af an animated object. It's
# Substitute for tracing arcs on your screen by hand with a marker. It can be used
# either as an overlay on your camera view, or in world space. It's a bake
# process; like a marker it doesn't update interactively. Lines are colored to
# distinguish between multiple traces. Frames are marked along the arc as black
# dots, with keyframes colored red, and the current frame is highlighted.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, and press the buttons to choose the action.
# 
#     ____________
# - -/__ Video __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# http://www.youtube.com/watch?v=xLA1aglvPYM
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Trace Camera] : Trace an arc as an overlay over the current camera.
# [Trace World] : Trace an arc in world space.
# [Retrace Previous] : Retrace the previously traced arc.
# [Clear Arcs] : Clear all arcs.
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
__revision__ = 11
__category__ = 'animation'

shelfButton = {'annotation': 'Open a UI to trace the animation of a node across the screen.',
               'menuItem': [['Trace Camera','import ml_arcTracer;ml_arcTracer.traceCamera()'],
                            ['Trace World','import ml_arcTracer;ml_arcTracer.traceWorld()'],
                            ['Retrace', 'import ml_arcTracer;ml_arcTracer.retraceArc()'],
                            ['Clear Arcs','import ml_arcTracer;ml_arcTracer.clearArcs()']],
               'order': 2}

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya
import random, math
from functools import partial

try:
    import ml_utilities as utl
    utl.upToDateCheck(32)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/tool/ml_utilities/',absolute=True)


def ui():
    '''
    User interface for arc tracer
    '''

    globalScale = 1
    if mc.optionVar(exists='ml_arcTracer_brushGlobalScale'):
        globalScale = mc.optionVar(query='ml_arcTracer_brushGlobalScale')

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
        fsg = mc.floatSliderGrp( label='Line Width', minValue=0.1, maxValue=5, value=globalScale)
        mc.floatSliderGrp(fsg, edit=True, dragCommand=partial(setLineWidthCallback, fsg))


def mini():
    name = 'ml_arcTracer_win_mini'
    w = 100
    h = 50
    if mc.window(name, exists=True):
        mc.deleteUI(name)
    win = mc.window(name, width=w, height=h, title='arcs', iconName='arc')
    form = mc.formLayout()

    a1 = mc.button(label='camera', command=traceCamera)
    a2 = mc.button(label='world', command=traceWorld)
    b1 = mc.button(label='retrace', command=retraceArc)
    b2 = mc.button(label='clear', command=clearArcs)

    utl.formLayoutGrid(form, [[a1,a2],[b1,b2]], )

    mc.showWindow(win)
    mc.window(win, edit=True, width=w, height=h)


def setLineWidthCallback(slider, *args):
    value = mc.floatSliderGrp(slider, query=True, value=True)
    for each in mc.ls('ml_arcTracer_brush_*', type='brush'):
        mc.setAttr(each+'.globalScale', value)

    mc.optionVar(floatValue=('ml_arcTracer_brushGlobalScale', value))


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


def getWorldValueAtFrame(attr, frame):
    mSelectionList = OpenMaya.MSelectionList()
    mSelectionList.add(attr)
    plug = OpenMaya.MPlug()
    mSelectionList.getPlug(0, plug)
    context = OpenMaya.MDGContext(OpenMaya.MTime(frame))
    return plug.asDouble(context)


def traceArc(space='camera'):
    '''
    The main function for creating the arc.
    '''

    if space not in ('world','camera'):
        OpenMaya.MGlobal.displayWarning('Improper space argument.')
        return

    global ML_TRACE_ARC_PREVIOUS_SELECTION
    global ML_TRACE_ARC_PREVIOUS_SPACE

    globalScale = 1
    if mc.optionVar(exists='ml_arcTracer_brushGlobalScale'):
        globalScale = mc.optionVar(query='ml_arcTracer_brushGlobalScale')

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
    group = []

    for i,obj in enumerate(objs):
        sn = mc.ls(obj,shortNames=True)[0]
        name = sn.replace(':','_')

        groupName = 'ml_{}_arcGrp'.format(name)
        if mc.objExists(groupName):
            mc.delete(groupName)

        group.append(mc.group(empty=True, name=groupName))

        group[i] = mc.parent(group[i],parentGrp)[0]
        mc.setAttr(group[i]+'.translate', 0,0,0)
        mc.setAttr(group[i]+'.rotate', 0,0,0)

    with utl.UndoChunk():

        #determine the method to run. Test fast against accurate.
        #If fast is the same, continue with fast method.
        #Otherwise revert to accurate method.

        mc.currentTime(start)
        fastPoints = arcDataFast([objs[0]], parentGrp, start+1, start+1, space, nearClipPlane, cam)
        accuratePoints = arcDataAccurate([objs[0]], parentGrp, start+1, start+1, space, nearClipPlane, cam)

        points = None
        #if they're equivalent, continue with fast:
        if [int(x*1000000) for x in fastPoints[0][0]] == [int(x*1000000) for x in accuratePoints[0][0]]:
            points = arcDataFast([objs[0]], parentGrp, start, end, space, nearClipPlane, cam)
        else:
            points = arcDataAccurate([objs[0]], parentGrp, start, end, space, nearClipPlane, cam)

        #create the curves and do paint effects
        mc.ResetTemplateBrush()
        brush = mc.getDefaultBrush()
        mc.setAttr(brush+'.screenspaceWidth',1)
        mc.setAttr(brush+'.distanceScaling',0)
        mc.setAttr(brush+'.brushWidth',0.005)

        for i,obj in enumerate(objs):

            #setup brush for path
            globalScale
            mc.setAttr(brush+'.globalScale', globalScale)
            mc.setAttr(brush+'.screenspaceWidth',1)
            mc.setAttr(brush+'.distanceScaling',0)
            mc.setAttr(brush+'.brushWidth',0.003)

            #color
            for c in ('R','G','B'):
                color = random.uniform(0.3,0.7)
                mc.setAttr(brush+'.color1'+c,color)

            baseCurve = mc.curve(d=3,p=points[i])
            #fitBspline makes a curve that goes THROUGH the points, a more accurate path
            curve = mc.fitBspline(baseCurve, constructionHistory=False, tolerance=0.001, name='ml_arcTracer_curve_#')
            mc.delete(baseCurve)

            #paint fx
            mc.AttachBrushToCurves(curve)
            stroke = mc.ls(sl=True)[0]
            mc.rename(mc.listConnections(stroke+'.brush', destination=False)[0], 'ml_arcTracer_brush_#')

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
                    vec = utl.Vector(points[i][t][0],points[i][t][1],points[i][t][2])
                    vec*=0.98
                    frameCurve = mc.curve(d=1,p=[points[i][t],vec[:]])

                elif space=='world':
                    frameCurve = mc.circle(constructionHistory=False, radius=0.0001, sections=4)[0]
                    mc.setAttr(frameCurve+'.translate', points[i][t][0], points[i][t][1], points[i][t][2])
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
                thisBrush = mc.rename(thisBrush, 'ml_arcTracer_brush_#')

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
        try:
            mc.modelEditor(panel, edit=True, strokes=True)
        except:
            pass

    mc.select(objs,replace=True)
    mc.refresh()


def arcDataFast(objs, parentGrp, start, end, space, nearClipPlane, cam=None):

    points = []
    camSample = None
    camROO = 0
    if space=='camera':
        camSample = mc.spaceLocator()[0]
        mc.parentConstraint(cam, camSample)
        camROO = mc.getAttr(cam+'.rotateOrder')

    for i,obj in enumerate(objs):
        points.append([])
        sample = mc.spaceLocator()[0]
        mc.pointConstraint(obj, sample)

        #frame loop:
        time = list(range(int(start),int(end+1)))

        for t in time:
            objPnt = []
            for attr in ('.tx','.ty','.tz'):
                objPnt.append(getWorldValueAtFrame(sample+attr, t))

            if space=='camera':
                camPnt = []
                for attr in ('.tx','.ty','.tz'):
                    camPnt.append(getWorldValueAtFrame(camSample+attr, t))
                camRot = []
                for attr in ('.rx','.ry','.rz'):
                    camRot.append(getWorldValueAtFrame(camSample+attr, t))

                objVec = utl.Vector(objPnt[0],objPnt[1],objPnt[2])
                camVec = utl.Vector(camPnt[0],camPnt[1],camPnt[2])

                vec = objVec-camVec
                vec.normalize()
                #multiply here to offset from camera
                vec=vec*nearClipPlane*1.2

                oriLoc = mc.spaceLocator()[0]
                mc.setAttr(oriLoc+'.rotateOrder', camROO)
                mc.setAttr(oriLoc+'.rotate', *[math.degrees(x) for x in camRot])

                loc = mc.spaceLocator()[0]
                mc.setAttr(loc+'.translate', *vec[:])
                loc = mc.parent(loc, oriLoc)[0]

                trans = mc.getAttr(loc+'.translate')
                points[i].append(trans[0])

                mc.delete(oriLoc)

            elif space=='world':
                points[i].append(objPnt)

        mc.delete(sample)

    if camSample:
        mc.delete(camSample)

    return points


def arcDataAccurate(objs, parentGrp, start, end, space, nearClipPlane, cam=None):

    points = [[] for x in objs]

    with utl.IsolateViews():

        #helper locator
        loc = mc.spaceLocator()[0]
        mc.parent(loc,parentGrp)

        #frame loop:
        time = list(range(int(start),int(end+1)))
        for t in time:
            mc.currentTime(t, edit=True)

            #object loop
            for i,obj in enumerate(objs):

                objPnt = mc.xform(obj, query=True, worldSpace=True, rotatePivot=True)

                if space=='camera':
                    camPnt = mc.xform(cam, query=True, worldSpace=True, rotatePivot=True)

                    objVec = utl.Vector(objPnt[0],objPnt[1],objPnt[2])
                    camVec = utl.Vector(camPnt[0],camPnt[1],camPnt[2])

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
    return points


def retraceArc(*args):
    '''
    Reads the global variables to trace the previous selection and settings.
    '''

    try:
        sel = mc.ls(sl=True)
        mc.select(ML_TRACE_ARC_PREVIOUS_SELECTION, replace=True)
        traceArc(space=ML_TRACE_ARC_PREVIOUS_SPACE)
        mc.select(sel,replace=True)
    except Exception:
        pass


def clearArcs(*args):
    '''
    Simply deletes the arc group by name.
    '''

    try:
        mc.delete('ml_arcGroup')
    except Exception:
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


def markingMenu():
    '''
    Example of how a marking menu could be set up.
    '''

    menuKwargs = {'enable':True,
                  'subMenu':False,
                  'enableCommandRepeat':True,
                  'optionBox':False,
                  'boldFont':True}

    mc.menuItem(radialPosition='N', label='Trace Camera', command=traceCamera, **menuKwargs)
    mc.menuItem(radialPosition='E', label='Trace World', command=traceWorld, **menuKwargs)
    mc.menuItem(radialPosition='W', label='Re-Trace', command=retraceArc, **menuKwargs)
    mc.menuItem(radialPosition='S', label='Clear', command=clearArcs, **menuKwargs)

    mc.menuItem(label='Arc Tracer UI', command=ui, **menuKwargs)


if __name__ == '__main__':ui()

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
#
# Revision 5: 2016-12-10 : removing euclid dependency
#
# Revision 6: 2017-06-30 : Fixing bug with moving cameras, adding line width
#
# Revision 7: 2018-02-17 : Updating license to MIT.
#
# Revision 8: 2018-04-09 : Test for accuracy to determine whether the fast solution is accurate.
#
# Revision 9: 2018-05-05 : Adding shelf support.
#
# Revision 10: 2018-05-06 : Added marking menu.
#
# Revision 11: 2018-05-13 : shelf support