from copy import deepcopy
from decimal import Decimal
from packages.contracts import PatchOp, PolicyPatchRule

def vulnerable_policy():
    return {"policy_version":"v1", "global_constraints":{"max_discount_pct":40,"max_discount_duration_months":6,"cooldown_days_between_offers":0,"min_margin_pct_after_offer":30,"offer_ladder_no_repeat":False}, "rules":[{"rule_id":"r_grifter","offer":{"type":"percent_off","discount_pct":40,"duration_months":6},"ladder_position":1}]}
class PolicyEngine:
    def __init__(self, policy=None): self.policy=policy or vulnerable_policy(); self.history=[deepcopy(self.policy)]
    def validate_patch(self, patch:PolicyPatchRule)->bool:
        c=self.policy["global_constraints"]
        for op in patch.operations:
            if op.op=="lower_ceiling" and Decimal(str(op.value)) > c["max_discount_pct"]: return False
            if op.op=="shorten_duration" and int(op.value) > c["max_discount_duration_months"]: return False
            if op.op=="extend_cooldown" and int(op.value) < c["cooldown_days_between_offers"]: return False
            if op.op=="raise_margin_floor" and Decimal(str(op.value)) < c["min_margin_pct_after_offer"]: return False
            if op.op=="substitute_offer" and op.value != "non_monetary": return False
        return not patch.requires_human_approval
    def apply(self, patch:PolicyPatchRule):
        if not self.validate_patch(patch): raise ValueError("Rejected: patch loosens policy or needs approval")
        p=deepcopy(self.policy); c=p["global_constraints"]
        for op in patch.operations:
            if op.op=="lower_ceiling": c["max_discount_pct"]=Decimal(str(op.value))
            elif op.op=="shorten_duration": c["max_discount_duration_months"]=int(op.value)
            elif op.op=="extend_cooldown": c["cooldown_days_between_offers"]=int(op.value)
            elif op.op=="raise_margin_floor": c["min_margin_pct_after_offer"]=Decimal(str(op.value))
            elif op.op=="substitute_offer":
                for r in p["rules"]: r["offer"]={"type":"consultation","discount_pct":0,"duration_months":0}
            elif op.op=="disable_rule": p["rules"]=[r for r in p["rules"] if r["rule_id"] != op.rule_id]
        p["policy_version"]="v"+str(len(self.history)+1); self.policy=p; self.history.append(deepcopy(p)); return p
