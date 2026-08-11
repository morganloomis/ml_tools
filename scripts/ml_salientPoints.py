import maya.cmds as mc
import ml_utilities as utl

def main(): 
    pass

def curve_data(animCurves):
    data = {}
    if not isinstance(animCurves, (list, tuple)):
        animCurves = [animCurves]
    for curve in animCurves:
        times = mc.keyframe(curve, query=True, timeChange=True) or []
        values = mc.keyframe(curve, query=True, valueChange=True) or []
        data[curve] = list(zip(times, values))
    return data


def segment_outlier(data, tolerance):
    if not data or len(data) < 2:
        return None
    timeRange = data[-1][0] - data[0][0]
    if timeRange == 0:
        return None
    step = 1.0 / timeRange
    test = 0
    outlierTime = None
    for each in data:
        weight = (each[0] - data[0][0]) * step
        lerp = data[0][1] * (1 - weight) + data[-1][1] * weight
        delta = abs(each[1] - lerp)
        if delta > test and delta > tolerance:
            test = delta
            outlierTime = each[0]
    return outlierTime

def process_curves(animCurve):
    pass

def process_curve_test(animCurve, tolerance=0.1, start=None, end=None, ):
    times = mc.keyframe(animCurve, query=True, timeChange=True)
    values = mc.keyframe(animCurve, query=True, valueChange=True)
    data = zip(times, values)

