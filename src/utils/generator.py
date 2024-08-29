def generate_subscription(plan, rate: float, discount: str) -> tuple[str, float, str]:
    if rate in [2.99, 7.99, 9.99]:
        if not plan:
            if rate == 2.99:
                return 'Basic (Ads)', rate, discount
            elif rate == 7.99:
                return 'Premium (No Ads)', rate, discount
            elif rate == 9.99:
                return 'Premium (No Ads)', rate, discount
        else:
            return plan, rate, discount
    else:
        if plan:
            if plan == 'Basic (Ads)':
                return plan, 2.99, discount
            elif plan == 'Premium (No Ads)' and discount == 'No':
                return plan, 9.99, discount
            elif plan == 'Premium (No Ads)' and discount == 'Yes':
                return plan, 7.99, discount
