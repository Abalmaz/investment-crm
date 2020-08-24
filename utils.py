from calendar import monthrange


def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]


def calculate_profit(invest_sum,
                     percent,
                     days_in_month,
                     invest_days):
    return ((invest_sum / 100 * percent) / days_in_month) * invest_days
