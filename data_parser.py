from collections import namedtuple
import datetime

data_order = ['date','time','open','high','low','close','volume','split','earnings','dividends','extrapolation']

DataPoint = namedtuple('DataPoint',data_order)

def default_data_point():
    return DataPoint(datetime.datetime.strptime('19690101', '%Y%m%d').date(),
                     0,
                     1.0,
                     1.0,
                     1.0,
                     1.0,
                     1.0,
                     '','','','')

def line_to_data_point(line):
    args = []
    data_points = line.split(',')
    try:
        args.append(datetime.datetime.strptime(data_points[0], '%Y%m%d').date())
    except:
        args.append(datetime.datetime.strptime(data_points[0], '%m/%d/%Y').date())
    args.append(int(data_points[1])) # time
    args.append(float(data_points[2])) #open
    args.append(float(data_points[3])) #high
    args.append(float(data_points[4])) #low
    args.append(float(data_points[5])) #close
    args.append(float(data_points[6])) #volume

    try:
        args.append(data_points[7]) # split
    except:
        args.append('')
    try:
        args.append(data_points[8]) # earnings
    except:
        args.append('')
    try:
        args.append(data_points[9]) # dividends
    except:
        args.append('')
    try:
        args.append(data_points[10]) # extrapolation
    except:
        args.append('')

    return DataPoint(*args)


def parse_csv(path):
    with open(path,'r') as f:
        for line in f:
            line = line.strip()
            dp = line_to_data_point(line)
            yield dp

