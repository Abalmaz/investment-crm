import sys
from datetime import datetime

from models import Credit, Investor, Investment
from utils import calculate_profit, number_of_days_in_month


class BaseMenu:

    def display_menu(self):
        pass

    def quit(self):
        pass


class MenuCredit(BaseMenu):
    def __init__(self):
        self.credits = []
        self.choices = {
            "1": self.add_credit,
            "2": self.add_tranche_for_credit,
            "3": self.show_all_credits,
            "4": self.show_all_tranches,
            "5": self.show_credit_detail,
            "9": self.quit
        }

    def display_menu(self):
        print("""       
                Credit Menu  

                1. Create credit
                2. Add tranche for credit
                3. Show all credits
                4. Show all tranches
                5. Show credit details
                9. Return

                """)

    def add_credit(self):
        print("-" * 30)
        start_date = input("Enter start date:  ")
        end_date = input("Enter end date:   ")
        print("-" * 30)
        self.credits.append(Credit(start_date, end_date))
        print("Credit was successfully created.")

    def add_tranche_for_credit(self):
        print("-" * 30)
        print("Existing credits:")
        for credit in self.credits:
            print(f"ID: {credit.id}, "
                  f"start date: {credit.start_date}, "
                  f"end date: {credit.end_date}")
        print("-" * 30)
        credit_id = int(input("Enter Credit ID: "))
        percent = int(input("Percent: "))
        max_sum = int(input("Limit: "))
        print("-" * 30)
        credit = self.credits[credit_id]
        credit.create_tranche(percent, max_sum)
        print("Tranche was successfully created")

    def show_all_credits(self):
        print("-" * 30)
        for credit in self.credits:
            print(credit)
        print("-" * 30)

    def show_all_tranches(self):
        print("-" * 30)
        for credit in self.credits:
            for tranche in credit.tranches:
                print(f"ID: {tranche.id}, "
                      f"max sum: {tranche.max_sum}, "
                      f"percent: {tranche.percent}, "
                      f"current amount: {tranche.current_amount}, "
                      f"threshold limit: {tranche.threshold_limit}")
        print("-" * 30)

    def show_credit_detail(self):
        credit_id = int(input("Enter ID: "))
        credit = self.credits[credit_id]
        print("-" * 30)
        print(f"Credit ID: {credit.id}")
        print(f"Start date: {credit.start_date}")
        print(f"End date: {credit.end_date}")
        print(f"Credit's tranches: ")
        for tranche in credit.tranches:
            print(f"Tranche percent: {tranche.percent}, "
                  f"limit: {tranche.max_sum}, "
                  f"threshold limit: {tranche.threshold_limit} ")
        print("-" * 30)


class MenuInvestor(BaseMenu):
    def __init__(self):
        self.investors = []
        self.choices = {
            "1": self.add_investor,
            "2": self.show_all_investors,
            "3": self.show_investor_detail,
            "9": self.quit
        }

    def display_menu(self):
        print("""       
                Investor Menu  

                1. Create new investor
                2. Show all investors
                3. Show investor details
                9. Return

                """)

    def add_investor(self):
        print("-" * 30)
        name = input("Enter name:  ")
        print("-" * 30)
        self.investors.append(Investor(name))
        print(f"Investor {name} was successfully created")

    def show_all_investors(self):
        print("-" * 30)
        for investor in self.investors:
            print(investor)

    def show_investor_detail(self):
        investor_id = int(input("Enter ID: "))
        print("-" * 30)
        investor = self.investors[investor_id]
        print(f"ID: {investor.id}, "
              f"name: {investor.name}, "
              f"account: {investor.account}")
        print("-" * 30)


class MainMenu(BaseMenu):
    def __init__(self):
        self.credit_menu = MenuCredit()
        self.investor_menu = MenuInvestor()
        self.investments = []
        self.choices = {
            "1": self.credit_menu,
            "2": self.investor_menu,
            "3": self.create_investment,
            "4": self.calculated_profit,
            "9": self.quit
        }

    def display_menu(self):
        print("""       
                Bank_CRM Menu  

                1. Credit
                2. Investor
                3. Create investment
                4. Calculate profit by date
                9. Quit

                """)

    def add_investment(self, tranche, investor,
                       sum_invest, date_invest):
        self.investments.append(
            Investment(tranche, investor, sum_invest, date_invest)
        )

    def create_investment(self):
        print("-" * 30)
        print("Existing tranches:")
        for credit in self.credit_menu.credits:
            for tr in credit.tranches:
                print(f"ID: {tr.id}, "
                      f"percent: {tr.percent}, "
                      f"threshold limit: {tr.threshold_limit}")
        print("-" * 30)
        tranche = None
        tranche_id = int(input("Tranche id: "))
        for credit in self.credit_menu.credits:
            for tr in credit.tranches:
                if tr.id == tranche_id:
                    tranche = tr
        print("-" * 30)
        print("Existing investors:")
        for investor in self.investor_menu.investors:
            print(f"ID: {investor.id}, "
                  f"name: {investor.name}, "
                  f"account: {investor.account}")
        print("-" * 30)
        investor_id = int(input("Investor id: "))
        investor = self.investor_menu.investors[investor_id]
        amount = int(input("Amount of investment: "))
        date_invest = input("Date of investment: ")

        if tranche.credit.is_open_credit():
            if tranche.can_investment(amount):
                if investor.account >= amount:
                    self.add_investment(tranche, investor,
                                        amount, date_invest)
                    investor.account -= amount
                    tranche.current_amount += amount
                    print("Tranche was successfully created")
                else:
                    print("Investor didn't have enough money")
            else:
                print("The invest threshold limit is reached")
        else:
            print("Credit is close")

    def calculated_profit(self):
        settlement_date = input("Settlement date: ")
        calculate_date = datetime.strptime(settlement_date, '%Y-%m-%d').date()
        days_in_month = number_of_days_in_month(calculate_date.year,
                                                calculate_date.month)

        for investment in self.investments:
            count_days = calculate_date - investment.date_invest
            profit = calculate_profit(investment.sum,
                                      investment.tranche.percent,
                                      days_in_month,
                                      count_days.days)
            print(f"Investor: {investment.investor.name}, Profit: {profit:.2f}")

    def quit(self):
        print("Thank you for using Bank_CRM")
        sys.exit(0)
