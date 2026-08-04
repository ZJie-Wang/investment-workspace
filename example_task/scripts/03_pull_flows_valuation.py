"""
Pull market flows:
  - moneyflow_hsgt: 沪深港通资金流向 (northbound) doc_id=47
  - moneyflow_mkt_dc: 大盘资金流向(DC) doc_id=345
Also index_dailybasic (doc_id=128): PE/PB/turnover for major indices.
"""
import os, tushare as ts, pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
pro = ts.pro_api(os.environ["TUSHARE_TOKEN"])

# 1. Northbound (HSGT) - last ~150 trading days for trend; here get last 3 months
hsgt = pro.moneyflow_hsgt(start_date="20260401", end_date="20260717")
hsgt.to_csv(os.path.join(OUT, "moneyflow_hsgt_raw.csv"), index=False)
print("hsgt", hsgt.shape, "cols:", list(hsgt.columns))

# 2. DC market flow
mkt = pro.moneyflow_mkt_dc(start_date="20260401", end_date="20260717")
mkt.to_csv(os.path.join(OUT, "moneyflow_mkt_dc_raw.csv"), index=False)
print("mkt_dc", mkt.shape, "cols:", list(mkt.columns))

# 3. index_dailybasic for major indices (valuation/breadth)
INDICES = ["000001.SH","399001.SZ","399006.SZ","000688.SH","000016.SH",
           "000300.SH","000905.SH","000852.SH"]
frames = []
for code in INDICES:
    try:
        df = pro.index_dailybasic(ts_code=code, start_date="20260101", end_date="20260717")
        if df is not None and len(df):
            frames.append(df)
            print(code, "rows:", len(df))
    except Exception as e:
        print(code, "ERR:", e)
basic = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
basic.to_csv(os.path.join(OUT, "index_dailybasic_raw.csv"), index=False)
print("basic", basic.shape, "cols:", list(basic.columns))
