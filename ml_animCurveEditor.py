# 
#   -= ml_animCurveEditor.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 2, 2016-05-01
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_animCurveEditor.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_animCurveEditor
#     ml_animCurveEditor.ui()
# From MEL, this looks like:
#     python("import ml_animCurveEditor;ml_animCurveEditor.ui()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Various tools for editing animation curves, similar to video clip non-linear editing tools.
# Maya's tools for editing lots of keys can be slow or cumbersome, this is meant to be
# an alternative interface for editing lots of keyframes.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# The "Act on Anim Curves In:" drop-down controls which animCurves are affected in the scene.
# The tabs organize the different types of tools:
#   Offset: Slip curves in time.
#   Cut: Cut sections of curves.
#   Scale Time: Globally retime a curve
#   Scale Value: Globally adjust the value of a curve.
#   Clamp: Clamp keyframe values to a high or low value, for example to prevent a channel going below zero.
#   Clean-Up: Tools for getting rid of keyframes that you may not want or need.
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
__revision__ = 2


import maya.cmds as mc
from maya import OpenMaya

import itertools

try:
    import ml_utilities as utl
    utl.upToDateCheck(17)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
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
        
        mc.tabLayout( tabs, edit=True, tabLabel=((tab1, 'Offset'), 
                                                (tab2, 'Cut'), 
                                                (tab3, 'Scale Time'), 
                                                (tab4, 'Scale Value'), 
                                                (tab5, 'Clamp'),
                                                (tab6, 'Clean Up')
                                                ))
                                                

def _getKeySelection(selectionOption):
    
    selectedPreset = mc.optionMenuGrp('ml_animCurveEditor_selection_menu', query=True, select=True)
    
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
                cutIndex.extend(range(i+2,i+gsize))
            i+=gsize
        if cutIndex:
            mc.cutKey(curve, index=utl.castToTime(cutIndex))


def deleteSubFrameKeys(selectionOption=1):
    
    keySel = _getKeySelection(selectionOption)
    for curve, times in zip(keySel.curves, keySel.times):
        cutTimes = [x for x in times if x % 1 != 0 and -9999 < x < 9999]
        if cutTimes:
            mc.cutKey(curve, time=utl.castToTime(cutTimes))


if __name__ == '__main__': ui()


#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2016-02-29 : First publish.
#
# Revision 2: 2016-05-01 : Fixing command name typo.
