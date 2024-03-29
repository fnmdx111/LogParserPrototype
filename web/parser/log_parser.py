# encoding: utf-8

from collections import defaultdict, Counter
from logging import Logger
from operator import methodcaller
import os
from web.parser.type import Log
import type as t


logger = Logger(__name__)

_ = lambda (time, request, params): (
    time.split(),
    request.strip('/'),
    tuple(params.strip('[]\n').split(']['))
)


def process_line(line):
    return _(line.split('|'))


def get_log(path):
    if 'gitignore' in path:
        return Log(logger)

    with open(path, 'r') as f:
        d = defaultdict(set)

        log = Log(date=path.split('.')[-1])

        line_no = 1
        for line in f:
            line = line.decode('utf-8')
            if line_no % 10000 == 0:
                print line_no
            line_no += 1

            try:
                (_, time), req, params = process_line(line)
                # collect_request(req, params)
                log.add(time, (req, params))

            except Exception:
                pass

        for key, value in sorted(d.iteritems(), key=lambda (k, _): k):
            print '%s: %s' % (key, ','.join(map(lambda t: '[' + ', '.join(t) + ']',
                                                value)))

        return log



def get_counter(log):
    startswith = lambda what: methodcaller('startswith', what)

    total_stop_names = Counter()

    for time_slice in log.time_slices:
        for req_name in filter(startswith('stop!'), t.req_flag):
            total_stop_names.update(time_slice.requests[req_name].stop_names)

    total_line_numbers = Counter()
    for time_slice in log.time_slices:
        for req_name in filter(startswith('line!'), t.req_flag):
            total_line_numbers.update(time_slice.requests[req_name].line_numbers)

    return total_stop_names, total_line_numbers



def write(path, counter):
    l = sorted(counter.iteritems(),
               key=lambda (_, v): v,
               reverse=True)
    with open(path, 'w') as f:
        print >>f, 'total keyword:', len(l)
        print >>f, 'total requests:', sum(counter.values())
        for pair in l:
            print >>f, '%s: %s' % pair
    print 'done'



if __name__ == '__main__':
    stop_names, line_numbers = Counter(), Counter()

    original_cwd = os.getcwd()
    os.chdir('parser\\buslogs')
    for root, dir, files in os.walk('.'):
        for log in files:
            total_stop_names, total_line_numbers = get_counter(get_log(log))
            stop_names.update(total_stop_names)
            line_numbers.update(total_line_numbers)
            print 'processed', log
    os.chdir(original_cwd)

    write('e:\\line_numbers.log', line_numbers)
    write('e:\\stop_names.log', stop_names)



