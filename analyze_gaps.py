import data_parser
import os
from pprint import pprint

def within_error_margin(close, low, high, error_margin=.01):
    percent_diff_low = abs((low - close) / close)
    percent_diff_high = abs((high - close) / close)
    return error_margin > percent_diff_low and error_margin > percent_diff_high


def detect_closed_gaps_in_range(data_points, periods):
    data_points = list(data_points)
    closed = 0
    gaps = 0
    num_periods_to_close = 0
    for index, dp in enumerate(data_points):
        gaps += 1
        for num_periods,test_dp in enumerate(data_points[index+1:index+1+periods]):
            if within_error_margin(dp.close,test_dp.low,test_dp.high):
                gaps -= 1
                break

            if test_dp.high >= dp.close >= test_dp.low:
                closed += 1
                num_periods_to_close += num_periods+1
                break
        else:
            pass
            #not closed in periods

    print('{:5.5%} gaps ({}/{}) closed after {} periods'.format(closed / gaps, closed, gaps, periods))
    print('average amount of time to close gap {}'.format(float(num_periods_to_close) / closed))
    print('{} gaps and {} total periods'.format(gaps,len(data_points)))


def detect_gaps_from_previous(data_points):
    return detect_closed_gaps_in_range(data_points, 1)

for csv in os.listdir('data/daily/'):
    print(csv)
    parsed = data_parser.parse_csv('data/daily/' + csv)
    detect_gaps_from_previous(parsed)
    #detect_closed_gaps_in_range(parsed,1)
