import maya.cmds as mc
import ml_utilities as utl

def main(): 
    pass

def curve_data(animCurves):

    data = {}
    
    #get samples on every frame?


def segment_outlier(data, tolerance):
    #data is time and value pairs
    #interpolate between the first and last time
    #lerp through each key, save the one that is farthest from the average.

    timeRange = data[-1][0] - data[0][0]
    step = 1.0/timeRange
    test = 0
    outlierTime = None
    for each in timeRange:
        weight = (each[0]-data[0][0])*step
        lerp = data[0][1] * weight + data[-1][1] * (1-weight)
        delta = abs(each[1]-lerp)
        if delta > test and delta > tolerance:
            outlierTime = each[0]
    
    return outlierTime

def process_curves(animCurve):
    pass

def process_curve_test(animCurve, tolerance=0.1, start=None, end=None, ):
    times = mc.keyframe(animCurve, query=True, timeChange=True)
    values = mc.keyframe(animCurve, query=True, valueChange=True)
    data = zip(times, values)

