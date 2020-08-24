from menu import MainMenu


class BankCRM:
    menu = MainMenu()

    def run(self):
        while True:
            self.menu.display_menu()
            choice = input("Enter an option: ")
            item = self.menu.choices.get(choice)
            if item and item in (self.menu.credit_menu,
                                 self.menu.investor_menu):
                while True:
                    item.display_menu()
                    choice = input("Enter an option: ")
                    action = item.choices.get(choice)
                    if action == item.quit:
                        break
                    if action:
                        action()
                    else:
                        print("{0} is not a valid choice".format(choice))
                    continue
            elif item:
                item()
            else:
                print("{0} is not a valid choice".format(choice))


if __name__ == "__main__":
    BankCRM().run()
