import itertools
from datetime import date, datetime
from dataclasses import dataclass


@dataclass
class Tranche:
    id: int
    percent: int
    max_sum: int
    current_amount: int = 0,
    _threshold_limit: int = 0

    def __post_init__(self):
        self.id += 1

    @property
    def threshold_limit(self) -> int:
        return self.max_sum - self.current_amount

    def can_investment(self, amount) -> bool:
        return bool(amount <= self.threshold_limit)


@dataclass
class Credit:
    tranches: Tranche
    end_date: str
    id: int = 0
    start_date: str = str(datetime.utcnow().isoformat())

    def __post_init__(self):
        self.id += 1

    def is_open_credit(self) -> bool:
        return date.today() < datetime.strptime(
            self.end_date, '%Y-%m-%d').date()


@dataclass
class Investor:
    id: int
    name: str
    account: int = 1000
    id_iter = itertools.count()

    def __post_init__(self):
        self.id += 1

    def balance_check(self, amount) -> bool:
        return amount <= self.account


@dataclass
class Investment:
    tranche: Tranche
    investor: Investor
    sum: int
    date_invest: str = str(datetime.utcnow().isoformat())
