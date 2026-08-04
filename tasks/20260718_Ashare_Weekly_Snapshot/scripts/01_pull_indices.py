"""
Pull major A-share index daily quotes for the recent ~3 weeks + YTD.
Source: Tushare index_daily (doc_id=95)
Data as-of: 2026-07-18 (Sat). Last trading day expected 2026-07-17 (Fri).
"""
import os
import tushare as ts
import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

pro = ts.pro_api(os.environ["TUSHARE_TOKEN"])

INDICES = {
    "000001.SH": "上证指数",
    "399001.SZ": "深证成指",
    "399006.SZ": "创业板指",
    "000688.SH": "科创50",
    "000016.SH": "上证50",
    "000300.SH": "沪深300",
    "000905.SH": "中证500",
    "000852.SH": "中证1000",
    "899050.BJ": "北证50",
}

frames = []
for code in INDICES:
    df = pro.index_daily(ts_code=code, start_date="20251230", end_date="20260717")
    df["name"] = INDICES[code]
    frames.append(df)
    print(code, INDICES[code], "rows:", len(df))

raw = pd.concat(frames, ignore_index=True)
raw.to_csv(os.path.join(OUT, "indices_daily_raw.csv"), index=False)
print("saved", raw.shape, "date range:", raw["trade_date"].min(), raw["trade_date"].max())
