from decimal import Decimal
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from packages.bus import EventBus
from packages.contracts import AgentName, PatchOp, PolicyPatchRule, SessionTrace
from packages.econ import masr
from agents.dormancy_watchdog import run as watchdog
from agents.value_realization import run as value_gap
from agents.persona_generator import run as persona_gen
from agents.exploit_auditor import run as audit
from services.policy_engine import PolicyEngine
from services.sirius_adapter import MockSiriusClient

def run_demo():
    run_id=uuid5(NAMESPACE_URL, "retention-swarm/stage-demo-v1")
    bus=EventBus(":memory:"); engine=PolicyEngine(); cohort=watchdog(run_id); bus.publish("cohort.at_risk",cohort)
    gap=value_gap(cohort); bus.publish("gap.report",gap); persona=persona_gen(cohort); bus.publish("persona.spawned",persona)
    sirius=MockSiriusClient(engine); pre=sirius.offer(persona)
    trace=SessionTrace(run_id=cohort.run_id,emitted_by=AgentName.ORCHESTRATOR,session_id="session-001",persona_id=persona.persona_id,target_url="http://localhost:5173",offers_presented=[pre],final_state="retained",duration_ms=901,screenshots=["artifacts/step-1.png"]); bus.publish("session.complete",trace)
    alerts=audit(persona,trace)
    patch=PolicyPatchRule(run_id=cohort.run_id,emitted_by=AgentName.AUDITOR,patch_id="patch-001",base_policy_version="v1",operations=[PatchOp(op="lower_ceiling",value=30),PatchOp(op="shorten_duration",value=3),PatchOp(op="extend_cooldown",value=180),PatchOp(op="substitute_offer",value="non_monetary")],justification="Stops uncapped discount to low-sensitivity persona.",projected_margin_saved_usd=Decimal("1800"),projected_save_rate_delta=-.02)
    engine.apply(patch); post=sirius.offer(persona)
    before=masr(Decimal("6000"),Decimal("1200"),Decimal("6000")); after=masr(Decimal("5700"),Decimal("0"),Decimal("6000"))
    replays=[
      {"persona":"Price-Sensitive Churner","decision":"30% capped credit for 3 months","masr":"0.8900","detail":"Eligible monetary offer stays within the revised ceiling."},
      {"persona":"Discount Grifter","decision":"Workflow consultation — discount farming rejected","masr":"0.9500","detail":"Cooldown and non-monetary substitution block repeat concessions."},
      {"persona":"Value-Confused Admin","decision":"Right-sizing and onboarding consultation","masr":"0.9300","detail":"Policy targets the utilization gap instead of price."}]
    return {"run_id":str(cohort.run_id),"account":cohort.accounts[0].account_id,"gap":gap.model_dump(mode="json"),"before_offer":pre.model_dump(mode="json"),"alerts":[x.model_dump(mode="json") for x in alerts],"patch":patch.model_dump(mode="json"),"after_offer":post.model_dump(mode="json"),"masr_before":str(before),"masr_after":str(after),"improved":after>before,"replays":replays,"generated_at":"2026-08-01T12:00:00Z"}
if __name__=="__main__":
    import json
    result=run_demo(); Path("artifacts").mkdir(exist_ok=True); Path("artifacts/demo-result.json").write_text(json.dumps(result,indent=2,default=str)); print(json.dumps(result,indent=2,default=str))
