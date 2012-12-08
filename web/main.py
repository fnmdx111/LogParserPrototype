from collections import defaultdict
from flask import render_template, jsonify
from web.parser import type
from web import app, log_adapter
from web.misc import from_t_slice_get_name, from_t_slice_get_count, from_t_slice_get_count_of

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/get_init_data', methods=['POST'])
def get_init_data():
    log = log_adapter.get_multiple_log()
    from_log = lambda func: map(func, log.time_slices)

    d = map(lambda (k, v): (k.split('!'), v),
             {req_flag: from_log(from_t_slice_get_count_of(req_flag))
              for req_flag in type.req_flag[1:]}.iteritems())
    d_prime = defaultdict(dict)
    for (main, sub), v in d:
        d_prime[main][sub] = v

    d_prime.update({
        'time_slice_names': from_log(from_t_slice_get_name),
        'total_requests_per_hour':  from_log(from_t_slice_get_count),
        'client': from_log(from_t_slice_get_count_of('client'))
    })
    print d_prime

    return jsonify(d_prime)



@app.route('/test')
def test():
    return render_template('test.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


