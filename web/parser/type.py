# encoding: utf-8

from collections import Counter, defaultdict
from flask import jsonify
from web.misc import get_request_count_per_t_slice_of, from_, get_name, get_count

class Requests(object):
    def __init__(self):
        self.request_count = 0

        self.requests = {}
        for i in range(24): # current resolution is hard-coded to 1 hour
            self.requests[i] = []


    def add_req(self, time_number, params):
        self.request_count += 1

        # self.requests[time_number].append(Requests.parse_params(params))

        self.handle(params)


    def __add__(self, other):
        requests = self.__class__()
        requests.request_count = self.request_count + other.request_count
#        for i in range(24):
#            requests.requests[i] = self.requests[i][:]
#            requests.requests[i].extend(other.requests[i])
        return requests


    @staticmethod
    def parse_params(params):
        return dict(map(lambda s: s.split('/'),
                        params))


    def handle(self, params):
        pass



class ReqLine(Requests):
    def __init__(self):
        super(ReqLine, self).__init__()

        self.line_numbers = Counter()


    def handle(self, params):
        self.line_numbers.update((Requests.parse_params(params)['lineNo'],))


    def __add__(self, other):
        request = super(ReqLine, self).__add__(other)
        request.line_numbers = Counter()
        request.line_numbers.update(self.line_numbers)
        request.line_numbers.update(other.line_numbers)

        return request



class ReqLine_Live(ReqLine):
    def __init__(self):
        super(ReqLine_Live, self).__init__()



class ReqLine_Live2(ReqLine):
    def __init__(self):
        super(ReqLine_Live2, self).__init__()



class ReqLine_Map(ReqLine):
    def __init__(self):
        super(ReqLine_Map, self).__init__()



class ReqLine_Map2(ReqLine):
    def __init__(self):
        super(ReqLine_Map2, self).__init__()



class ReqLine_Query(ReqLine):
    def __init__(self):
        super(ReqLine_Query, self).__init__()



class ReqNews_Detail(Requests):
    def __init__(self):
        super(ReqNews_Detail, self).__init__()



class ReqNews_List(Requests):
    def __init__(self):
        super(ReqNews_List, self).__init__()



class ReqParam_PGet(Requests):
    def __init__(self):
        super(ReqParam_PGet, self).__init__()



class ReqStop(Requests):
    def __init__(self):
        super(ReqStop, self).__init__()

        self.stop_names = Counter()


    def handle(self, params):
        self.stop_names.update((Requests.parse_params(params)['stopName'],))


    def __add__(self, other):
        request = super(ReqStop, self).__add__(other)
        request.stop_names = Counter()
        request.stop_names.update(self.stop_names)
        request.stop_names.update(other.stop_names)

        return request



class ReqStop_Lines(ReqStop):
    def __init__(self):
        super(ReqStop_Lines, self).__init__()



class ReqStop_List4Name(ReqStop):
    def __init__(self):
        super(ReqStop_List4Name, self).__init__()



class ReqStop_Nearby(ReqStop):
    def __init__(self):
        super(ReqStop_Nearby, self).__init__()



class ReqStop_StopList(ReqStop):
    def __init__(self):
        super(ReqStop_StopList, self).__init__()



class ReqStop2Stop_Lines4Less(Requests):
    def __init__(self):
        super(ReqStop2Stop_Lines4Less, self).__init__()



class ReqStop2Stop_Name2Id(Requests):
    def __init__(self):
        super(ReqStop2Stop_Name2Id, self).__init__()



class ReqClient(Requests):
    def __init__(self):
        super(ReqClient, self).__init__()



req_classes = [
    ReqClient,
    ReqLine_Live, ReqLine_Live2,
    ReqLine_Map, ReqLine_Map2, ReqLine_Query,
    ReqNews_Detail, ReqNews_List,
    ReqParam_PGet,
    ReqStop_Lines, ReqStop_List4Name, ReqStop_Nearby, ReqStop_StopList,
    ReqStop2Stop_Lines4Less, ReqStop2Stop_Name2Id
]
req_flag = [
    'client',
    'line!live', 'line!live2',
    'line!map', 'line!map2', 'line!query',
    'news!detail', 'news!list',
    'param!pget',
    'stop!lines', 'stop!list4name', 'stop!nearby', 'stop!stoplist',
    'stop2stop!lines4less', 'stop2stop!name2id'
]
req_main_flag = [
    'line', 'news', 'param', 'stop', 'stop2stop'
]

class TimeSlice(object):
    def __init__(self, number):
        self.hour_number = number
        self.name = '%02d-%02d' % (self.hour_number, self.hour_number + 1)
        self.count = 0

        self.requests = dict(zip(req_flag,
                                 map(lambda req_class: req_class(),
                                     req_classes)))


    def add(self, time_number, (req_name, params)):
        self.count += 1
        self.requests[req_name].add_req(time_number, params) # e.g. ReqLine_Live.add_req(time_number, params)


    def __add__(self, other):
        if not isinstance(other, TimeSlice):
            raise ValueError, 'incompatible operand type'

        time_slice = TimeSlice(self.hour_number)
        time_slice.count = self.count + other.count
        for req_name in self.requests:
            time_slice.requests[req_name] = self.requests[req_name] + other.requests[req_name]
        return time_slice




class Log(object):
    def __init__(self, date=None, logger=None, day=None):
        self.day = day
        self.logger = logger

        self.time_slices = map(TimeSlice, range(24))
        self.date = date

        self.count = 0


    @staticmethod
    def time_to_number(time):
        return int(time.split(':')[0])


    def add(self, time, request):
        self.count += 1

        time_number = Log.time_to_number(time)
        self.time_slices[time_number].add(time_number, request)


    def __add__(self, other):
        if not isinstance(other, Log):
            raise ValueError, 'incompatible operand type'

        log = Log()

        log.count = self.count + other.count

        for i in range(24):
            log.time_slices[i] = self.time_slices[i] + other.time_slices[i]

        return log


    def request_count(self, req_flag):
        return sum(map(get_request_count_per_t_slice_of(req_flag),
                       self.time_slices))


    def jsonify(self):
        from_log = from_(self.time_slices)

        d = map(lambda (k, v): (k.split('!'), v),
                {r_flag: from_log(get_request_count_per_t_slice_of(r_flag))
                 for r_flag in req_flag[1:]}.iteritems())
        d_prime = defaultdict(dict)
        for (main, sub), v in d:
            d_prime[main][sub] = v
        for main in d_prime:
            stub = {sub: sum(d_prime[main][sub])
                    for sub in d_prime[main]}
            d_prime[main]['overview'] = [stub.keys(), map(lambda i: [i], stub.values())]

        d_prime.update({
            'time_slice_names': from_log(get_name),
            'client': from_log(get_request_count_per_t_slice_of('client'))
        })

        req_names = ['line', 'news', 'param', 'stop', 'stop2stop']
        d_prime.update({
            'total': {
                'perhour': from_log(get_count),
                'overview': [['client'] + req_names,
                             map(lambda i: [i],
                                 [sum(d_prime['client'])] +
                                  map(lambda name: sum(map(lambda (i,): i,
                                                           d_prime[name]['overview'][1])),
                                      req_names))]
            }
        })

        print d_prime

        return jsonify(d_prime)





if __name__ == '__main__':
    req1 = Requests()
    req1.add_req(1, ['a/b'])
    req2 = Requests()
    req2.add_req(1, ['b/c'])
    req2.add_req(2, ['b/c'])
    print (req1 + req2).requests, (req1 + req2).request_count
    ts1 = TimeSlice(0)
    ts2 = TimeSlice(0)
    ts1.add(0, ('line!live', ['a/b', 'b/c']))
    ts2.add(0, ('line!live', ['c/d', 'd/e']))
    ts2.add(0, ('line!live', ['e/f', 'f/g']))
    ts3 = ts1 + ts2
    for req_name in ts3.requests:
        print req_name, ts3.requests[req_name].requests

