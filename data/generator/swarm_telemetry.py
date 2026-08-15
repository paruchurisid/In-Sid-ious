"""Deterministic 10-account / 90-day telemetry and closed-loop audit fixture generator."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
import numpy as np

SEED = 42
PROFILES = [
    ("acct_001", "Northstar Logistics", "seat_shelf_ghost"),
    ("acct_002", "Alpine Health", "seat_shelf_ghost"),
    ("acct_003", "Beacon Commerce", "discount_grifter"),
    ("acct_004", "Cobalt Media", "discount_grifter"),
    ("acct_005", "Delta Legal", "feature_stranded_team"),
    ("acct_006", "Evergreen Foods", "feature_stranded_team"),
    ("acct_007", "Fathom Security", "critical_churn_risk"),
    ("acct_008", "Granite Systems", "critical_churn_risk"),
    ("acct_009", "Harbor Works", "healthy_anchor"),
    ("acct_010", "Indigo Labs", "healthy_anchor"),
]

def make_telemetry(account_id, name, archetype, rng):
    paid = {"seat_shelf_ghost": 60, "discount_grifter": 35, "feature_stranded_team": 45, "critical_churn_risk": 50, "healthy_anchor": 40}[archetype]
    mrr = {"seat_shelf_ghost": 7200, "discount_grifter": 4200, "feature_stranded_team": 6400, "critical_churn_risk": 9000, "healthy_anchor": 5800}[archetype]
    start = datetime(2026, 5, 4, tzinfo=timezone.utc); days=[]
    for day in range(90):
        if archetype == "seat_shelf_ghost": active=max(6, int(16+rng.normal(0,1))); feature={"webhooks":0,"api_calls":active*12,"reports":active*2,"seat_invites":0}; health=.38
        elif archetype == "discount_grifter": active=int(29+rng.normal(0,2)); feature={"webhooks":8,"api_calls":active*60,"reports":active*5,"seat_invites":2}; health=.72
        elif archetype == "feature_stranded_team": active=int(34+rng.normal(0,2)); feature={"webhooks":0,"api_calls":active*18,"reports":active*8,"seat_invites":1}; health=.61
        elif archetype == "critical_churn_risk":
            factor=1 if day < 76 else max(.15,1-(day-76)*.12); active=max(3,int((43+rng.normal(0,2))*factor)); feature={"webhooks":int(10*factor),"api_calls":int(active*45*factor),"reports":int(active*4*factor),"seat_invites":0}; health=round(.84*factor,2)
        else: active=min(paid,int(35+day*.05+rng.normal(0,2))); feature={"webhooks":15,"api_calls":int(active*(70+day*.4)),"reports":active*7,"seat_invites":3}; health=.91
        days.append({"timestamp":(start+timedelta(days=day)).isoformat(),"paid_seats":paid,"active_seats_dau":active,"active_seats_wau":min(paid,max(active,int(active*1.35))),"feature_events_daily":feature,"health_score":round(float(health),2),"mrr_usd":mrr})
    return {"account_id":account_id,"account_name":name,"archetype":archetype,"telemetry":days}

def audit_event(account_id, name, archetype):
    is_grifter=archetype == "discount_grifter"; run_id=str(uuid5(NAMESPACE_URL, "retention-swarm/"+account_id)); ratio="0.20" if not is_grifter else "0.83"
    discount="40" if is_grifter else "35"; erosion="1800.00" if is_grifter else "1260.00"
    action="downgrade" if not is_grifter else "rightsizing"; unused=["webhooks","seat_invites"] if not is_grifter else ["audit_log"]
    return {"run_id":run_id,"account_id":account_id,"account_name":name,"archetype":archetype,"timestamp":"2026-08-01T12:00:00+00:00","gap":{"unused_high_value_features":unused,"utilization_ratio":float(ratio),"roi_gap_usd_monthly":"400","recommended_action":action,"narrative":f"{name} has a measured utilization gap requiring {action}.","evidence":["90-day telemetry aggregation","entitlement comparison"]},"before_offer":{"text":f"{discount}% discount for six months","offer_type":"percent_off","discount_pct":discount,"duration_months":6,"sequence_idx":1,"rule_id":"r_grifter" if is_grifter else "r_seat_shelf"},"alerts":[{"vuln_class":"uncapped_discount","severity":"critical","persona_ids":["persona_grifter_001" if is_grifter else "persona_shelf_001"],"ltv_erosion_usd":erosion,"annualized_exposure_usd":str(float(erosion)*40),"offending_rule_ids":["r_grifter" if is_grifter else "r_seat_shelf"]},{"vuln_class":"unnecessary_concession","severity":"high","persona_ids":["persona_grifter_001" if is_grifter else "persona_shelf_001"],"ltv_erosion_usd":"0.00","annualized_exposure_usd":"0.00","offending_rule_ids":["r_grifter" if is_grifter else "r_seat_shelf"]}],"patch":{"patch_id":"patch-"+account_id,"base_policy_version":"v1","operations":[{"op":"lower_ceiling","value":30,"rule_id":None},{"op":"shorten_duration","value":3,"rule_id":None},{"op":"extend_cooldown","value":180,"rule_id":None},{"op":"substitute_offer","value":"non_monetary","rule_id":None}],"justification":"Caps monetary concessions and replaces the repeatable discount with value recovery.","projected_margin_saved_usd":erosion,"projected_save_rate_delta":-0.02,"requires_human_approval":False},"after_offer":{"text":"Complimentary workflow consultation and right-sizing review","offer_type":"consultation","discount_pct":"0","duration_months":0,"sequence_idx":2,"rule_id":"r_grifter" if is_grifter else "r_seat_shelf"},"masr_before":"0.8000","masr_after":"0.9500","improved":True}

def generate(output="data/generated_swarm"):
    rng=np.random.default_rng(SEED); result=[make_telemetry(*profile,rng) for profile in PROFILES]; audits=[audit_event(*profile) for profile in PROFILES if profile[2] in {"seat_shelf_ghost","discount_grifter"}]
    root=Path(output); root.mkdir(parents=True,exist_ok=True); (root/"accounts_telemetry.json").write_text(json.dumps(result,indent=2)); (root/"swarm_audit_events.json").write_text(json.dumps(audits,indent=2)); return result,audits
if __name__ == "__main__":
    accounts,audits=generate(); print(f"Generated {len(accounts)} accounts, {len(accounts)*90} daily telemetry records, and {len(audits)} audit events.")
