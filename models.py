import itertools
from datetime import date, datetime


class Credit:
    @property
    def end_date(self):
        return self._end_date

    id_iter = itertools.count()

    def __init__(self, start_date, end_date):
        self.id = next(Credit.id_iter)
        self._start_date = start_date
        self._end_date = end_date
        self.tranches = []

    def __str__(self):
        return f'Credit ID: {self.id} '

    start_date = property()

    @start_date.setter
    def start_date(self, str_date):
        self._start_date = datetime.strptime(
            str_date, '%Y-%m-%d'
        ).date()

    @start_date.getter
    def start_date(self):
        return self._start_date

    end_date = property()

    @end_date.setter
    def end_date(self, str_date):
        self._end_date = datetime.strptime(
            str_date, '%Y-%m-%d'
        ).date()

    @end_date.getter
    def end_date(self):
        return self._end_date

    def is_open_credit(self):
        return date.today() < datetime.strptime(self._end_date, '%Y-%m-%d').date()

    def create_tranche(self, percent, max_sum):
        self.tranches.append(Tranche(self,
                                     percent=percent,
                                     max_sum=max_sum)
                             )

    def get_tranche(self, tranche_id):
        return self.tranches[tranche_id]


class Tranche:
    id_iter = itertools.count()

    def __init__(self, credit, percent, max_sum):
        self.id = next(Tranche.id_iter)
        self.credit = credit
        self.percent = percent
        self.max_sum = max_sum
        self.current_amount = 0
        self._threshold_limit = 0

    def __str__(self):
        return f"{self.credit}, " \
               f"{self.id}, " \
               f"{self.percent}, " \
               f"{self.current_amount}, " \
               f"{self.threshold_limit}"

    @property
    def threshold_limit(self):
        return self.max_sum - self.current_amount

    def can_investment(self, amount):
        return bool(amount <= self.threshold_limit)


class Investor:
    id_iter = itertools.count()

    def __init__(self, name, account=1000):
        self.id = next(Investor.id_iter)
        self.name = name
        self.account = account

    def __str__(self):
        return f"Investor:{self.id}  {self.name}"

    def balance_check(self, amount):
        return amount <= self.account


class Investment:
    def __init__(self,
                 tranche,
                 investor,
                 sum_invest,
                 date_invest_str):
        self.tranche = tranche
        self.investor = investor
        self.sum = sum_invest
        self._date_invest = date_invest_str

    date_invest = property()

    @date_invest.setter
    def date_invest(self, str_date):
        datetime.strptime(
            str_date, '%Y-%m-%d'
        ).date()

    @date_invest.getter
    def date_invest(self):
        return datetime.strptime(
            self._date_invest, '%Y-%m-%d'
        ).date()
