from collections import defaultdict
from logging import Logger
from type import Log


logger = Logger(__name__)

def process_line(line):
    whole = (date, time), request, params = (
        lambda (time, request, params): (
                time.split(),
                request.strip('/'),
                tuple(params.strip('[]\n').split(']['))
            )
        )(line.split('|'))

    return whole


def main():
    with open('e:\\bus.log') as f:
        d = defaultdict(set)

        def collect_request(request, params):
            d[request].add(tuple(map(lambda param: param.split('/')[0],
                                     params)))

        log = Log(logger)

        line_no = 1
        for line in f:
            print line_no,
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



