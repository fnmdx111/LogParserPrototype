from collections import Counter

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
        requests = Requests()
        requests.request_count = self.request_count + other.request_count
        for i in range(24):
            requests.requests[i] = self.requests[i][:]
            requests.requests[i].extend(other.requests[i])
        return requests


    @staticmethod
    def parse_params(params):
        return dict(map(lambda s: s.split('/'),
                        params))


    def handle(self, params):
        pass



class ReqLine_Live(Requests):
    def __init__(self):
        super(ReqLine_Live, self).__init__()



class ReqLine_Live2(Requests):
    def __init__(self):
        super(ReqLine_Live2, self).__init__()

        self.line_numbers = Counter()


    def handle(self, parsed_params):
        self.line_numbers.update((parsed_params['lineNo'],))



class ReqLine_Map(Requests):
    def __init__(self):
        super(ReqLine_Map, self).__init__()



class ReqLine_Map2(Requests):
    def __init__(self):
        super(ReqLine_Map2, self).__init__()

        self.line_numbers = Counter()


    def handle(self, params):
        self.line_numbers.update((Requests.parse_params(params)['lineNo'],))



class ReqLine_Query(Requests):
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



class ReqStop_Lines(Requests):
    def __init__(self):
        super(ReqStop_Lines, self).__init__()



class ReqStop_List4Name(Requests):
    def __init__(self):
        super(ReqStop_List4Name, self).__init__()



class ReqStop_Nearby(Requests):
    def __init__(self):
        super(ReqStop_Nearby, self).__init__()



class ReqStop_StopList(Requests):
    def __init__(self):
        super(ReqStop_StopList, self).__init__()

        self.stop_names = Counter()


    def handle(self, params):
        self.stop_names.update((Requests.parse_params(params)['stopName'],))



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
    def __init__(self, logger=None, day=None):
        self.day = day
        self.logger = logger

        self.time_slices = map(TimeSlice, range(24))


    @staticmethod
    def time_to_number(time):
        return int(time.split(':')[0])


    def add(self, time, request):
        time_number = Log.time_to_number(time)
        self.time_slices[time_number].add(time_number, request)


    def __add__(self, other):
        if not isinstance(other, Log):
            raise ValueError, 'incompatible operand type'

        log = Log()
        for i in range(24):
            log.time_slices[i] = self.time_slices[i] + other.time_slices[i]

        return log




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

