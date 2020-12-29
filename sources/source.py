from order.order_generator import order_generator


class Source:
    def __init__(self, type_, generation_law, number, amount, delay):
        self.__type = type_
        self.__generation_law = generation_law
        self.__number = number
        self.__amount = amount
        self.__orders_amount = 0
        self.__orders = []
        self.__cur_time = 0
        self.__delay = delay
        self.__cooldown = 0.7
        self.__order_generator = order_generator(number, generation_law, self.__cooldown, delay)

    def generate_order(self):
        self.__orders.append(next(self.__order_generator))
        self.__orders_amount += 1
        self.__orders[self.__orders_amount - 1].set_number(self.__orders_amount - 1)
        return self.__orders[self.__orders_amount - 1]

    def set_type(self, type_):
        self.__type = type_

    def get_type(self):
        return self.__type

    def set_generation_law(self, generation_law):
        self.__generation_law = generation_law

    def get_generation_law(self):
        return self.__generation_law

    def set_number(self, number):
        self.__number = number

    def get_number(self):
        return self.__number

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_orders_amount(self, orders_amount):
        self.__orders_amount = orders_amount

    def get_orders_amount(self):
        return self.__orders_amount

    def set_orders(self, orders):
        self.__orders = orders

    def get_orders(self):
        return self.__orders

    def set_cur_time(self, cur_time):
        self.__cur_time = cur_time

    def get_cur_time(self):
        return self.__cur_time

    def set_delay(self, delay):
        self.__delay = delay

    def get_delay(self):
        return self.__delay

    def set_order_generator(self, order_gen):
        self.__order_generator = order_gen

    def get_order_generator(self):
        return self.__order_generator
