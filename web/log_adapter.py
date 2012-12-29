# encoding: utf-8

import os
import threading
import operator
from web import misc, app
from web.parser import log_parser


cache = {}

def cached(func):
    def wrapper(arg):
        if arg not in cache:
            cache[arg] = func(arg)
        return cache[arg]
    return wrapper


def get_buslogs_path():
    cwd = os.getcwd()
    if 'LogParserPrototype' not in cwd:
        # working outside `LogParserPrototype'
        buslogs_path_part = 'LogParserPrototype'
    else:
        if 'web' in cwd:
            # working inside `web'
            buslogs_path_part = '..'
        else:
            # working under `LogParserPrototype'
            buslogs_path_part = ''

    return os.path.join(buslogs_path_part, 'buslogs')



def list_logs(buslogs_dir=None):
    if not buslogs_dir:
        buslogs_dir = get_buslogs_path()

    root, _, files = list(os.walk(buslogs_dir))[0]
    file_names = filter(lambda name: name != '.gitignore', files)

    return sorted(zip(file_names,
                      map(lambda file_name: os.path.join(root, file_name),
                          file_names)),
                  key=lambda (v1, _): v1)



@cached
def get_single_log(full_path):
    return log_parser.get_log(full_path)



def get_multiple_logs():
    logs = []
    lock = threading.RLock()
    def _(l, path):
        log = get_single_log(path)
        with lock:
            l.append(log)

    buslogs_path = get_buslogs_path()
    app.logger.info(buslogs_path)

    # a bit ugly here, but we'll figure it out later
    for root, dir, files in os.walk(buslogs_path):
        if app.debug:
            files = files[:]
            files.remove('.gitignore')
        else:
            pass

        for paths in misc.take(files):
            threads = []
            for log_path in paths:
                thread = threading.Thread(target=lambda: _(logs, os.path.join(root, '', log_path)))
                app.logger.info('starting %s' % log_path)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

    return sorted(logs, key=lambda log: log.date)





get_counter = log_parser.get_counter


if __name__ == '__main__':
    print get_multiple_logs()


