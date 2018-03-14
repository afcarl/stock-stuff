from src.DataProvisioner import StockDataProvisioner, Timespan
from src.Indicators.AccumulationDistribution import AccumulationDistribution
from src.Indicators.MACD import MACD

def test_MACD():
    with StockDataProvisioner('QCOM',Timespan.HOURS_4) as sdp:
        macd = MACD(list(sdp.read_datapoints()))
        for m in macd.calculate():
            pass

def test_ADL():
    with StockDataProvisioner('QCOM', Timespan.HOURS_4) as sdp:
        adl = AccumulationDistribution(list(sdp.read_datapoints()))
        for m in adl.calculate():
            pass
