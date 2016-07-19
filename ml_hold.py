# 
#   -= ml_hold.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 6, 2015-01-10
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_hold.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_hold
#     ml_hold.ui()
# From MEL, this looks like:
#     python("import ml_hold;ml_hold.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This is a tool for creating animation holds, either for individual
# poses or over a range of keys. Select a range of keys in the graph editor
# or the time slider, or match your current pose to the next or previous one.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI. 
# Press Next and Previous to match keys to the value of next or previous keyframes.
# Press Current or Average to turn a frame range into a hold. Current sets the 
# hold to be the current value, and average sets the value to the average of 
# all keys across the range. The range is determined by one of 3 things, 
# in the following order: 1. Selected range in the time slider. 2. The highest
# and lowest selected keys in the graph editor. 3. If nothing is selected,
# the previous and next keys from the current time determine the range.
# If you have no keys selectd, all commands will operate only on curves
# that are visibile in the graph editor.
#      ____________________
# - -/__ Video Tutorial __/- - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# http://www.youtube.com/watch?v=fOeDwGbuHFE
#      ________________
# - -/__ UI Options __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [Hold Current] : Creates a hold for the selected range, or the surrounding keys, based on current frame.
# [Hold Average] : Creates a hold for the selected range, or the surrounding keys, based on average of keys.
# [<< Previous] : Matches selected key or current frame to the previous keyframe value.
# [Next >>] : Matches selected key or current frame to the next keyframe value.
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'animationScripts'
__revision__ = 6

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya

try:
    import ml_utilities as utl
    utl.upToDateCheck(11)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    

def ui():
    '''
    user interface for ml_hold
    '''

    with utl.MlUi('ml_hold', 'Hold Keys', width=400, height=150, info='''Press Next and Previous to match keys to the next or previous keyframes.
Press Current or Average to turn a frame range into a hold.''') as win:

        win.buttonWithPopup(label='Hold Current', command=current, annotation='Creates a hold for the selected range, or the surrounding keys, based on current frame.', shelfLabel='cur', shelfIcon='defaultTwoStackedLayout')
        win.buttonWithPopup(label='Hold Average', command=average, annotation='Creates a hold for the selected range, or the surrounding keys, based on average of keys.', shelfLabel='avg', shelfIcon='defaultTwoStackedLayout')
        
        mc.paneLayout(configuration='vertical2',separatorThickness=1)
        win.buttonWithPopup(label='<< Previous', command=previous, annotation='Matches selected key or current frame to the previous keyframe value.', shelfLabel='<_', shelfIcon='defaultTwoStackedLayout')
        win.buttonWithPopup(label='Next >>', command=next, annotation='Matches selected key or current frame to the next keyframe value.', shelfLabel='_>', shelfIcon='defaultTwoStackedLayout')
        

def next(*args):
    '''Matches selected key or current frame to the next keyframe value.'''
    holdFrame(next=True)
    
def previous(*args):
    '''Matches selected key or current frame to the previous keyframe value.'''
    holdFrame(previous=True)
    
def current(*args):
    '''Creates a hold for the selected range, or the surrounding keys, based on current frame.'''
    holdRange(current=True)

def average(*args):
    '''Creates a hold for the selected range, or the surrounding keys, based on average of keys.'''
    holdRange(average=True)

def holdFrame(next=False, previous=False):
    '''
    Creates a hold between the specified key or frame and the next or previous key
    Arguments:
        next: Match the value of the specified frame to the next key in time.
        previous: Match the value of the specified frame to the previous key in time.
    '''

    if (next and previous) or (not next and not previous):
        OpenMaya.MGlobal.displayWarning('This function requires exactly one argument to be true.')
        return

    sel = mc.ls(sl=True)

    if not sel:
        OpenMaya.MGlobal.displayWarning('Nothing selected.')
        return
    
    curves = None
    start = None
    end = None
    value = None
    currentTime = mc.currentTime(query=True)

    keySel = utl.KeySelection()
    if keySel.selectedKeys():
        pass
    elif keySel.visibleInGraphEditor():
        pass
    elif keySel.keyedChannels():
        pass
    
    if keySel.selectedFrameRange():
        pass
    elif keySel.keyRange():
        pass
    else:
        keySel.setKeyframe()

    start = None
    end = None

    #if you're using maya before 2011, python doesn't undo properly
    with utl.UndoChunk():
        itt,ott = utl.getHoldTangentType()
        selected = mc.keyframe(query=True, name=True, selected=True)
            
        for curve in keySel.curves:
            value = None
            start = currentTime
            end = currentTime
            findFrom = currentTime
            if selected:
                keyTimes = mc.keyframe(curve, query=True, timeChange=True, selected=True)
                if next:
                    start = keyTimes[0]
                    findFrom = keyTimes[-1]
                elif previous:
                    end = keyTimes[-1]
                    findFrom = keyTimes[0]
            if next:
                end = mc.findKeyframe(curve, time=(findFrom,), which='next')
                value = mc.keyframe(curve, time=(end,), query=True, valueChange=True)[0]
            elif previous:
                start = mc.findKeyframe(curve, time=(findFrom,), which='previous')
                value = mc.keyframe(curve, time=(start,), query=True, valueChange=True)[0]
            
            #TODO: delete redundant keys
            
            if (end-start) > 1:
                mc.cutKey(curve, time=(start+0.1, end-0.1))
            
            mc.keyframe(curve, time=(start,end), edit=True, valueChange=value)
            
            #set tangents
            mc.keyTangent(curve, time=(start,end), itt=itt, ott=ott)
        

def holdRange(current=False, average=False):
    '''
    Create a hold over a range of frames. 
    Arguments:
        current: hold value comes from current frame
        average: hold value comes from the average of all keys over the range.
    '''


    if (current and average) or (not current and not average):
        OpenMaya.MGlobal.displayWarning('This function requires exactly one argument to be true.')
        return

    sel = mc.ls(sl=True)
    
    if not sel:
        OpenMaya.MGlobal.displayWarning('Nothing selected.')
        return
        
    curves = None
    start = None
    end = None
    value = None
    
    currentTime = mc.currentTime(query=True)
    graphVis = mc.selectionConnection('graphEditor1FromOutliner', query=True, obj=True)

    # first check if a range is selected
    gPlayBackSlider = mm.eval('$temp=$gPlayBackSlider')
    if mc.timeControl(gPlayBackSlider, query=True, rangeVisible=True):
        pbRange = mc.timeControl(gPlayBackSlider, query=True, rangeArray=True)
        start = float(pbRange[0])
        end = float(pbRange[1])-1

        #visible in graph editor
        if graphVis:
            curves = mc.keyframe(graphVis, query=True, name=True)
        else:
            curves = mc.keyframe(sel, query=True, name=True)
    else:
        #selected key range
        curves = mc.keyframe(query=True, name=True, selected=True)
        if curves:
            keyTimes = mc.keyframe(query=True, timeChange=True, selected=True)
            keyTimes.sort()
            if keyTimes[0] == keyTimes[-1]:
                return
            
            start = keyTimes[0]
            end = keyTimes[-1]
            
        else:
            if graphVis:
                curves = mc.keyframe(graphVis, query=True, name=True)
            else:
                curves = mc.keyframe(sel, query=True, name=True)
                
            start = mc.findKeyframe(curves, time=(currentTime,), which='previous')
            end = mc.findKeyframe(curves, time=(currentTime,), which='next')
            
    #set start and end frames
    mc.setKeyframe(curves, time=(start,end))

    #if you're using maya before 2011, python doesn't undo properly
    with utl.UndoChunk():
        for curve in curves:
            if average:
                v = mc.keyframe(curve, time=(start,end), query=True, valueChange=True)
                value = sum(v)/len(v)
            elif current:
                if 'animCurveT' in mc.nodeType(curve):
                    plug = mc.listConnections('.'.join((curve,'output')), source=False, plugs=True)[0]
                    value = mc.getAttr(plug)
                
            mc.keyframe(curve, time=(start,end), edit=True, valueChange=value)
            
        #delete inbetweens
        if (end-start) > 1:
            mc.cutKey(curves, time=(start+0.1, end-0.1))
        itt,ott = utl.getHoldTangentType()
        mc.keyTangent(curves, time=(start,end), itt=itt, ott=ott)

if __name__ == '__main__':
    ui()

#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - - 
#
# Revision 1: : First publish
#
# Revision 4: 2011-05-01 : Updated to use ml_utilities
#
# Revision 5: 2014-03-01 : adding category
#
# Revision 6: 2015-01-10 : Fixed bug relating to KeySelection
