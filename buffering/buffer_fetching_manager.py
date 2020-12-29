from typing import Any
from sources.source_manager import SourceManager
from utils.get_order_from_collection import get_oldest_order_in_collection


class BufferFetchingManager:
    # Singleton
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(BufferFetchingManager, cls).__new__(cls)
        return cls.instance

    # when the order is returned, it is supposed to be removed from the buffer
    @staticmethod
    def get_order_from_buffer(buffer):
        return buffer.take_oder()


    # package number = source number
    @staticmethod
    def get_highest_prior_package_num(buffer):
        if not buffer.is_empty():
            priorities = []

            # get priorities of all the orders in a buffer
            orders = buffer.get_orders()
            for order in orders:
                if order is not None:
                    priorities.append(SourceManager.get_order_priority(order))

            return min(priorities)
        else:
            return -1

    @staticmethod
    def send_order_to_worker(order, worker):
        if worker is not None:
            order.set_time_out_of_buffer(worker.get_time_free())
            worker.process_order(order)
        else:
            raise RuntimeError("Logical error! Sending order to worker which is None!")
