from src.DataProvisioner import StockDataProvisioner, Timespan
from src.Analysis.LocalMinMax import find_local_minima

#def test_extrema():
with StockDataProvisioner('QCOM', Timespan.HOURS_4) as sdp:
    dps = sdp.read_datapoints()
    print(dps)
    print(find_local_minima(dps,5))