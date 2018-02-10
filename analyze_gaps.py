import data_parser
import os
from pprint import pprint

def within_error_margin(close, low, high, error_margin=.01):
    percent_diff_low = abs((low - close) / close)
    percent_diff_high = abs((high - close) / close)
    return error_margin > percent_diff_low and error_margin > percent_diff_high


def detect_closed_gaps_in_range(data_points, periods):
    #slice off the very last #periods of data_points to avoid oob errors
    data_points_to_check = list(data_points)[:-periods]
    total_periods = len(data_points_to_check)
    closed = 0
    gaps = 0
    num_periods_to_close = 0
    for index, dp in enumerate(data_points_to_check):
        gaps += 1
        for num_periods,test_dp in enumerate(data_points[index+1:index+1+periods]):
            if within_error_margin(dp.close,test_dp.low,test_dp.high):
                gaps -= 1
                #the open and close are so close that there's no point in trying to analyze
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
    print('{} gaps and {} total periods'.format(gaps,total_periods))


def detect_gaps_from_previous(data_points):
    gaps = []
    num_gaps = 0
    num_gaps_closed = 0
    gap_sum = 0.0
    prev_dp = None
    first = True
    for dp in data_points:
        if first:
            first = False
            prev_dp = dp
            continue
        gap = dp.open - prev_dp.close
        gap_sum += abs(gap) / prev_dp.close
        percent_diff = gap / prev_dp.close
        gap_up = gap > 0.0
        closed = dp.high >= prev_dp.close >= dp.low

        num_gaps += 1
        if closed:
            num_gaps_closed += 1
        out_str = '{:2.2%} gap {} {} closed next day'.format(percent_diff,'up' if gap_up else 'down', '' if closed else 'not')
        #print(out_str)
        prev_dp = dp

    print('gaps closed',num_gaps_closed)
    print('gaps not closed',num_gaps - num_gaps_closed)
    print('average gap {:5.5%}'.format(gap_sum / num_gaps))


def analyze_gaps(data_points):
    pass

for csv in os.listdir('data/daily/'):
    print(csv)
    parsed = list(data_parser.parse_csv('data/daily/' + csv))
    #detect_gaps_from_previous(parsed)
    detect_closed_gaps_in_range(parsed,1)
