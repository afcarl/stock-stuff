from src.DataPoint import DataPoint
def find_data(data_points):
    minutes = data_points[0].minutes
    high = 0.0
    low = 9999999999999.0
    volume = 0
    open_ = data_points[0].open
    close = data_points[-1].close
    for dp in data_points:
        if dp.high > high:
            high = dp.high
        if dp.low < low:
            low = dp.low
        volume += dp.volume
    return DataPoint(open_=open_, high=high, low=low, close=close, volume=volume, minutes=minutes)

def gen_new_intraday(data_points, num_minutes):
    all_periods = zip(*[iter(data_points)]*num_minutes)
    for chunk in all_periods:
        yield find_data(chunk)

def clean_minute_data(data_points):
    data_points_iterator = iter(data_points)
    ret_data_points = []
    num_minutes_missing = 0
    num_minutes = 0

    prev_dp = next(data_points_iterator)
    for dp in data_points_iterator:
        if dp.minutes - prev_dp.minutes == 1:
            num_minutes += 1
            ret_data_points.append(prev_dp)
        elif dp.minutes - prev_dp.minutes > 390:
            #trading day break... so dont do anything
            pass
        elif dp.minutes - prev_dp.minutes:
            num_minutes_missing += dp.minutes - prev_dp.minutes - 1
            ret_data_points.append(prev_dp)
            ret_data_points.extend(DataPoint.interpolate_datapoint(prev_dp,dp))
        prev_dp = dp
    print("num minutes missing",num_minutes_missing)
    print("num minutes",num_minutes)
    return ret_data_points



def count_missing(data_points):
    data_points_iterator = iter(data_points)
    num_minutes_missing = 0
    num_minutes = 0
    prev_dp = next(data_points_iterator)
    for dp in data_points_iterator:
        if dp.minutes - prev_dp.minutes == 1:
            num_minutes += 1
        elif dp.minutes - prev_dp.minutes > 390:
            # trading day break... so dont do anything
            pass
        elif dp.minutes - prev_dp.minutes:
            num_minutes_missing += dp.minutes - prev_dp.minutes - 1

        prev_dp = dp
    print("num minutes missing", num_minutes_missing)
    print("num minutes", num_minutes)
    percent = float(num_minutes_missing) / (float(num_minutes_missing)+float(num_minutes))
    print("percent missing",float(num_minutes_missing) / (float(num_minutes_missing)+float(num_minutes)))
    return percent*100.0