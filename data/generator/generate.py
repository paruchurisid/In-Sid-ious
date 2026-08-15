"""Deterministic compact generator; scale with --accounts for fuller demos."""
import argparse, json
from pathlib import Path
from datetime import date, timedelta
import numpy as np
import polars as pl
ARCHETYPES=[("silent_decay",.12),("champion_departure",.08),("failed_onboarding",.09),("seat_overprovisioned",.07),("frustration_driven",.08),("budget_cut",.06),("price_shock",.05),("discount_grifter",.04),("payment_failure",.03),("healthy_growth",.18),("healthy_seasonal",.12),("healthy_lumpy",.08)]
def main():
 p=argparse.ArgumentParser();p.add_argument("--accounts",type=int,default=2000);a=p.parse_args(); rng=np.random.default_rng(42); out=Path("data/parquet");out.mkdir(parents=True,exist_ok=True)
 names=[x for x,w in ARCHETYPES for _ in range(round(w*a.accounts))][:a.accounts]; ids=[f"acct_{i:04d}" for i in range(a.accounts)]
 accounts=pl.DataFrame({"account_id":ids,"archetype":names,"tier":["Business" if i%3 else "Pro" for i in range(a.accounts)],"seats_purchased":rng.integers(5,100,a.accounts),"mrr":rng.integers(100,1200,a.accounts)})
 accounts.write_parquet(out/"accounts.parquet")
 dates=[date(2026,7,1)+timedelta(days=i) for i in range(31)]; rows=[]
 for i,archetype in enumerate(names):
  for day,d in enumerate(dates):
   base=max(1,20-(day*.25 if archetype=="silent_decay" else 0)); rows.append((d,ids[i],int(base),int(base*.7),int(base*100)))
 events=pl.DataFrame(rows,schema=["date","account_id","logins","active_seats","api_calls"],orient="row");events.write_parquet(out/"daily_events.parquet")
 keys, counts=np.unique(names,return_counts=True)
 manifest={"seed":42,"accounts":a.accounts,"archetype_counts":{str(k):int(v) for k,v in zip(keys,counts)},"churn_rate":.22,"files":["accounts.parquet","daily_events.parquet"]}; Path("data/manifest.json").write_text(json.dumps(manifest,indent=2)); print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
