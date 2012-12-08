
from operator import attrgetter


from_t_slice_get_name = attrgetter('name')

from_t_slice_get_count = attrgetter('count')

from_t_slice_get_count_of = lambda req_flag: lambda time_slice: time_slice.requests[req_flag].request_count


def take(iterable, by=2):
    while iterable:
        if len(iterable) < by:
            yield iterable
        else:
            yield iterable[:by]
        iterable = iterable[by:]


