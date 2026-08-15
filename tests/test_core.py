from decimal import Decimal
import pytest
from packages.econ import ltv_erosion,masr
from services.policy_engine import PolicyEngine
from packages.contracts import AgentName, PatchOp, PolicyPatchRule
from agents.dormancy_watchdog import run
from packages.bus import EventBus
def test_economics(): assert ltv_erosion(Decimal("40"),Decimal("500"),12,Decimal("75")) == Decimal("1800.00"); assert masr(Decimal("6000"),Decimal("1200"),Decimal("6000")) == Decimal("0.8000")
def test_bus_roundtrip(tmp_path):
 c=run(); bus=EventBus(tmp_path/"events.db");bus.publish("cohort",c);assert bus.replay("cohort",type(c))[0].run_id==c.run_id
def test_policy_rejects_loosen():
 e=PolicyEngine();p=PolicyPatchRule(emitted_by=AgentName.AUDITOR,patch_id="x",base_policy_version="v1",operations=[PatchOp(op="lower_ceiling",value=50)],justification="bad",projected_margin_saved_usd=Decimal(0),projected_save_rate_delta=0)
 with pytest.raises(ValueError): e.apply(p)
def test_demo_improves_masr():
 from services.orchestrator.demo_cycle import run_demo
 assert run_demo()["improved"]
