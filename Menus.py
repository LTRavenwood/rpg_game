def blocking_input(acceptable_responses: [str]) -> str:
    """calls input('>') until an appropriate input is selected
    :param acceptable_responses: the inputs that will get a go-ahead"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


class HeadMenu:
    def __init__(self, data, next_menu, previous):
        self.data = data
        self.next_menu = next_menu
        self.previous = previous

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_menu

    def set_next(self, new_next):
        self.next_menu = new_next

    def get_previous(self):
        return self.previous

    def set_previous(self, new_previous):
        self.previous = new_previous


class Menus(HeadMenu):
    def __init__(self, data, next_menu, previous):
        super().__init__(data, next_menu, previous)

    def get_input(self, next_menu, last_menu):
        output = input('>')
        while True:
            if output == self.next_menu:
                return next_menu
            if output == self.previous:
                return last_menu
            return output


start_menu = Menus('Start Menu', 'e', None)
main_menu = Menus('Main Menu', None, 's')

start_menu.get_data()


