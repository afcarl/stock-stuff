import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from data_parser import count_missing
from Utils.FileHandling.CSV.csv_file import CSVFile
import operator

stock_to_missing = dict()
for csv in os.listdir('../../1minute/'):
    with CSVFile('../../1minute/' + csv, 'r+t') as input:
        print("scoring",csv)
        percent = count_missing(input.read_datapoints())
        stock_to_missing[csv] = percent
for stock,percent in sorted(stock_to_missing.items(), key=operator.itemgetter(1)):
    print (stock,percent)
