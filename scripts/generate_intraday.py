import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import argparse
from Utils.FileHandling import *
from data_parser import gen_new_intraday
from Utils.FileHandling.HID import *
from multiprocessing import Pool

def main(hids, minutes):
    for f in hids:
        input_path = '../data/1minute/' + f
        output_path = '../data/'+str(minutes) + 'minute/' + f.replace('hid.xz','csv')
        start = time.time()
        with CSVFile(input_path, 'rt+') as input_hid, CSVFile(output_path, 'wt+') as output_csv:
            output_csv.write_datapoints(gen_new_intraday(input_hid.read_datapoints(), minutes))
        end = time.time()
        print("took",(end-start),'seconds to convert',f)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

import time
if __name__ == '__main__':
    #csv_sets = split(sorted(os.listdir('../data/minute')),4)
    #pool = Pool(processes=4)
    #print(pool.map(main, csv_sets))
    hids = os.listdir('../data/1minute')
    main(hids, 5)