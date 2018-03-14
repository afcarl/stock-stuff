from src.DataProvisioner import StockDataProvisioner, Timespan
from src.Analysis.LocalMinMax import find_local_minima, find_local_maxima

def test_extrema():
    with StockDataProvisioner('QCOM', Timespan.HOURS_4) as sdp:
        dps = list(sdp.read_datapoints())
        minima = find_local_minima(dps,100)
        print(minima)
        for minimum in minima[0]:
            pass

        maxima = find_local_maxima(dps, 100)
        print(maxima)
        for maximum in maxima[0]:
            pass