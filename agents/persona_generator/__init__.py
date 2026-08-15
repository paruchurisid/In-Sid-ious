from packages.contracts import *
def run(cohort):
    a=cohort.accounts[0]
    return SyntheticPersona(run_id=cohort.run_id,emitted_by=AgentName.PERSONA,persona_id="persona_grifter_001",archetype=PersonaArchetype.DISCOUNT_GRIFTER,derived_from_account_id=a.account_id,price_sensitivity=.15,aggression=.9,negotiation_rounds_max=3,walk_away_threshold="Demands a monetary discount.",accepts_non_monetary_offers=False,stated_reason="budget",hidden_true_reason=a.primary_dropoff_vector.value,system_prompt="Negotiate aggressively; seek repeat discounts.")
