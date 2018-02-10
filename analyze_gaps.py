import data_parser
import os
from pprint import pprint

def detect_closed_gaps_in_range(data_points, periods):
    #slice off the very last #periods of data_points to avoid oob errors
    data_points_to_check = list(data_points)[:-periods]
    closed = 0
    gaps = 0
    for index, dp in enumerate(data_points_to_check):
        gaps += 1
        for test_dp in data_points[index+1:index+1+periods]:
            if test_dp.high >= dp.close >= test_dp.low:
                closed += 1
                #gap closed
                break
        else:
            pass
            #not closed in periods

    print('{:5.5%} gaps closed after {} periods'.format(closed / gaps,periods))



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
    detect_gaps_from_previous(parsed)
    detect_closed_gaps_in_range(parsed,2)
