/**
 * the answer to the ultimate question is 42
 */

console.log('charts.js loaded.');


var sum = function (array) {
    var result = 0;
    for (var i = 0; i < array.length; i++) {
        result += array[i];
    }
    return result;
};


var make_title = function (title, array) {
    return 'Requests `' + title + '\' per Hour (total: ' + sum(array) + ')';
};


var bar_chart = function (title, target, series, ticks) {
    return $.jqplot(target, series, {
        title: title,
        animate: !$.jqplot.use_excanvas,
        seriesDefaults: {
            renderer:$.jqplot.BarRenderer,
            pointLabels: {
                show: true
            }
        },
        axes: {
            xaxis: {
                renderer:$.jqplot.CategoryAxisRenderer,
                ticks: ticks
            }
        },
        highlighter: {
            show: false
        }
    });
};


var with_ticks = function (ticks) {
    return function (title, target, series) {
        return bar_chart(title, target, series, ticks);
    }
};


var init_charts = function () {
    $.post('get_init_data', function (data) {
        $.jqplot.config.enablePlugins = true;

        var ticks = data['time_slice_names'];

        var my_bar_chart = with_ticks(ticks);

        $('#indicator_total_per_hour').hide();
        var total_per_hour_plot = my_bar_chart('Total Requests per Hour' +
                                                   ' (total: ' + sum(data['total_requests_per_hour']) + ')',
                                               'total_per_hour',
                                               [data['total_requests_per_hour']]);
        $('#indicator_client').hide();
        var client_plot = my_bar_chart(make_title('client', data['client']),
                                       'client_div',
                                       [data['client']]);
        $('#indicator_param').hide();
        var param_chart = my_bar_chart(make_title('param!pget', data['param']['pget']),
                                       'param_div',
                                       [data['param']['pget']]);

        var keys = ['stop', 'line', 'news', 'stop2stop'];
        var charts = {
            stop: {},
            line: {},
            news: {},
            stop2stop: {}
        };
        for (var key in keys) {
            if (keys.hasOwnProperty(key)) {
                var sub_dict = data[keys[key]];
                for (var series in sub_dict) {
                    if (sub_dict.hasOwnProperty(series)) {
                        console.log(keys[key] + '_' + series + '_div');

                        $('#indicator_' + keys[key] + '_' + series).hide();
                        charts[keys[key]][series] = my_bar_chart(
                            make_title(keys[key] + '!' + series, sub_dict[series]),
                            keys[key] + '_' + series + '_div',
                            [sub_dict[series]]);
                    }
                }
            }
        }
        $('#main').bind('shown', function (e, ui) {
            var series = e.target.innerHTML.split('!');
            charts[series[0]][series[1]].replot();
        })
    });
};


