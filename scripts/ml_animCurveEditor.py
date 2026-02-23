# -= ml_animCurveEditor.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 6
#   / / / / / / /  2018-05-14
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_animCurveEditor.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_animCurveEditor
#     ml_animCurveEditor.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Various tools for editing animation curves, similar to video clip non-linear
# editing tools. Maya's tools for editing lots of keys can be slow or cumbersome,
# this is meant to be an alternative interface for editing lots of keyframes.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# The "Act on Anim Curves In:" drop-down controls which animCurves are affected
# in the scene. The tabs organize the different types of tools:  Offset: Slip
# curves in time.  Cut: Cut sections of curves.  Scale Time: Globally retime a
# curve  Scale Value: Globally adjust the value of a curve.  Clamp: Clamp keyframe
# values to a high or low value, for example to prevent a channel going below
# zero.  Clean-Up: Tools for getting rid of keyframes that you may not want or
# need.
# 
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
__revision__ = 6
__category__ = 'animation'

shelfButton = {'annotation': 'Open an UI to edit animation curves in bulk.',
               'imageOverlayLabel': 'edit',
               'order': 3}

import maya.cmds as mc
from maya import OpenMaya

import bisect
import itertools

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
    '''

    with utl.MlUi('ml_animCurveEditor', 'Animation Curve Editing', width=400, height=300, info='''Non-Linear Editing workflows for animation curves.
Choose which animCurves to affect from the drop-down menu, then
change tabs to choose options related to that function.''') as win:

        mc.separator(height=8, style='none')

        mc.optionMenuGrp('ml_animCurveEditor_selection_menu',label='Act On AnimCurves In:')

        mc.menuItem(label='Selected Nodes')
        mc.menuItem(label='Selected Channels')
        mc.menuItem(label='Hierarchy')
        mc.menuItem(label='Graph Editor')
        mc.menuItem(label='Entire Scene')
        #mc.menuItem(label='AnimLayer')

        mc.separator(height=8, style='none')

        tabs = mc.tabLayout()

        # ________
        #/ Offset \_________________________________
        tab1 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Offset animCurves by the number of frames specified.')
        mc.text('Use negative values to offset backward in time.')
        mc.separator(height=16, style='in')

        mc.floatFieldGrp('ml_animCurveEditor_frames_floatField', label='Frames')

        mc.paneLayout(configuration='vertical2', separatorThickness=1)

        win.ButtonWithPopup(label='Offset', command=offset, name='ml_animCurveEditor',
                            readUI_toArgs={'frames':'ml_animCurveEditor_frames_floatField',
                                           'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation='Offset curves in time by the number of frames specified. use negative numbers to offset backwards.'
                            )

        win.ButtonWithPopup(label='Offset Current Frame To', command=offsetCurrentTimeTo, name='ml_animCurveEditor',
                            readUI_toArgs={'frame':'ml_animCurveEditor_frames_floatField',
                                           'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation='Offset curves so that the current time is moved to the specified frame.')
        mc.setParent('..')
        mc.paneLayout(configuration='vertical2', separatorThickness=1)

        win.ButtonWithPopup(label='Cut Frame', command=cutFrame,  name='ml_animCurveEditor',
                            readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation='Cut the current frame and shift animation back.'
                            )
        win.ButtonWithPopup(label='Insert Frame', command=insertFrame,  name='ml_animCurveEditor',
                            readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation='Insert frame at the current frame by shifting animation forward.'
                            )
        mc.setParent('..')
        mc.setParent('..')


        #             _____
        #____________/ Cut \_______________________
        tab2 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Cut sections of animation, based on the current frame or timeline selection.')
        mc.text('If Set Key At Cut is checked, a key will be set so that the integrity of the curves are mainained.')
        mc.separator(height=16, style='in')

        mc.checkBoxGrp('ml_animCurveEditor_setKeyAtCut_checkBox',
                       label='Set Key At Cut', value1=True,
                       annotation='Set a key at the cut point to preserve curves.')


        mc.paneLayout(configuration='vertical2', separatorThickness=1)

        b11 = win.ButtonWithPopup(label='Cut Before Current Frame', command=cutEarlier, name='ml_animCurveEditor',
                                  readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu',
                                                 'setKey':'ml_animCurveEditor_setKeyAtCut_checkBox'},
                                  annotation='Cut all keys before the current frame'
                                  )
        b21 = win.ButtonWithPopup(label='Cut After Current Frame', command=cutLater, name='ml_animCurveEditor',
                                  readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu',
                                                 'setKey':'ml_animCurveEditor_setKeyAtCut_checkBox'},
                                  annotation='Cut all keys after the current frame'
                                  )
        mc.setParent('..')
        mc.paneLayout(configuration='vertical2', separatorThickness=1)

        b12 = win.ButtonWithPopup(label='Cut Selected Range', command=cutSelected, name='ml_animCurveEditor',
                                  readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu',
                                                 'setKey':'ml_animCurveEditor_setKeyAtCut_checkBox'},
                                  annotation='Cut all keys within the range selected in the timeline'
                                  )
        b22 = win.ButtonWithPopup(label='Cut Unselected Range (Keep Only Selection)', command=cutUnselected, name='ml_animCurveEditor',
                                  readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu',
                                                 'setKey':'ml_animCurveEditor_setKeyAtCut_checkBox'},
                                  annotation='Cut all keys outside of the selected range'
                                  )
        mc.setParent('..')
        b22 = win.ButtonWithPopup(label='Ripple Cut Selection', command=rippleCut,  name='ml_animCurveEditor',
                                  readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu',
                                                 'setKey':'ml_animCurveEditor_setKeyAtCut_checkBox'},
                                  annotation='Cut keys within the selection, and move the later keys to close the gap'
                                  )
        mc.setParent('..')


        #     ____________
        #____/ Scale Time \_______________________
        tab3 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Scale animation in time to speed it up or slow it down.')
        mc.text('Time Pivot is where the animation scales from, values at this position wont change.')
        mc.separator(height=16, style='in')

        mc.radioButtonGrp('ml_animCurveEditor_scaleTimePivot_radioButton', label='Time Pivot', numberOfRadioButtons=4,
                          labelArray4=('Current Frame','Start','End','Middle'), select=1,
                          annotation='Where in time to scale from. start, end and middle refer to the range of the animation curves, not the timeline.'
                          )
        mc.floatSliderGrp('ml_animCurveEditor_scaleTimePercent_floatField', label='Percent', field=True, value=100,
                          precision=0, step=1, sliderStep=10,
                          minValue=0, maxValue=200, fieldMinValue=-10000, fieldMaxValue=10000,
                          annotation='Percentage to scale time by. 50% will make motion go twice as fast, etc.'
                          )

        win.ButtonWithPopup(label='Scale Key Time', command=scaleTime,  name='ml_animCurveEditor',
                            readUI_toArgs={'percent':'ml_animCurveEditor_scaleTimePercent_floatField',
                                           'pivotOption':'ml_animCurveEditor_scaleTimePivot_radioButton',
                                           'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation='Scale curves in time.'
                            )

        mc.setParent('..')

        #         _____________
        #________/ Scale Value \____________________
        tab4 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Scale animCurve values to change how much they affect the animation.')
        mc.text('Value Pivot is where the animation scales from, values at this position wont change.')
        mc.separator(height=16, style='in')

        mc.radioButtonGrp('ml_animCurveEditor_scaleValuePivot_radioButton', label='Value Pivot', numberOfRadioButtons=4,
                          labelArray4=('Zero','Top','Bottom','Middle'), select=1,
                          annotation='Where to scale the curves from. top, bottom and middle refer to the highest and lowest keys on the curve.'
                          )
        mc.floatSliderGrp('ml_animCurveEditor_scaleValuePercent_floatField', label='Percent', field=True, value=100,
                          precision=0, step=1, sliderStep=10,
                          minValue=0, maxValue=200, fieldMinValue=-10000, fieldMaxValue=10000,
                          annotation='Percentage to scale keyframe values by'
                          )
        win.ButtonWithPopup(label='Scale Keys', command=scaleValue, name='ml_animCurveEditor',
                            readUI_toArgs={'percent':'ml_animCurveEditor_scaleValuePercent_floatField',
                                           'pivotOption':'ml_animCurveEditor_scaleValuePivot_radioButton',
                                           'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation='Scale keyframe values'
                            )

        mc.setParent('..')


        #                 _____________
        #________________/ Value Clamp \______________
        tab5 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Clamp animation curve values at an upper or lower bound.')
        mc.text('For example to keep keys from passing below a zero-level ground plane.')
        mc.separator(height=16, style='in')

        mc.radioButtonGrp('ml_animCurveEditor_clamp_radioButton', label='Clamp:', numberOfRadioButtons=2,
                          labelArray2=('Clamp Upper','Clamp Lower'), select=1,
                          annotation='Either clamp everything above the specified value, or below'
                          )
        mc.floatFieldGrp('ml_animCurveEditor_clampValue_floatField', label='Value:',
                         annotation='Clamp keyframes above or below this value to this value'
                         )

        win.ButtonWithPopup(label='Clamp', command=clampValues,  name='ml_animCurveEditor',
                           readUI_toArgs={'value':'ml_animCurveEditor_clampValue_floatField',
                                          'clampOption':'ml_animCurveEditor_clamp_radioButton',
                                          'selectionOption':'ml_animCurveEditor_selection_menu'},
                           annotation='Clamp keyframe values'
                           )
        mc.setParent('..')

        #                         __________
        #________________________/ Clean Up \_________
        tab6 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Various tools for deleting keys.')
        mc.separator(height=16, style='in')

        win.ButtonWithPopup(label='Delete Static Channels', command=deleteStaticChannels,  name='ml_animCurveEditor',
                            readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation="Delete all keys on channels which don't change value"
                            )

        win.ButtonWithPopup(label='Delete Redundant Keys', command=deleteRedundantKeys, name='ml_animCurveEditor',
                            readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation="Delete keyframes who's values are the same as previous and next key."
                            )

        win.ButtonWithPopup(label='Delete Sub-Frame Keys', command=deleteSubFrameKeys, name='ml_animCurveEditor',
                            readUI_toArgs={'selectionOption':'ml_animCurveEditor_selection_menu'},
                            annotation="Delete keys that aren't on a whole-number frame."
                            )
        mc.setParent('..')

        #                         __________
        #________________________/ Reduce \_________
        tab7 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Reduce keyframes on dense animation while maintaining motion.')
        mc.text('All channels on each node will be synchronized to the same frames.')
        mc.text('Drag slider to preview, changes apply when you release or change selection.')
        mc.separator(height=16, style='in')

        mc.intSliderGrp('ml_animCurveEditor_reduceCompression_slider',
                        label='Compression %', field=True, value=0,
                        minValue=0, maxValue=100,
                        dragCommand=_onReduceSliderDrag,
                        changeCommand=_onReduceSliderChange,
                        annotation='Drag to interactively reduce keyframes. 0 = no change, 100 = only first/last keys')

        mc.button(label='Reset', command=lambda *args: _keyframeReducer.reset(),
                  annotation='Reset to original keyframes')
        mc.setParent('..')

        #                    ___________
        #___________________/ Spline \___
        tab8 = mc.columnLayout(adj=True)

        mc.separator(height=8, style='none')
        mc.text('Unify keytimes across selected nodes, then convert to spline interpolation.')
        mc.separator(height=16, style='in')

        win.ButtonWithPopup(label='Convert Stepped to Spline', command=convertSteppedToSpline,
                            name='ml_animCurveEditor',
                            readUI_toArgs={'selectionOption': 'ml_animCurveEditor_selection_menu'},
                            annotation='Unify keytimes so every node has a key on every frame that any node has a key; then set tangents to spline.')
        mc.setParent('..')

        mc.tabLayout( tabs, edit=True, tabLabel=((tab1, 'Offset'),
                                                (tab2, 'Cut'),
                                                (tab3, 'Scale Time'),
                                                (tab4, 'Scale Value'),
                                                (tab5, 'Clamp'),
                                                (tab6, 'Clean Up'),
                                                (tab7, 'Reduce'),
                                                (tab8, 'Spline')
                                                ))


def _getKeySelection(selectionOption):

    keySel = utl.KeySelection()

    if selectionOption == 1:
        keySel.selectedObjects()
    elif selectionOption == 2:
        keySel.selectedChannels()
    elif selectionOption == 3:
        keySel.keyedInHierarchy()
    elif selectionOption == 4:
        keySel.visibleInGraphEditor()
    elif selectionOption == 5:
        keySel.scene()
    elif selectionOption == 6:
        keySel.selectedLayers()

    return keySel


def offset(frames=0, selectionOption=1):

    keySel = _getKeySelection(selectionOption)
    keySel.moveKey(frames)


def offsetCurrentTimeTo(frame=0, selectionOption=1):

    keySel = _getKeySelection(selectionOption)
    keySel.moveKey(frame-mc.currentTime(query=True))


def scaleTime(percent=100, selectionOption=1, pivotOption=0):

    value = percent/100.0
    keySel = _getKeySelection(selectionOption)

    timePivot = 0
    if pivotOption == 0:
        timePivot = mc.currentTime(query=True)
    else:
        times = keySel.getSortedKeyTimes()
        if pivotOption == 1:
            timePivot = times[0]
        elif pivotOption == 2:
            timePivot = times[-1]
        elif pivotOption == 3:
            timePivot = (times[0]+times[-1])/2

    keySel.scaleKey(timeScale=value, timePivot=timePivot)


def scaleValue(percent=100, selectionOption=1, pivotOption=0):

    value = percent/100.0
    keySel = _getKeySelection(selectionOption)
    valuePivot = 0
    if pivotOption:
        values = keySel.keyframe(query=True, valueChange=True)
        values = sorted(list(set(values)))
        if pivotOption == 1:
            valuePivot = values[-1]
        elif pivotOption == 2:
            valuePivot = values[0]
        elif pivotOption == 3:
            valuePivot = (values[0]+values[-1])/2

    keySel.scaleKey(valueScale=value, valuePivot=valuePivot)


def cutEarlier(selectionOption=1, setKey=True):

    keySel = _getKeySelection(selectionOption)
    keySel.fromBeginning()
    if setKey and keySel.findKeyframe('previous', time=(keySel._timeRangeEnd,)) < keySel._timeRangeEnd :
        mc.setKeyframe(keySel.curves, time=keySel._timeRangeEnd)
    keySel.cutKey()


def cutLater(selectionOption=1, setKey=True):

    keySel = _getKeySelection(selectionOption)
    keySel.toEnd()
    timeValue = keySel._timeRangeStart-keySel.shortestTime
    if setKey and keySel.findKeyframe('next', time=(timeValue,)) > timeValue:
        mc.setKeyframe(keySel.curves, time=(timeValue,))
    keySel.cutKey()


def cutSelected(selectionOption=1, setKey=True):

    keySel = _getKeySelection(selectionOption)
    if keySel.selectedKeys():pass
    elif keySel.frameRange():pass

    if setKey:
        start, end = keySel.time

        if keySel.findKeyframe('previous', time=(start-1,)) < start-1:
            mc.setKeyframe(keySel.curves, time=(start-1,), insert=True)

        if keySel.findKeyframe('next', time=(end,)) > end:
            mc.setKeyframe(keySel.curves, time=(end,), insert=True)

    keySel.cutKey()


def cutUnselected(selectionOption=1, setKey=True):

    keySel = _getKeySelection(selectionOption)
    start = None
    end = None
    if keySel.keyRange():
        start, end = keySel.time
    else:
        start, end = utl.frameRange()

    if setKey:
        if keySel.findKeyframe('previous', time=(start,)) < start:
            mc.setKeyframe(keySel.curves, time=(start,), insert=True)
        if keySel.findKeyframe('next', time=(end-1,)) > end-1:
            mc.setKeyframe(keySel.curves, time=(end-1,), insert=True)

    keySel.cutKey(time=(':'+str(start),))
    keySel.cutKey(time=(str(end)+':',))


def cutFrame(selectionOption=1):

    keySel = _getKeySelection(selectionOption)

    frame = mc.currentTime(query=True)
    keySel.cutKey(time=(frame,frame), includeSubFrames=True)

    #move everything after the cut
    keySel.keyframe(edit=True, time=(str(frame)+':',), relative=True, timeChange=-1)


def rippleCut(selectionOption=1, setKey=True):

    keySel = _getKeySelection(selectionOption)

    if keySel.selectedFrameRange():pass
    else: return

    start, end = keySel.time

    if setKey:
        if keySel.findKeyframe('previous', time=(start-1,)) < start-1:
            mc.setKeyframe(keySel.curves, time=(start-1,), insert=True)
        if keySel.findKeyframe('next', time=(end,)) > end:
            mc.setKeyframe(keySel.curves, time=(end,), insert=True)
        mc.setKeyframe(keySel.curves, time=(start-1,end), insert=True)

    keySel.cutKey()

    #move everything after the cut
    keySel.keyframe(edit=True, time=(str(end)+':',), relative=True, timeChange=start-end)


def insertFrame(selectionOption=1):

    keySel = _getKeySelection(selectionOption)

    #move everything after the current frame
    keySel.keyframe(edit=True, time=(str(mc.currentTime(query=True))+':',), relative=True, timeChange=1)


def clampValues(value=0, selectionOption=1, clampOption=0):
    keySel = _getKeySelection(selectionOption)

    for curve, values in zip(keySel.curves, keySel.values):
        indicies = None
        if clampOption==0:
            indicies = [i for i, x in enumerate(values) if x > value]
        elif clampOption==1:
            indicies = [i for i, x in enumerate(values) if x < value]
        if indicies:
            mc.keyframe(curve, index=utl.castToTime(indicies), edit=True, valueChange=value)
            mc.keyTangent(curve, index=utl.castToTime(indicies), itt='auto', ott='auto')


def deleteStaticChannels(selectionOption=1):

    keySel = _getKeySelection(selectionOption)

    for curve, values in zip(keySel.curves, keySel.values):
        #sometimes zero'd values aren't proper zero
        minTest = values[0]-0.000001
        maxTest = values[0]+0.000001
        if all(minTest <= x and maxTest >= x for x in values):
            mc.delete(curve)


def deleteRedundantKeys(selectionOption=1):

    keySel = _getKeySelection(selectionOption)
    for curve, values in zip(keySel.curves, keySel.values):
        groups = [list(g) for k, g in itertools.groupby(values)]
        i = -1
        cutIndex = list()
        for group in groups:
            gsize = len(group)
            if gsize > 2:
                cutIndex.extend(list(range(i+2,i+gsize)))
            i+=gsize
        if cutIndex:
            mc.cutKey(curve, index=utl.castToTime(cutIndex))


def deleteSubFrameKeys(selectionOption=1):

    keySel = _getKeySelection(selectionOption)
    for curve, times in zip(keySel.curves, keySel.times):
        cutTimes = [x for x in times if x % 1 != 0 and -9999 < x < 9999]
        if cutTimes:
            mc.cutKey(curve, time=utl.castToTime(cutTimes))


def convertSteppedToSpline(selectionOption=1):
    """
    Unify keytimes across selected nodes: for any frame that has a key on any node,
    set a key on all nodes at that frame (hold/stepped). Then convert all keys to spline.
    """
    keySel = _getKeySelection(selectionOption)
    if not keySel.curves:
        OpenMaya.MGlobal.displayWarning('No animation curves found.')
        return

    all_times = keySel.getSortedKeyTimes()
    if not all_times:
        return

    for curve in keySel.curves:
        existing = set(mc.keyframe(curve, query=True, timeChange=True) or [])
        missing = [t for t in all_times if t not in existing]
        if missing:
            mc.setKeyframe(curve, time=utl.castToTime(missing), insert=True)

    mc.keyTangent(keySel.curves, itt='spline', ott='spline')


class KeyframeReducer:
    """
    Manages interactive keyframe reduction with cached state.
    Pre-computes importance order so slider dragging is instant.
    """
    
    def __init__(self):
        self.reset_state()
        self._selection_job = None
    
    def reset_state(self):
        """Clear all cached state."""
        self.initialized = False
        self.curves_by_node = {}
        self.original_data = {}  # {curve: {time: value}}
        self.importance_order = {}  # {node: [times ordered by importance, least important first]}
        self.all_times_by_node = {}  # {node: set of all times}
        self.current_compression = 0
    
    def initialize(self, selectionOption):
        """
        Cache current keyframe data and pre-compute importance order.
        Call this before interactive editing begins.
        """
        # Clean up redundant keys first
        deleteRedundantKeys(selectionOption)
        
        keySel = _getKeySelection(selectionOption)
        if not keySel.curves:
            OpenMaya.MGlobal.displayWarning('No animation curves found.')
            return False
        
        self.reset_state()
        
        # Group curves by their source node
        for curve in keySel.curves:
            connections = mc.listConnections(curve, destination=True, source=False, plugs=True)
            if connections:
                node = connections[0].split('.')[0]
                if node not in self.curves_by_node:
                    self.curves_by_node[node] = []
                self.curves_by_node[node].append(curve)
        
        # For each node, cache data and compute importance order
        for node, curves in self.curves_by_node.items():
            self._cache_and_compute_importance(node, curves)
        
        self.initialized = True
        
        # Set up selection change callback to finalize
        if self._selection_job is not None:
            try:
                mc.scriptJob(kill=self._selection_job, force=True)
            except:
                pass
        self._selection_job = mc.scriptJob(event=['SelectionChanged', self._on_selection_changed], runOnce=True)
        
        return True
    
    def _cache_and_compute_importance(self, node, curves):
        """
        Cache keyframe data and compute importance order for one node's curves.
        Optimized with bisect for O(log n) segment lookup and incremental sorted list.
        """
        all_times = set()
        curve_data = {}
        curve_ranges = {}
        
        # Batch query all curve data
        for curve in curves:
            times = mc.keyframe(curve, query=True, timeChange=True)
            if times:
                all_times.update(times)
                values = mc.keyframe(curve, query=True, valueChange=True)
                time_value_map = dict(zip(times, values))
                curve_data[curve] = time_value_map
                self.original_data[curve] = dict(time_value_map)  # Copy for reset
                min_val, max_val = min(values), max(values)
                curve_ranges[curve] = max(max_val - min_val, 0.0001)
        
        if len(all_times) <= 2:
            self.all_times_by_node[node] = all_times
            self.importance_order[node] = []
            return
        
        sorted_times = sorted(all_times)
        self.all_times_by_node[node] = set(sorted_times)
        first_time, last_time = sorted_times[0], sorted_times[-1]
        num_curves = len(curve_data)
        
        # Pre-cache all curve values at all times for fast lookup
        # value_cache[curve_idx][time] = normalized_value (value / range)
        curve_list = list(curve_data.keys())
        value_cache = []
        for curve in curve_list:
            data = curve_data[curve]
            range_val = curve_ranges[curve]
            cache = {}
            for t in sorted_times:
                if t in data:
                    cache[t] = data[t] / range_val
                else:
                    # Evaluate curve at this time
                    vals = mc.keyframe(curve, query=True, time=(t,), eval=True, valueChange=True)
                    cache[t] = (vals[0] if vals else 0) / range_val
            value_cache.append(cache)
        
        # Run full RDP to get importance order (most important added first)
        # Use sorted list + bisect for O(log n) segment lookup
        sorted_keep = [first_time, last_time]  # Maintained sorted
        candidate_times = set(sorted_times[1:-1])
        addition_order = []
        
        while candidate_times:
            best_frame = None
            best_deviation = -1
            
            for t in candidate_times:
                # O(log n) segment lookup using bisect
                idx = bisect.bisect_left(sorted_keep, t)
                if idx == 0:
                    seg_start = sorted_keep[0]
                    seg_end = sorted_keep[0]
                elif idx >= len(sorted_keep):
                    seg_start = sorted_keep[-1]
                    seg_end = sorted_keep[-1]
                else:
                    seg_start = sorted_keep[idx - 1]
                    seg_end = sorted_keep[idx]
                
                if seg_start == seg_end:
                    continue
                
                # Calculate deviation using pre-cached normalized values
                seg_len = seg_end - seg_start
                ratio = (t - seg_start) / seg_len
                total_deviation = 0
                
                for cache in value_cache:
                    actual = cache[t]
                    linear_val = cache[seg_start] + ratio * (cache[seg_end] - cache[seg_start])
                    total_deviation += abs(actual - linear_val)
                
                if total_deviation > best_deviation:
                    best_deviation = total_deviation
                    best_frame = t
            
            if best_frame is not None:
                addition_order.append(best_frame)
                # O(log n) insertion to maintain sorted order
                bisect.insort(sorted_keep, best_frame)
                candidate_times.remove(best_frame)
            else:
                break
        
        # Reverse so least important is first (these get removed first at low compression)
        self.importance_order[node] = list(reversed(addition_order))
    
    def apply_compression(self, compression):
        """
        Apply the given compression level. Uses cached importance order for speed.
        """
        if not self.initialized:
            return
        
        self.current_compression = compression
        
        for node, curves in self.curves_by_node.items():
            all_times = self.all_times_by_node.get(node, set())
            if len(all_times) <= 2:
                continue
            
            sorted_times = sorted(all_times)
            importance_list = self.importance_order.get(node, [])
            
            # Calculate how many keys to keep
            target_count = max(2, int(len(sorted_times) * (1 - compression / 100.0)))
            
            # Always keep first and last, then keep most important frames
            # importance_list is ordered least->most important
            # So we remove from the front (least important) based on compression
            num_to_remove = len(sorted_times) - target_count
            times_to_remove = set(importance_list[:num_to_remove]) if num_to_remove > 0 else set()
            keep_times = all_times - times_to_remove
            
            # Apply to each curve
            for curve in curves:
                original = self.original_data.get(curve, {})
                current_times = set(mc.keyframe(curve, query=True, timeChange=True) or [])
                
                # Remove keys that shouldn't be there
                for t in current_times:
                    if t not in keep_times:
                        mc.cutKey(curve, time=(t, t))
                
                # Add back keys that should be there
                for t in keep_times:
                    if t not in current_times:
                        if t in original:
                            mc.setKeyframe(curve, time=t, value=original[t])
                        else:
                            mc.setKeyframe(curve, time=t, insert=True)
    
    def reset(self):
        """Reset to original keyframes (compression = 0)."""
        if not self.initialized:
            return
        
        # Restore all original keyframes
        for curve, data in self.original_data.items():
            current_times = set(mc.keyframe(curve, query=True, timeChange=True) or [])
            original_times = set(data.keys())
            
            # Remove keys not in original
            for t in current_times - original_times:
                mc.cutKey(curve, time=(t, t))
            
            # Add back original keys
            for t, v in data.items():
                if t not in current_times:
                    mc.setKeyframe(curve, time=t, value=v)
        
        self.current_compression = 0
        # Reset slider
        if mc.intSliderGrp('ml_animCurveEditor_reduceCompression_slider', exists=True):
            mc.intSliderGrp('ml_animCurveEditor_reduceCompression_slider', edit=True, value=0)
    
    def _on_selection_changed(self):
        """Called when selection changes - finalize and reset state."""
        self.reset_state()
        # Reset slider to 0
        if mc.intSliderGrp('ml_animCurveEditor_reduceCompression_slider', exists=True):
            mc.intSliderGrp('ml_animCurveEditor_reduceCompression_slider', edit=True, value=0)


# Global instance
_keyframeReducer = KeyframeReducer()


def _onReduceSliderDrag(value):
    """Called while slider is being dragged."""
    selectionOption = mc.optionMenuGrp('ml_animCurveEditor_selection_menu', query=True, select=True)
    
    # Initialize on first drag if needed
    if not _keyframeReducer.initialized:
        if not _keyframeReducer.initialize(selectionOption):
            return
    
    _keyframeReducer.apply_compression(value)


def _onReduceSliderChange(value):
    """Called when slider value changes (after drag release or field edit)."""
    # Same as drag - apply the compression
    _onReduceSliderDrag(value)


def _get_curve_value(curve, time, data_dict):
    """Get curve value at time, from cache or by evaluating."""
    if time in data_dict:
        return data_dict[time]
    vals = mc.keyframe(curve, query=True, time=(time,), eval=True, valueChange=True)
    return vals[0] if vals else 0


if __name__ == '__main__': ui()

