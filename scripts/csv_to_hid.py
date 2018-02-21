import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from multiprocessing import Pool

import argparse
from Utils.FileHandling.CSV.csv_file import CSVFile
from Utils.FileHandling.HID.hid_file import HIDFile
def main(csvs):
    for f in csvs:
        if not f.endswith('csv'):
            continue
        input_path = '../data/240minute/' + f
        output_path = '../data/240minute/' + f.replace('csv','hid')
        start = time.time()
        with CSVFile(input_path, 'rt') as input_csv, HIDFile(output_path, 'wb') as output_hid:
            output_hid.write_datapoints(input_csv.read_datapoints(), output_hid.hid_type)
        end = time.time()
        print("took",(end-start),'seconds to convert',f)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

import time
if __name__ == '__main__':
    csv_sets = split(sorted(os.listdir('../data/240minute')),2)
    pool = Pool(processes=2)
    print(pool.map(main, csv_sets))


