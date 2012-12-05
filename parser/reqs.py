from json import dumps
from log_parser import get_log

cache = {}

def cached(func):
    def wrapper(*args):
        if func not in cache:
            cache[func] = func(*args)
        return cache[func]
    return wrapper



@cached
def count_total_request_per_day(log):
    return dumps(map(lambda time_slice: time_slice.name,
                     log.time_slices),
                 map(lambda time_slice: time_slice.count,
                     log.time_slices))



log = get_log(r'e:\bus.log')
count_total_request_per_day(log)

