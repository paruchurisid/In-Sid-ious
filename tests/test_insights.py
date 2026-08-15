from data.generator.swarm_telemetry import generate
from services.api.insights import insight, portfolio
def test_each_account_has_matching_stage_state(tmp_path):
 accounts,_=generate(tmp_path); rows=[insight(a) for a in accounts]
 assert len(rows)==10 and all(0 <= r["utilization_ratio"] <= 1 for r in rows)
 assert next(r for r in rows if r["account_id"]=="acct_001")["state"]=="critical"
 assert next(r for r in rows if r["account_id"]=="acct_009")["state"]=="healthy"
 assert portfolio(accounts)["at_risk_mrr"]==53600
