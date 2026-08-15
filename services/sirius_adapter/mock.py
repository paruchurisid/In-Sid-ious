from decimal import Decimal
from packages.contracts import CapturedOffer, SyntheticPersona
class MockSiriusClient:
    def __init__(self, engine): self.engine=engine; self.log=[]
    def offer(self, persona:SyntheticPersona):
        rule=self.engine.policy["rules"][0] if self.engine.policy["rules"] else {"rule_id":"fallback","offer":{"type":"consultation","discount_pct":0,"duration_months":0}}
        o=rule["offer"]; offer=CapturedOffer(text=("40% discount" if o["discount_pct"] else "Complimentary workflow consultation"),offer_type=o["type"],discount_pct=Decimal(str(o["discount_pct"])),duration_months=o["duration_months"],sequence_idx=len(self.log)+1,rule_id=rule["rule_id"]); self.log.append(offer); return offer
