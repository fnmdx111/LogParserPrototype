
from operator import attrgetter, methodcaller


get_name = attrgetter('name')

get_count = attrgetter('count')

get_request_count_per_t_slice_of = lambda req_flag: lambda time_slice: time_slice.requests[req_flag].request_count

get_request_count_of = lambda req_flag: methodcaller('request_count', req_flag)

get_date = attrgetter('date')

from_ = lambda iterable: lambda func: map(func, iterable)


def take(iterable, by=2):
    while iterable:
        if len(iterable) < by:
            yield iterable
        else:
            yield iterable[:by]
        iterable = iterable[by:]


