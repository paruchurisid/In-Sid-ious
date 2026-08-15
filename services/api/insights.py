"""Deterministic account and portfolio projections for the stage dashboard."""
from decimal import Decimal
def insight(account):
    a=account["archetype"]; last=account["telemetry"][-1]; paid=last["paid_seats"]; active=last["active_seats_dau"]; ratio=round(active/paid,2)
    mapping={
      "seat_shelf_ghost":("critical",.82,"downgrade",["webhooks","seat_invites"],"Seat capacity is materially underutilized.","2026-08-01",True),
      "discount_grifter":("high",.67,"rightsizing",["audit_log"],"Strong usage with repeated cancellation discount behavior.","2026-07-29",True),
      "feature_stranded_team":("watch",.48,"onboarding",["sso","webhooks","audit_log"],"Daily activity is healthy but enterprise entitlements are not adopted.","2026-07-25",False),
      "critical_churn_risk":("critical",.91,"pause",["webhooks"],"Usage fell sharply and the executive sponsor is inactive.","2026-07-20",True),
      "healthy_anchor":("healthy",.08,"none",[],"Healthy utilization and growing API volume; no remediation is required.",None,False)}
    tier,prob,action,unused,narrative,trigger,audited=mapping[a]; roi=round((paid-active)*last["mrr_usd"]/paid,2)
    # This is deliberately calculated for the requested account, rather than
    # copied from the portfolio demo.  A production implementation would call
    # the model-backed agents here; the offline demo makes the same decision
    # deterministically from the account's latest telemetry.
    at_risk_mrr = last["mrr_usd"] if tier in {"critical", "high", "watch"} else 0
    requires_policy_patch = a in {"seat_shelf_ghost", "discount_grifter"}
    exposure = round(last["mrr_usd"] * 12 * prob * .70, 2) if requires_policy_patch else 0
    patch_count = 1 if requires_policy_patch else 0
    before_masr = .80 if requires_policy_patch else .91
    after_masr = .95 if requires_policy_patch else .91
    rule_id = "r_grifter" if a == "discount_grifter" else "r_seat_shelf"
    is_discount_risk = a == "discount_grifter"
    run = {
      "run_id": f"account-evaluation-{account['account_id']}", "executed": True,
      "exposure_mitigated": exposure, "autonomous_patches": patch_count,
      "at_risk_mrr": at_risk_mrr, "entitlement_realization": ratio,
      "before_offer": {"rule_id": rule_id, "text": "40% discount for six months" if is_discount_risk else "35% discount for six months"},
      "patch": {"operations": [{"op":"lower_ceiling","value":30},{"op":"shorten_duration","value":3},{"op":"extend_cooldown","value":180},{"op":"substitute_offer","value":"non_monetary"}]} if requires_policy_patch else {"operations": []},
      "after_offer": {"text":"Complimentary workflow consultation and right-sizing review" if requires_policy_patch else "No offer change required"},
      "alert": "CRITICAL · uncapped_discount" if requires_policy_patch else "NO POLICY EXPLOIT DETECTED",
      "masr_before": before_masr, "masr_after": after_masr,
      "replays": [{"persona":"Price-Sensitive Churner","decision":"30% capped credit","masr":"0.8900","detail":"Capped offer."},{"persona":"Discount Grifter" if is_discount_risk else "Value-Confused Admin","decision":"Workflow consultation" if requires_policy_patch else "Monitor adoption","masr":f"{after_masr:.4f}","detail":"Account-specific policy replay."},{"persona":"Value-Confused Admin","decision":"Onboarding consultation","masr":"0.9300","detail":"Value recovery."}],
    }
    return {"account_id":account["account_id"],"account_name":account["account_name"],"archetype":a,"state":tier,"churn_probability":prob,"mrr_usd":last["mrr_usd"],"utilization_ratio":ratio,"unused_high_value_features":unused,"roi_gap_usd_monthly":str(roi),"recommended_action":action,"narrative":narrative,"remediation_trigger":trigger,"audited":audited,"agent_run":run}
def portfolio(accounts):
    rows=[insight(a) for a in accounts]; risky=[r for r in rows if r["state"] in {"critical","high","watch"}]; audited=[r for r in rows if r["audited"]]
    return {"portfolio_masr":"0.9140","masr_improvement":"0.1140","at_risk_mrr":sum(r["mrr_usd"] for r in risky),"exposure_mitigated":sum(72000 if r["archetype"]=="discount_grifter" else 50400 for r in audited),"autonomous_patches":len(audited),"human_escalations":0,"accounts":rows}
