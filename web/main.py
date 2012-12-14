# encoding: utf-8

from collections import defaultdict
from flask import render_template, request, jsonify
import operator
from web.parser import type
from web import app, log_adapter
from web.misc import get_count, get_request_count_of, from_, get_date
from web.parser.type import Log

sum_log = lambda logs: reduce(operator.add, logs, Log())



@app.route('/')
def home():
    return render_template('home.html',
                           options=log_adapter.list_logs())



@app.route('/top')
def top():
    return render_template('top.html', options=log_adapter.list_logs())



@app.route('/get_top_data', methods=['POST'])
def get_top_data():
    full_path = request.form.get('full_path', '', type=unicode)
    if full_path == 'all':
        stop_names_counter, line_numbers_counter = log_adapter.get_counter(sum_log(log_adapter.get_multiple_logs()))
    else:
        stop_names_counter, line_numbers_counter = log_adapter.get_counter(log_adapter.get_single_log(full_path))

    return jsonify(top_stop_names=stop_names_counter.most_common(100),
                   top_line_numbers=line_numbers_counter.most_common(100))



@app.route('/weekly')
def weekly():
    return render_template('weekly.html')


@app.route('/get_single_data', methods=['POST'])
def get_single_data():
    full_path = request.form.get('full_path', '', type=unicode)
    log = log_adapter.get_single_log(full_path)

    return log.jsonify()



@app.route('/get_total_data', methods=['POST'])
def get_total_data():
    return sum_log(log_adapter.get_multiple_logs()).jsonify()



@app.route('/get_weekly_data', methods=['POST'])
def get_weekly_data():
    logs = log_adapter.get_multiple_logs()
    from_logs = from_(logs)

    d_prime = defaultdict(dict)

    for (main, sub), req_flag in map(lambda req_flag: (req_flag.split('!'), req_flag),
                                     type.req_flag[1:]):
        d_prime[main][sub] = from_logs(get_request_count_of(req_flag))

    d_prime.update({
        'total_requests_per_day': from_logs(get_count),
        'ticks': from_logs(get_date),
        'client': from_logs(get_request_count_of('client'))
    })

    print d_prime

    return jsonify(d_prime)



@app.route('/test')
def test():
    return render_template('test.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


