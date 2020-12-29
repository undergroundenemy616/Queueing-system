def get_oldest_order_in_collection(collection):
    time_ins = []
    for i in range(len(collection)):
        time_ins.append(collection[i].get_time_got_buffered())
    return collection[time_ins.index(min(time_ins))]


def get_newest_order_in_collection(collection):
    time_ins = []
    for i in range(len(collection)):
        time_ins.append(collection[i].get_time_got_buffered())
    return collection[time_ins.index(max(time_ins))]
