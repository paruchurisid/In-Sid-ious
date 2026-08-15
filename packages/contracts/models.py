from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class AgentName(StrEnum):
    WATCHDOG="dormancy_watchdog"; VALUE="value_realization"; PERSONA="persona_generator"; AUDITOR="exploit_auditor"; ORCHESTRATOR="orchestrator"
class DropoffVector(StrEnum):
    LOGIN_DECAY="login_decay"; CHAMPION_DEPARTURE="champion_departure"; ONBOARDING_INCOMPLETE="onboarding_incomplete"; SEAT_UNDERUTILIZATION="seat_underutilization"; ERROR_FRUSTRATION="error_frustration"; BILLING_FAILURE="billing_failure"; RENEWAL_PRICE_SHOCK="renewal_price_shock"
class UrgencyTier(StrEnum): CRITICAL="critical"; HIGH="high"; WATCH="watch"
class PersonaArchetype(StrEnum):
    DISCOUNT_GRIFTER="discount_grifter"; FRUSTRATED_DEV="frustrated_dev"; COST_CUTTING_CFO="cost_cutting_cfo"; CASUAL_QUITTER="casual_quitter"; PRICE_SHOCKED_RENEWER="price_shocked_renewer"; OVERPROVISIONED_ADMIN="overprovisioned_admin"
class VulnerabilityClass(StrEnum):
    UNCAPPED_DISCOUNT="uncapped_discount"; DISCOUNT_STACKING="discount_stacking"; OFFER_LADDER_CYCLING="offer_ladder_cycling"; COOLDOWN_BYPASS="cooldown_bypass"; MARGIN_NEGATIVE_OFFER="margin_negative_offer"; UNNECESSARY_CONCESSION="unnecessary_concession"; ELIGIBILITY_LOGIC_FLAW="eligibility_logic_flaw"
class SwarmPayload(BaseModel):
    schema_version: str="1.0"; run_id: UUID=Field(default_factory=uuid4); emitted_at: datetime=Field(default_factory=lambda: datetime.now(timezone.utc)); emitted_by: AgentName
class ShapFactor(BaseModel): feature:str; shap_value:float; direction:Literal["up","down"]
class AccountHealth(BaseModel):
    account_id:str; tier:str; mrr:Decimal; seats_purchased:int; seats_active_30d:int; churn_probability:float; confidence_interval:tuple[float,float]; primary_dropoff_vector:DropoffVector; contributing_factors:list[ShapFactor]; urgency_tier:UrgencyTier; days_to_predicted_churn:int; predicted_arr_at_risk:Decimal
class AtRiskCohort(SwarmPayload): accounts:list[AccountHealth]; model_version:str; scored_at:datetime; cohort_arr_at_risk:Decimal
class ValueGapReport(SwarmPayload):
    account_id:str; unused_high_value_features:list[str]; utilization_ratio:float; roi_gap_usd_monthly:Decimal; recommended_action:Literal["educate","downgrade","expand","support_escalate","pause_offer"]; narrative:str; evidence:list[str]
class SyntheticPersona(SwarmPayload):
    persona_id:str; archetype:PersonaArchetype; derived_from_account_id:str; price_sensitivity:float; aggression:float; negotiation_rounds_max:int; walk_away_threshold:str; accepts_non_monetary_offers:bool; stated_reason:str; hidden_true_reason:str; system_prompt:str
class CapturedOffer(BaseModel): text:str; offer_type:str; discount_pct:Decimal; duration_months:int; sequence_idx:int; rule_id:str
class SessionTrace(SwarmPayload):
    session_id:str; persona_id:str; target_url:str; offers_presented:list[CapturedOffer]; final_state:Literal["retained","cancelled","errored","abandoned"]; duration_ms:int; screenshots:list[str]=[]; video_path:str="artifacts/session.webm"
class PersuasionScore(SwarmPayload): persona_id:str; score:int; friction_rating:int; addressed_true_reason:bool; tone_flags:list[str]; qualitative_feedback:str; rubric_version:str="v1"; scoring_variance:float|None=0.0
class VulnerabilityAlert(SwarmPayload):
    vuln_class:VulnerabilityClass; severity:Literal["critical","high","medium","low"]; reproduction:list[str]; persona_ids:list[str]; ltv_erosion_usd:Decimal; annualized_exposure_usd:Decimal; offending_rule_ids:list[str]; evidence_session_ids:list[str]
class PatchOp(BaseModel): op:Literal["lower_ceiling","shorten_duration","extend_cooldown","narrow_eligibility","raise_margin_floor","substitute_offer","disable_rule"]; value:object|None=None; rule_id:str|None=None
class PolicyPatchRule(SwarmPayload): patch_id:str; base_policy_version:str; operations:list[PatchOp]; justification:str; projected_margin_saved_usd:Decimal; projected_save_rate_delta:float; requires_human_approval:bool=False
