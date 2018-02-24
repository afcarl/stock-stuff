import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from src.data_parser import count_missing
from src.Utils.FileHandling import HIDFile
import operator

stock_to_missing = dict()
for hid in os.listdir('../data/1minute/'):
    with HIDFile('../data/1minute/' + hid, 'r+b') as input:
        print("scoring",hid)
        percent = count_missing(input.read_datapoints())
        stock_to_missing[hid] = percent
for stock,percent in sorted(stock_to_missing.items(), key=operator.itemgetter(1)):
    print (stock,percent)
