from typing import Any
from sources.source_manager import SourceManager


class BufferPlacementManager:
    # Singleton
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(BufferPlacementManager, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def find_place_in_buffer(buffer):
        if not buffer.is_full():
            return buffer.get_orders_amount_now()
        else:
            return None

    @staticmethod
    def find_order_to_reject(buffer, new_order):
        if buffer.is_full():
            priorities = []

            # get priorities of all the orders in a buffer and the new_order
            orders = buffer.get_orders()
            for order in orders:
                priorities.append(SourceManager.get_order_priority(order))
            least_priority_val = max(priorities)

            # check if the new_order has the least priority order
            # if yes, the method returns None and no order from the buffer gets rejected
            new_order_prior = SourceManager.get_order_priority(new_order)
            if new_order_prior >= least_priority_val:
                return None

            # if we have the only one least priority order - return the position of it
            number_of_least_prior_orders = priorities.count(least_priority_val)
            if number_of_least_prior_orders == 1:
                return priorities.index(least_priority_val)

            # if we have more, we look at the times the orders got into buffer
            least_priority_positions = [priorities.index(least_priority_val)]
            for i in range(1, number_of_least_prior_orders):
                least_priority_positions.append(priorities.index(least_priority_val,
                                                                 least_priority_positions[i-1]))

            # now we have to decide which order has the newest time_got_buffered
            time_ins = []
            for i in range(number_of_least_prior_orders):
                time_ins.append(orders[least_priority_positions[i]].get_time_got_buffered())

            return least_priority_positions[time_ins.index(max(time_ins))]
        else:
            raise AttributeError("Buffer is not full! Do not use rejection when buffer is not full!")
