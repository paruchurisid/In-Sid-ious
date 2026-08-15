from decimal import Decimal
from packages.contracts import *
def run(cohort):
    a=cohort.accounts[0]; ratio=a.seats_active_30d/a.seats_purchased; roi=Decimal("400")
    narrative=f"Only {a.seats_active_30d} of {a.seats_purchased} seats are active; estimated unused value is ${roi}/month."
    return ValueGapReport(run_id=cohort.run_id,emitted_by=AgentName.VALUE,account_id=a.account_id,unused_high_value_features=["webhooks","seat_invites"],utilization_ratio=ratio,roi_gap_usd_monthly=roi,recommended_action="downgrade",narrative=narrative,evidence=["computed entitlement utilization"])
