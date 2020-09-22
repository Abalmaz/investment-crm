import itertools
from datetime import date, datetime
from dataclasses import dataclass, field
from typing import List

count_tranche = itertools.count()
count_credit = itertools.count()
count_investor = itertools.count()


@dataclass
class Tranche:
    percent: int
    max_sum: int
    id: int = field(default_factory=lambda: next(count_tranche))
    current_amount: int = 0,
    _threshold_limit: int = 0

    @property
    def threshold_limit(self) -> int:
        return self.max_sum - self.current_amount

    def can_investment(self, amount) -> bool:
        return bool(amount <= self.threshold_limit)


@dataclass
class Credit:
    end_date: str
    id: int = field(default_factory=lambda: next(count_credit))
    start_date: str = str(datetime.utcnow().isoformat())
    tranches: List[Tranche] = field(default_factory=list)

    def is_open_credit(self) -> bool:
        return date.today() < datetime.strptime(
            self.end_date, '%Y-%m-%d').date()


@dataclass
class Investor:
    name: str
    id: int = field(default_factory=lambda: next(count_investor))
    account: int = 1000
    id_iter = itertools.count()

    def balance_check(self, amount) -> bool:
        return amount <= self.account


@dataclass
class Investment:
    tranche: Tranche
    investor: Investor
    sum: int
    date_invest: str = str(datetime.utcnow().isoformat())
