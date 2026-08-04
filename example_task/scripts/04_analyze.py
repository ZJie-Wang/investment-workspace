"""
Analyze weekly performance (2026-07-13 to 2026-07-17) + YTD + sector ranking + flows.
Generates figures and a summary CSV.
"""
import os, pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["axes.unicode_minus"] = False
try:
    plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC", "Heiti TC"]
except Exception:
    pass

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")
FIG = os.path.join(BASE, "..", "figures")
os.makedirs(FIG, exist_ok=True)

# ---------- identify trading days ----------
idx = pd.read_csv(os.path.join(DATA, "indices_daily_raw.csv"))
idx["trade_date"] = idx["trade_date"].astype(str)
all_dates = sorted(idx["trade_date"].unique())
last_date = all_dates[-1]            # 20260717
week_end_prev = None
# find the Friday of previous week: trading days before this week
# this week = 20260713..20260717 ; prev week end = 20260710
week_dates = [d for d in all_dates if "20260713" <= d <= "20260717"]
prev_week_end = max(d for d in all_dates if d < "20260713")
ytd_base = min(d for d in all_dates if d >= "20251229")  # last trading day of 2025
print("week:", week_dates, "prev_week_end:", prev_week_end, "ytd_base:", ytd_base)

# ---------- index weekly + YTD ----------
names = idx.drop_duplicates("ts_code")[["ts_code","name"]].set_index("ts_code")["name"].to_dict()
rows = []
for code, g in idx.sort_values("trade_date").groupby("ts_code"):
    g = g.set_index("trade_date")
    if last_date not in g.index or prev_week_end not in g.index or ytd_base not in g.index:
        continue
    close_last = g.loc[last_date, "close"]
    close_prev = g.loc[prev_week_end, "close"]
    close_ytd = g.loc[ytd_base, "close"]
    week_ret = (close_last/close_prev - 1)*100
    ytd_ret = (close_last/close_ytd - 1)*100
    rows.append({"ts_code":code,"name":names[code],
                 "close":close_last,"week_ret_%":round(week_ret,2),
                 "ytd_ret_%":round(ytd_ret,2)})
idx_tbl = pd.DataFrame(rows).sort_values("week_ret_%", ascending=False)
idx_tbl.to_csv(os.path.join(DATA,"index_summary.csv"), index=False)
print("\n=== Index weekly + YTD ===")
print(idx_tbl.to_string(index=False))

# chart: index weekly returns
fig, ax = plt.subplots(figsize=(9,5))
colors = ["#d62728" if v<0 else "#2ca02c" for v in idx_tbl["week_ret_%"]]
ax.barh(idx_tbl["name"], idx_tbl["week_ret_%"], color=colors)
ax.set_xlabel("本周涨跌 (%)")
ax.set_title(f"A股主要指数本周收益 ({week_dates[0]}~{week_dates[-1]})")
ax.axvline(0, color="k", lw=0.8)
for i,v in enumerate(idx_tbl["week_ret_%"]):
    ax.text(v, i, f" {v:+.2f}%", va="center", fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"01_index_weekly.png"), dpi=130); plt.close()

# ---------- sector (SW primary) weekly ----------
sw = pd.read_csv(os.path.join(DATA,"sw_daily_raw.csv"))
sw["trade_date"] = sw["trade_date"].astype(str)
# filter to 申万一级 using authoritative L1 classify list
l1 = pd.read_csv(os.path.join(DATA, "sw_l1_classify.csv"), dtype=str)
l1_codes = set(l1["index_code"])
sw1 = sw[sw["ts_code"].isin(l1_codes)].copy()
sect_rows = []
for code, g in sw1.sort_values("trade_date").groupby("ts_code"):
    g = g.set_index("trade_date")
    if last_date not in g.index or prev_week_end not in g.index:
        continue
    nm = g.loc[last_date,"name"]
    c0 = g.loc[prev_week_end,"close"]; c1 = g.loc[last_date,"close"]
    sect_rows.append({"ts_code":code,"name":nm,
                      "week_ret_%":round((c1/c0-1)*100,2),
                      "close":c1})
sect_tbl = pd.DataFrame(sect_rows).sort_values("week_ret_%", ascending=False)
sect_tbl.to_csv(os.path.join(DATA,"sector_weekly.csv"), index=False)
print(f"\n=== SW primary sectors ({len(sect_tbl)}) top/bottom 5 ===")
print("TOP:"); print(sect_tbl.head(5).to_string(index=False))
print("BOTTOM:"); print(sect_tbl.tail(5).to_string(index=False))

fig, ax = plt.subplots(figsize=(9,9))
colors = ["#d62728" if v<0 else "#2ca02c" for v in sect_tbl["week_ret_%"]]
ax.barh(sect_tbl["name"], sect_tbl["week_ret_%"], color=colors)
ax.set_xlabel("本周涨跌 (%)")
ax.set_title(f"申万一级行业本周收益 ({week_dates[0]}~{week_dates[-1]})")
ax.axvline(0, color="k", lw=0.8)
ax.invert_yaxis()
plt.tight_layout(); plt.savefig(os.path.join(FIG,"02_sector_weekly.png"), dpi=130); plt.close()

# ---------- flows: northbound + DC market ----------
hsgt = pd.read_csv(os.path.join(DATA,"moneyflow_hsgt_raw.csv"))
hsgt["trade_date"] = hsgt["trade_date"].astype(str)
hsgt = hsgt.sort_values("trade_date")
hsgt["north_net"] = pd.to_numeric(hsgt["north_money"], errors="coerce")
hsgt_recent = hsgt[hsgt["trade_date"]>="20260601"].copy()

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(hsgt_recent["trade_date"], hsgt_recent["north_net"]/1e4, color="#1f77b4")
ax.set_title("北向资金每日净流入 (亿元, 近期)")
ax.set_ylabel("亿元")
ax.axhline(0, color="k", lw=0.8)
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(os.path.join(FIG,"03_northbound.png"), dpi=130); plt.close()

# weekly northbound net
wk_hsgt = hsgt[hsgt["trade_date"].isin(week_dates)]
nb_week = wk_hsgt["north_net"].sum()/1e4
print(f"\n北向资金本周累计净流入: {nb_week:.2f} 亿元")

mkt = pd.read_csv(os.path.join(DATA,"moneyflow_mkt_dc_raw.csv"))
mkt["trade_date"] = mkt["trade_date"].astype(str)
mkt = mkt.sort_values("trade_date")
mkt_recent = mkt[mkt["trade_date"]>="20260601"].copy()
fig, ax = plt.subplots(figsize=(10,5))
net = pd.to_numeric(mkt_recent["net_amount"], errors="coerce")/1e8
ax.bar(mkt_recent["trade_date"], net, color="#ff7f0e")
ax.set_title("大盘资金净流入 (DC, 亿元, 近期)")
ax.set_ylabel("亿元"); ax.axhline(0, color="k", lw=0.8)
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(os.path.join(FIG,"04_mkt_flow.png"), dpi=130); plt.close()
wk_mkt = mkt[mkt["trade_date"].isin(week_dates)]
mkt_week = pd.to_numeric(wk_mkt["net_amount"], errors="coerce").sum()/1e8
print(f"大盘资金(DC)本周累计净流入: {mkt_week:.2f} 亿元")

# ---------- valuation snapshot ----------
basic = pd.read_csv(os.path.join(DATA,"index_dailybasic_raw.csv"))
basic["trade_date"] = basic["trade_date"].astype(str)
basic_last = basic[basic["trade_date"]==last_date][["ts_code","pe_ttm","pb","turnover_rate_f"]]
basic_last = basic_last.dropna()
print("\n=== Valuation @", last_date, "===")
print(basic_last.to_string(index=False))

# ---------- index trend chart (last 3 months) ----------
fig, ax = plt.subplots(figsize=(10,5))
for code in ["000001.SH","399001.SZ","399006.SZ","000300.SH","000852.SH"]:
    g = idx[idx["ts_code"]==code].sort_values("trade_date").copy()
    g = g[g["trade_date"]>="20260417"]
    g["ret"] = g["close"]/g["close"].iloc[0]*100
    ax.plot(g["trade_date"], g["ret"], label=names[code])
ax.set_title("主要指数相对走势 (近3个月, 归一为100)")
ax.legend(); plt.xticks(rotation=45); ax.set_ylabel("归一化")
plt.tight_layout(); plt.savefig(os.path.join(FIG,"05_index_trend.png"), dpi=130); plt.close()

print("\nFigures saved to", FIG)
