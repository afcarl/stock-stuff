import scipy.signal
import numpy

def find_local_minima(data_points, order):
    return scipy.signal.argrelextrema(numpy.array([x.close for x in data_points]),numpy.less,order=order)

find_local_minima([],2)


with HIDFile('../data/daily/table_qcom.csv', 'rt') as f:
    data_points = list(f.read_datapoints())[-1000:]
    ma = RSI(data_points, 14)
    x_axis = []
    y_axis = []
    for minutes, point in ma.calculate():
        x_axis.append(minutes)
        y_axis.append(point)
    plt.plot(x_axis[-10:], y_axis[-10:])
    plt.show()