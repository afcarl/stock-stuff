import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from data_parser import clean_minute_data
from Utils.FileHandling.CSV.csv_file import CSVFile


for csv in os.listdir('../../1minute/'):
    print(csv)
    with CSVFile('../../1minute/' + csv, 'r+t') as input, CSVFile('../../1minutenew/' +csv, 'wt') as output:
        clean = clean_minute_data(input.read_datapoints())
        output.write_datapoints(clean)
