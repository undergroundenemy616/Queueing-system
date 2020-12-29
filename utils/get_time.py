import random
import math
from utils.parse_config import parse_config


def get_time_working(service_law):
    if service_law == "exp":
        exp_arg_range = float(parse_config("Worker", "exp_arg_range"))
        return math.exp(random.random()*exp_arg_range)
    else:
        raise ValueError("I can generate time only exponentially!")


def time_next_order(generation_law, cooldown, delay=0):
    if generation_law == "poison":
        delay = -1.0 / cooldown * math.log(random.random())
        print("delay is", delay)
        cur_time = delay
        while True:
            yield cur_time
            cur_time += -1.0 / cooldown * math.log(random.random())


def get_delay(rangee):
    return random.random()*rangee + 1

