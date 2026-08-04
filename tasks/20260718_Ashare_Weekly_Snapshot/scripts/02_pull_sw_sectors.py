"""
Pull Shenwan (申万) industry index daily quotes for the recent week.
Source: Tushare sw_daily (doc_id=327). 申万2021一级行业 (31 sectors).
We pull by trade_date for the last ~10 trading days.
"""
import os, tushare as ts, pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
pro = ts.pro_api(os.environ["TUSHARE_TOKEN"])

# Pull recent trading days from index file
idx = pd.read_csv(os.path.join(OUT, "indices_daily_raw.csv"))
dates = sorted(idx["trade_date"].unique())[-12:]

frames = []
for d in dates:
    df = pro.sw_daily(trade_date=str(d))
    if df is not None and len(df):
        frames.append(df)
        print(d, "rows:", len(df))

raw = pd.concat(frames, ignore_index=True)
raw.to_csv(os.path.join(OUT, "sw_daily_raw.csv"), index=False)
print("saved", raw.shape, "dates:", dates[0], "..", dates[-1])
print("cols:", list(raw.columns))
