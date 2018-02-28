from src.DataProvisioner import StockDataProvisioner, Timespan
from src.Indicators.MACD import MACD

def test_MACD():
    with StockDataProvisioner('QCOM',Timespan.HOURS_4) as sdp:
        macd = MACD(list(sdp.read_datapoints()))
        for m in macd.calculate():
            print(m)