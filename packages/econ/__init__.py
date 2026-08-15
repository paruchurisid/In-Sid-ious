from decimal import Decimal
def ltv_erosion(discount_pct: Decimal, mrr: Decimal, months: int, gross_margin_pct: Decimal) -> Decimal:
    return (discount_pct / 100 * mrr * months * gross_margin_pct / 100).quantize(Decimal("0.01"))
def masr(retained_arr: Decimal, discount_cost: Decimal, at_risk_arr: Decimal) -> Decimal:
    if at_risk_arr <= 0: raise ValueError("at_risk_arr must be positive")
    return ((retained_arr-discount_cost)/at_risk_arr).quantize(Decimal("0.0001"))
def margin_after_discount(discount_pct: Decimal, gross_margin_pct: Decimal) -> Decimal:
    return (gross_margin_pct-discount_pct).quantize(Decimal("0.01"))
