class Statistics:

    # ==============================
    # AUTO MODE
    # ==============================

    # ==============================
    # PRINT METHODS
    # ==============================

    @staticmethod
    def print_num_of_orders(sources):
        print("========== Numbers of orders")
        for source in sources:
            print("Source", source.get_number(), ": ", source.get_orders_amount())
        print("==========")

    @staticmethod
    def print_num_rejected_orders(sources):
        print("========== Numbers of rejected orders")
        for source in sources:
            print("Source", source.get_number(), ": ", Statistics.get_num_of_rejected_orders(source))
        print("==========")

    @staticmethod
    def print_reject_probability(sources):
        print("========== Reject probability")
        count = 0
        time = 0
        for source in sources:
            count += 1
            orders_amount = source.get_orders_amount()
            if orders_amount > 0:
                final = Statistics.get_num_of_rejected_orders(source) / orders_amount
                time += final
                print("Source", source.get_number(), ": ",
                      final)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were generated")
        print('Average reject: ', time / count)
        print("==========")

    @staticmethod
    def print_average_time_spent_in_system(sources):
        print("========== Average time spent in system")
        for source in sources:
            value = Statistics.get_average_time_spent_in_system(source)
            if value != -1:
                print("Source", source.get_number(), ": ", value)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were generated")
        print("==========")

    @staticmethod
    def print_average_time_spent_in_wait(sources):
        print("========== Average time spent in wait")
        for source in sources:
            value = Statistics.get_average_time_spent_in_wait(source)
            if value != -1:
                print("Source", source.get_number(), ": ", value)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were buffered")
        print("==========")

    @staticmethod
    def print_dispersion_time_in_wait(sources):
        print("========== Dispersion of time spent in wait")
        for source in sources:
            avg_time = Statistics.get_average_time_spent_in_wait(source)
            if avg_time != -1:
                dispersion = Statistics.get_dispersion_time_in_wait(source, avg_time)
                if dispersion != -1:
                    print("Source", source.get_number(), ": ", dispersion)
                else:
                    print("Source", source.get_number(), ": only 1 order from this source was buffered")
            else:
                print("Source", source.get_number(), ": 0 orders from this source were buffered")
        print("==========")

    @staticmethod
    def print_average_time_spent_in_service(sources):
        print("========== Average time spent in service")
        for source in sources:
            value = Statistics.get_average_time_spent_in_service(source)
            if value != -1:
                print("Source", source.get_number(), ": ", value)
            else:
                print("Source", source.get_number(), ": 0 orders from this source were served")
        print("==========")

    @staticmethod
    def print_dispersion_time_in_service(sources):
        print("========== Dispersion of time spent in service")
        for source in sources:
            avg_time = Statistics.get_average_time_spent_in_service(source)
            if avg_time != -1:
                dispersion = Statistics.get_dispersion_time_in_service(source, avg_time)
                if dispersion != -1:
                    print("Source", source.get_number(), ": ", dispersion)
                else:
                    print("Source", source.get_number(), ": only 1 order from this source was served")
            else:
                print("Source", source.get_number(), ": 0 orders from this source were served")
        print("==========")

    @staticmethod
    def print_worker_use_coef(workers, impl_time):
        if impl_time > 0:
            print("========== Workers use coefficient")
            for worker in workers:
                print("Worker", worker.get_number(), ": ", Statistics.get_worker_use_coef(worker, impl_time))
            print("==========")
        else:
            raise ValueError("Implementation time <= 0!")

    @staticmethod
    def print_orders_left_buffer(buffer):
        print("========== Iterations stopped. Orders left in buffer:")
        num_orders_left_buffer = buffer.get_orders_amount_now()
        orders = [elem for elem in buffer.get_orders() if elem is not None]
        print(orders)
        for i in range(num_orders_left_buffer):
            print("Buffer[", i, "] ", "order's source num: ", orders[i].get_source_number(),
                  "; time in: ", orders[i].get_time_in(),
                  "; time buffered: ", orders[i].get_time_got_buffered())
        print("Empty slots in buffer: ", buffer.get_volume() - num_orders_left_buffer)
        print("Number of orders in buffer now: ", num_orders_left_buffer)
        print("All of the orders left in buffer get rejected")
        print("==========")

    # ==============================
    # GET METHODS
    # ==============================

    @staticmethod
    def get_num_of_rejected_orders(source):
        count = 0
        for order in source.get_orders():
            time_out = order.get_time_out()
            if time_out is not None:
                if order.get_time_in() == time_out or time_out == order.get_time_out_of_buffer():
                    count += 1
        return count

    @staticmethod
    def get_average_time_spent_in_system(source):
        sum_ = 0
        count_orders = source.get_orders_amount()
        for order in source.get_orders():
            sum_ += order.get_time_out() - order.get_time_in()
        return sum_ / count_orders if count_orders > 0 else -1

    @staticmethod
    def get_average_time_spent_in_wait(source):
        sum_ = 0
        count_orders_buffered = 0
        for order in source.get_orders():
            time_out_of_buffer = order.get_time_out_of_buffer()
            if time_out_of_buffer is not None:
                sum_ += time_out_of_buffer - order.get_time_got_buffered()
                count_orders_buffered += 1
        return sum_ / count_orders_buffered if count_orders_buffered > 0 else -1

    @staticmethod
    def get_dispersion_time_in_wait(source, avg_time):
        sum_ = 0
        count_orders_buffered = 0
        for order in source.get_orders():
            time_out_of_buffer = order.get_time_out_of_buffer()
            if time_out_of_buffer is not None:
                time_in_wait = time_out_of_buffer - order.get_time_got_buffered()
                sum_ += (time_in_wait - avg_time) ** 2
                count_orders_buffered += 1
        return sum_ / (count_orders_buffered - 1) if count_orders_buffered > 1 else -1

    @staticmethod
    def get_average_time_spent_in_service(source):
        sum_ = 0
        count_orders_served = 0
        for order in source.get_orders():
            time_finish = order.get_time_service_finished()
            time_start = order.get_time_service_started()
            if time_finish is not None and time_start is not None:
                sum_ += time_finish - time_start
                count_orders_served += 1
        return sum_ / count_orders_served if count_orders_served > 0 else -1

    @staticmethod
    def get_dispersion_time_in_service(source, avg_time):
        sum_ = 0
        count_orders_served = 0
        for order in source.get_orders():
            time_finish = order.get_time_service_finished()
            time_start = order.get_time_service_started()
            if time_finish is not None and time_start is not None:
                time_in_service = time_finish - time_start
                sum_ += (time_in_service - avg_time) ** 2
                count_orders_served += 1
        return sum_ / (count_orders_served - 1) if count_orders_served > 1 else -1

    @staticmethod
    def get_worker_use_coef(worker, impl_time):
        time_working = worker.get_time_working()
        return time_working / impl_time

    # ==============================
    # STEP MODE
    # ==============================

    # ==============================
    # PRINT METHODS
    # ==============================

    @staticmethod
    def print_cur_sources_state(sources):
        print("========== Sources")
        print("№  ", "Time generated  ", "Orders number  ", "Rejected orders number")
        for source in sources:
            orders = source.get_orders()
            print(
                source.get_number(), "  ", "%.4f" % orders[-1].get_time_in(), "          ",
                source.get_orders_amount(), "             ", Statistics.get_num_of_rejected_orders(source)
            )
        print("==========")

    @staticmethod
    def print_cur_buffer_state(buffer):
        print("========== Buffer")
        print("№  ", "Time generated  ", "Source №  ", "Order №")
        volume = buffer.get_volume()
        orders = buffer.get_orders()
        for i in range(volume):
            if orders[i] is not None:
                print(
                    i, "  ", "%.4f" % orders[i].get_time_in(), "          ",
                    orders[i].get_source_number(), "        ", orders[i].get_number()
                )
            else:
                print(i)
        print("==========")

    @staticmethod
    def print_cur_workers_state(workers, cur_time):
        print("========== Workers")
        print("№  ", "Time free  ", "Time Working  ", "Source №  ", "Order №  ", "Time generated")
        workers_num = len(workers)
        for i in range(workers_num):
            time_idle = cur_time - workers[i].get_time_working()
            if time_idle < 0:
                time_idle = 0

            cur_order = workers[i].get_cur_order()
            # 1)cur_order = None, 2)cur_order.srv_fnshd() < cur_time, 3)>

            if cur_order is None or cur_order.get_time_service_finished() < cur_time:
                print(
                    i, "  ", "%.4f" % workers[i].get_time_free(), "    ",
                             "%.4f" % workers[i].get_time_working()
                )
            else:
                print(
                    i, "  ", "%.4f" % workers[i].get_time_free(), "    ",
                             "%.4f" % workers[i].get_time_working(), "     ", cur_order.get_source_number(),
                    "        ", cur_order.get_number(), "      ", "%.4f" % cur_order.get_time_in()
                )
        print("==========")

    # ==============================
    # PRINT EVERYTHING METHODS (both auto and step modes)
    # ==============================

    @staticmethod
    def print_everything_step(sources, buffer, workers, cur_time):
        print("=====================================================================")
        Statistics.print_cur_sources_state(sources)
        Statistics.print_cur_buffer_state(buffer)
        Statistics.print_cur_workers_state(workers, cur_time)
        input("Enter - next step...\n")

    @staticmethod
    def print_everything_auto(sources, workers, time_impl_end):
        #Statistics.print_num_of_orders(sources)
        Statistics.print_num_rejected_orders(sources)
        #Statistics.print_reject_probability(sources)
        #Statistics.print_average_time_spent_in_system(sources)
        #Statistics.print_average_time_spent_in_wait(sources)
        Statistics.print_dispersion_time_in_wait(sources)
        #Statistics.print_average_time_spent_in_service(sources)
        Statistics.print_dispersion_time_in_service(sources)
        #Statistics.print_worker_use_coef(workers, time_impl_end)
