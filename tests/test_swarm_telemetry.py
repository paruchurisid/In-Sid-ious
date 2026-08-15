from data.generator.swarm_telemetry import generate
def test_swarm_fixture_shape(tmp_path):
 accounts, audits=generate(tmp_path)
 assert len(accounts)==10 and all(len(x["telemetry"])==90 for x in accounts)
 assert {x["archetype"] for x in accounts} == {"seat_shelf_ghost","discount_grifter","feature_stranded_team","critical_churn_risk","healthy_anchor"}
 assert len(audits)==4 and all(x["improved"] and x["after_offer"]["discount_pct"]=="0" for x in audits)
