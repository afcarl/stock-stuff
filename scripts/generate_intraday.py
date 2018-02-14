import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import argparse
from Utils.FileHandling import *
from data_parser import gen_new_intraday

def main():
    parser = argparse.ArgumentParser(description='converts a smaller period intra file to a larger period intra day file')
    parser.add_argument('input', type=str, help='path to input data (.hid or .CSV)')
    parser.add_argument('output', type=str, help='path to output data (.hid or .CSV)')
    parser.add_argument('minutes', type=int, help='period length in minutes (> 1 minute')
    args = parser.parse_args()

    with DataFile(args.input, 'r') as input, DataFile(args.output, 'w') as output:
        output.write_datapoints(gen_new_intraday(input.read_datapoints(), args.minutes))

if __name__ == '__main__':
    main()