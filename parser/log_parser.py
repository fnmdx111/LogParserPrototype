from collections import defaultdict, Counter
from logging import Logger
from type import Log


logger = Logger(__name__)

_ = lambda (time, request, params): (
    time.split(),
    request.strip('/'),
    tuple(params.strip('[]\n').split(']['))
)


def process_line(line):
    return _(line.split('|'))


def get_log(path):
    with open(path, 'r') as f:
        d = defaultdict(set)

        log = Log(logger)

        line_no = 1
        for line in f:
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




if __name__ == '__main__':
    log = get_log(r'e:\bus.log')

    def write(path, counter):
        l = sorted(counter.iteritems(),
                   key=lambda (_, v): v,
                   reverse=True)
        with open(path, 'w') as f:
            print >>f, 'total:', len(l)
            for pair in l:
                print >>f, '%s: %s' % pair
        print 'done'


    total = Counter()
    for time_slice in log.time_slices:
        total.update(time_slice.requests['stop!stoplist'].stop_names)

    write(r'e:\stop_names.log', total)

    total.clear()
    for time_slice in log.time_slices:
        total.update(time_slice.requests['line!live2'].line_numbers)
        total.update(time_slice.requests['line!map2'].line_numbers)

    write(r'e:\line_numbers.log', total)




