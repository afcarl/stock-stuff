import pyEX

syms = pyEX.refdata.symbols()

for thing in sorted(syms, key= lambda x: x['symbol']):
    print(thing)
