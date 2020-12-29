from utils.get_time import get_time_working


class Worker:
    def __init__(self, service_law, number, amount, manager, busy=False, time_working=0):
        self.__service_law = service_law
        self.__number = number
        self.__amount = amount
        self.__manager = manager
        self.__cur_order = None
        self.__busy = busy
        self.__time_working = time_working
        self.__time_free = 0

    def process_order(self, order):
        self.set_busy(True)
        self.__cur_order = order
        order.set_time_service_started(self.__time_free)
        time = get_time_working(self.__service_law)
        self.__time_working += time
        self.__time_free += time
        order.set_time_service_finished(self.__time_free)
        order.set_time_out(self.__time_free)

    def notify_free(self):
        self.set_busy(False)
        self.__manager.update_free_workers(self.__number, True)

    def set_service_law(self, service_law):
        self.__service_law = service_law

    def get_service_law(self):
        return self.__service_law

    def set_number(self, number):
        self.__number = number

    def set_cur_order(self, cur_order):
        self.__cur_order = cur_order

    def get_cur_order(self):
        return self.__cur_order

    def get_number(self):
        return self.__number

    def set_amount(self, amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_manager(self, manager):
        self.__manager = manager

    def get_manager(self):
        return self.__manager

    def set_busy(self, busy):
        self.__busy = busy

    def is_busy(self):
        return self.__busy

    def set_time_working(self, time_working):
        self.__time_working = time_working

    def get_time_working(self):
        return self.__time_working

    def set_time_free(self, time_free):
        self.__time_free = time_free

    def get_time_free(self):
        return self.__time_free
