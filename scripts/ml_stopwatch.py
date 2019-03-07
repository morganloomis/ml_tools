# -= ml_stopwatch.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 4
#   / / / / / / /  2018-02-17
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
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_stopwatch.py
# 
# Run the tool in a python shell or shelf button by importing the module, 
# and then calling the primary function:
# 
#     import ml_stopwatch
#     ml_stopwatch.ui()
# 
# 
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Record the timing of mouse clicks to help you plan out the timing of your shot.
# Clicks are reported in a UI that allows you to record notes for individual beats
# and navigate through them in the timeslider.
# 
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the UI, and then click the big button to start recording time. Once
# recording has begun, continue clicking the big button to record the timing of
# beats. When you're done recording, click the stop button to stop recording and
# open up the results UI. From there you can change the start frame if you want a
# different reference point for your timing. Click the individual frame buttons or
# the previous and next buttons to navigate between the beats. Use the text fields
# to write notes about specific beats.
# 
#     _________
# - -/__ Ui __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# [] Round to nearest frame : Only whole number frames
# [Stop] : Stop the recording.
# [<< Previous] : Go to the previous frame in the list.
# [Next >>] : Go to the next frame in the list.
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
__revision__ = 4
__category__ = 'animation'


import maya.cmds as mc
from maya import OpenMaya
import time

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


STOPWATCH = None

def ui():
    '''
    User interface for stopwatch
    '''

    with utl.MlUi('ml_stopwatch', 'Stopwatch', width=400, height=175, info='''Press the start button to start recording.
Continue pressing to set marks.
When finished, press the stop button and the report will pop up.''') as win:

        mc.checkBoxGrp('ml_stopwatch_round_checkBox',label='Round to nearest frame', value1=True, annotation='Only whole number frames')

        mc.text('ml_stopwatch_countdown_text', label='Ready...')

        mc.button('ml_stopwatch_main_button', label='Start', height=80)
        _setButtonStart()
        mc.button(label='Stop', command=_stopButton, annotation='Stop the recording.')


def _startButton(*args):
    '''
    Run when the start button is pressed, gathers args and starts the stopwatch.
    '''

    global STOPWATCH
    _setButtonMark()

    rounded = mc.checkBoxGrp('ml_stopwatch_round_checkBox', query=True, value1=True)

    kwargs = dict()
    kwargs['startFrame'], null = utl.frameRange()

    if rounded:
        kwargs['roundTo'] = 0

    STOPWATCH = Stopwatch(**kwargs)
    STOPWATCH.start()


def _markButton(*args):
    '''
    Run when the Mark button is pressed, records a mark with the stopwatch.
    '''
    global STOPWATCH
    STOPWATCH.mark()


def _stopButton(*args):

    global STOPWATCH
    _setButtonStart()
    if not STOPWATCH:
        return
    STOPWATCH.stop()


def _setButtonStart(*args):
    '''
    Resets the UI text and button labels.
    '''
    mc.button('ml_stopwatch_main_button', edit=True, label='Start', command=_startButton, annotation='Start the timer. Once running, use this same button to set marks.')
    mc.text('ml_stopwatch_countdown_text', edit=True, label='Ready...')


def _setButtonMark(*args):
    '''
    Sets the UI text and button labels during recording.
    '''
    mc.button('ml_stopwatch_main_button', edit=True, label='Mark', command=_markButton, annotation='Record a mark.')
    mc.text('ml_stopwatch_countdown_text', edit=True, label='Recording...')


def addMarksToScene(marks):
    '''
    This is temp and will possibly be rolled into future releases.
    '''

    start,end = utl.frameRange()
    camera = utl.getCurrentCamera()
    camShape = mc.listRelatives(camera, shapes=True)[0]
    aov = mc.getAttr(camShape+'.horizontalFilmAperture')

    name = 'ml_stopwatch_'

    numStopwatches = len(mc.ls(name+'*', type='locator'))
    top = mc.spaceLocator(name=name+'#')

    ename = ':'.join([str(x) for x in marks])
    mc.addAttr(top, longName='keyTimes', at='enum', enumName=ename, keyable=True)

    markRange = float(marks[-1]-marks[0])
    viewWidth = aov*2
    viewHeight = -0.4*aov+(numStopwatches*aov*0.08)
    depth = 5

    for mark in marks[1:-1]:

        ann = mc.annotate(top, text=str(mark))
        mc.setAttr(ann+'.displayArrow', 0)

        #parent
        annT = mc.parent(mc.listRelatives(ann, parent=True, path=True), top)[0]
        annT = mc.rename(annT, 'mark_'+str(round(mark)))
        ann = mc.listRelatives(annT, shapes=True, path=True)[0]

        #set the position
        normalX = float(mark-marks[0])/markRange-0.5
        mc.setAttr(annT+'.translateX', viewWidth*normalX*2)
        mc.setAttr(annT+'.translateY', viewHeight)
        mc.setAttr(annT+'.translateZ', -depth)

        #keyframe for color
        mc.setAttr(ann+'.overrideEnabled', 1)

        mc.setKeyframe(ann, attribute='overrideColor', value=17, time=(int(marks[0]-1),int(mark+1)))
        mc.setKeyframe(ann, attribute='overrideColor', value=13, time=(int(mark),))
        mc.keyTangent(ann+'.overrideColor', ott='step')


    mc.select(clear=True)
    mc.parentConstraint(camera, top)


class Stopwatch(object):

    def __init__(self, startFrame=0, endFrame=None, addMarkers=True, roundTo=2):
        '''
        Initializes the stopwatch.
        '''

        self.frameRate = utl.getFrameRate()

        self.startFrame = int(startFrame)
        self.endFrame = endFrame
        self.addMarkers = True
        self.roundTo = roundTo

        self.markTime = list()


    def start(self):
        '''
        Starts the stopwatch.
        '''
        self.startTime = time.time()


    def stop(self):
        '''
        Stop the stopwatch and convert the time to frames.
        '''

        if not self.markTime:
            OpenMaya.MGlobal.displayWarning('No marks recorded, the "Mark" button needs to be pressed at least once after recording is started.')
            return

        #don't mark the last frame
        #self.mark()
        self.elapsed = self.markTime[-1] - self.startTime

        #mark frames
        self.frameMarks = [0]
        for m in self.markTime:

            seconds = m - self.startTime
            frame = (seconds*self.frameRate)
            frame = round(frame, self.roundTo)

            if not self.roundTo:
                frame = int(frame)

            self.frameMarks.append(frame)

        self.ui()


    def mark(self):
        '''
        Save the current time.
        '''

        self.markTime.append(time.time())


    def ui(self):
        '''
        Launch a UI to display the marks that were recorded.
        '''

        with utl.MlUi('ml_stopwatchReport', 'Stopwatch Report', width=400, height=400, info='''This is the report from the stopwatch you just ran.
Adjust the start frame, and then press the frame buttons to jump to that frame.
The fields on the right can be used for notes.''', menu=False) as win:

            self.uiSlider = mc.intSliderGrp(field=True, label='Start Frame', value=self.startFrame,
                minValue=((-0.5*self.frameMarks[-1])+self.startFrame), maxValue=(self.frameMarks[-1]/2)+self.startFrame,
                fieldMinValue=-1000, fieldMaxValue=1000,
                changeCommand=self.uiUpdateStartFrame)

            self.frameRateField = mc.intFieldGrp(label='Frame Rate', value1=self.frameRate, enable1=False, extraLabel='fps', annotation='')

            mc.scrollLayout()
            mc.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 50), (2, 80), (3, 340)])
            mc.text('Frame')
            mc.text('Duration')
            mc.text('Notes')

            for i in range(3):
                mc.separator(style='single', height=15)

            self.uiButton = list()

            for i in range(len(self.frameMarks)):

                #frame button
                frame = self.frameMarks[i]+self.startFrame
                self.uiButton.append(mc.button(label=str(frame), annotation='Go to frame %i' % frame,command='import maya.cmds;maya.cmds.currentTime(%i,edit=True)' % frame))

                #duration text
                if i:
                    mc.text(label=str(self.frameMarks[i]-self.frameMarks[i-1]))
                else:
                    mc.text(label='Start')

                #notes field
                mc.textField()

            #add the stop
            mc.text(label='')
            mc.text(label='Stop')
            mc.setParent('..')
            mc.setParent('..')

            #next and prev buttons!
            mc.paneLayout(configuration='vertical2',separatorThickness=1)
            mc.button(label='<< Previous', command=self.previousFrame, annotation='Go to the previous frame in the list.')
            mc.button(label='Next >>', command=self.nextFrame, annotation='Go to the next frame in the list.')


    def previousFrame(self, *args):
        '''
        Go to the previous frame based on the current time and frame list.
        '''
        current = mc.currentTime(query=True)
        for f in [x+self.startFrame for x in reversed(self.frameMarks)]:
            if current <= f:
                continue
            mc.currentTime(f)
            break


    def nextFrame(self, *args):
        '''
        Go to the next frame based on the current time and frame list.
        '''
        current = mc.currentTime(query=True)
        for f in [x+self.startFrame for x in self.frameMarks]:
            if current >= f:
                continue
            mc.currentTime(f)
            break


    def uiUpdateStartFrame(self, *args):
        '''
        Update the UI text with the new frames when the slider is updated.
        '''

        self.startFrame = mc.intSliderGrp(self.uiSlider, query=True, value=True)

        for b,f in zip(self.uiButton, self.frameMarks):
            frame = f+self.startFrame
            mc.button(b, edit=True, label=str(frame), annotation='Go to frame %i' % frame, command='import maya.cmds;maya.cmds.currentTime(%i,edit=True)' % frame)


if __name__ == '__main__': ui()



#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 1: 2012-06-04 : First publish.
#
# Revision 2: 2014-03-01 : adding category
#
# Revision 3: 2016-05-01 : Fixing go to frame buttons import error.
#
# Revision 4: 2018-02-17 : Updating license to MIT.