from datetime import datetime, timezone
from uuid import uuid4
from decimal import Decimal
from packages.contracts import *
def run(run_id=None):
    account=AccountHealth(account_id="acct_001",tier="Business",mrr=Decimal("500"),seats_purchased=40,seats_active_30d=8,churn_probability=.82,confidence_interval=(.76,.88),primary_dropoff_vector=DropoffVector.SEAT_UNDERUTILIZATION,contributing_factors=[ShapFactor(feature="active_seat_ratio",shap_value=.39,direction="up")],urgency_tier=UrgencyTier.CRITICAL,days_to_predicted_churn=12,predicted_arr_at_risk=Decimal("6000"))
    return AtRiskCohort(run_id=run_id or uuid4(),emitted_by=AgentName.WATCHDOG,accounts=[account],model_version="baseline-1",scored_at=datetime.now(timezone.utc),cohort_arr_at_risk=Decimal("6000"))
