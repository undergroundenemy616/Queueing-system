class TimeQueue:
    def __init__(self):
        self.arr = []

    def put(self, order):
        if not self.arr:
            self.arr.append(order)
        else:
            flag = False
            for i in range(len(self.arr)):
                if order.get_time_in() < self.arr[i].get_time_in():
                    self.arr.insert(i, order)
                    flag = True
                    break
            if flag is False:
                self.arr.append(order)

    def get(self):
        return self.arr.pop(0)

    def empty(self):
        if not self.arr:
            return True
        else:
            return False