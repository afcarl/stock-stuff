import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import argparse
from Utils.FileHandling.CSV.csv_file import CSVFile
from Utils.FileHandling.HID import HIDFile
def main():
    parser = argparse.ArgumentParser(description="convert CSV file to hid file")
    parser.add_argument('input', type=str, help="path to input CSV file")
    parser.add_argument('output', type=str, help="path to output hid file")
    args = parser.parse_args()

    with CSVFile(args.input,'rt') as input_csv, HIDFile(args.output,'wb') as output_hid:
        output_hid.write_datapoints(input_csv.read_datapoints(),output_hid.hid_type)

if __name__ == '__main__':
    main()