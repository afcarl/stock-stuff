from DataPoint import DataPoint


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

