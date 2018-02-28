import scipy.signal
import numpy

def find_local_minima(data_points, order):
    return scipy.signal.argrelextrema(numpy.array([x.close for x in data_points]),numpy.less,order=order)

def find_local_maxima(data_points, order):
    return scipy.signal.argrelextrema(numpy.array([x.close for x in data_points]),numpy.greater,order=order)
