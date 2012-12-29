
from operator import attrgetter, methodcaller
import operator


get_name = attrgetter('name')

get_count = attrgetter('count')

get_request_count_per_t_slice_of = lambda req_flag: lambda time_slice: time_slice.requests[req_flag].request_count

get_request_count_of = lambda req_flag: methodcaller('request_count', req_flag)

get_date = attrgetter('date')

from_ = lambda iterable: lambda func: map(func, iterable)



MAX_PARSER_THREADS = 1


def take(iterable, by=MAX_PARSER_THREADS):
    while iterable:
        if len(iterable) < by:
            yield iterable
        else:
            yield iterable[:by]
        iterable = iterable[by:]


def get_overview(d):
    """d can be regarded as a matrix actually"""
    return reduce(lambda acc, item: map(operator.add,
                                        acc, item),
                  d.values(),
                  [0] * len(d[d.keys()[0]]))




