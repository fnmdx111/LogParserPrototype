from collections import Counter

class Requests(object):
    def __init__(self):
        self.request_count = 0

        self.requests = {}
        for i in range(24): # current resolution is hard-coded to 1 hour
            self.requests[i] = []


    def add_req(self, time_number, params):
        self.request_count += 1

        parsed = Requests.parse_params(params)
        self.requests[time_number].append(Requests.parse_params(params))

        self.handle(parsed)


    @staticmethod
    def parse_params(params):
        return dict(map(lambda s: s.split('/'),
                        params))


    def handle(self, parsed_params):
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


    def handle(self, parsed_params):
        self.line_numbers.update((parsed_params['lineNo'],))



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


    def handle(self, parsed_params):
        self.stop_names.update((parsed_params['stopName'],))



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
        self.name = '%02d:00 - %02d:00' % (self.hour_number, self.hour_number + 1)
        self.count = 0

        self.requests = dict(zip(req_flag,
                                 map(lambda req_class: req_class(),
                                     req_classes)))


    def add(self, time_number, (req_name, params)):
        self.count += 1
        self.requests[req_name].add_req(time_number, params) # e.g. ReqLine_Live.add_req(time_number, params)



class Log(object):
    def __init__(self, logger, day=None):
        self.day = day
        self.logger = logger

        self.time_slices = map(TimeSlice, range(24))


    @staticmethod
    def time_to_number(time):
        return int(time.split(':')[0])


    def add(self, time, request):
        # self.logger.info('processing', time, request)

        time_number = Log.time_to_number(time)
        self.time_slices[time_number].add(time_number, request)



