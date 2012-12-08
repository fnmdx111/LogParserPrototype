import os
import threading
import operator
from web import misc
from web.parser import log_parser
from web.parser.type import Log


cache = {}

def cached(func):
    def wrapper(*args):
        if func not in cache:
            cache[func] = func(*args)
        return cache[func]
    return wrapper


@cached
def get_multiple_log():
    logs = []
    lock = threading.RLock()
    def _(l, path):
        log = log_parser.get_log(path)
        with lock:
            l.append(log)

    buslogs_path = os.path.join('' if 'web' not in os.getcwd() else '..', 'buslogs')
    print buslogs_path
    # a bit ugly here, but we'll figure it out later
    for root, dir, files in os.walk(buslogs_path):
        files = files[:]
        files.remove('.gitignore')
        for paths in misc.take(files, by=3):
            threads = []
            for log_path in paths:
                thread = threading.Thread(target=lambda: _(logs, os.path.join(root, '', log_path)))
                print 'starting', log_path
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

    return reduce(operator.add, logs, Log())



@cached
def get_current_log():
    log = []
    def _(l):
        l.append(log_parser.get_log(r'e:\bus.log'))
        return l

    thread = threading.Thread(target=lambda: _(log))
    thread.start()
    thread.join()

    return log[0]



if __name__ == '__main__':
    print get_multiple_log()


