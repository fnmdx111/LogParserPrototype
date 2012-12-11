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

var sum_prime = function (array) {
    var result = 0;
    for (var i = 0; i < array.length; i++) {
        result += array[i][0];
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


var overview_bar_chart = function (title, target, legend, data, ticks) {
    return $.jqplot(target, data, {
        title: title,
        animate: !$.jqplot.use_excanvas,
        stackSeries: false,
        showMarker: false,
        highlighter: {
            show: true,
            showTooltip: false
        },
        seriesDefaults: {
            renderer:$.jqplot.BarRenderer,
            rendererOptions: {
                barDirection: 'vertical',
                barMargin: 30,
                highlightMouseOver: true
            },
            pointLabels: {
                show: true,
                edgeTolerance: -15
            }
        },
        series: legend.map(function (i) { return {label: i} }),
        axes: {
            xaxis: {
                renderer:$.jqplot.CategoryAxisRenderer,
                ticks: ticks
            },
            yaxis: {
                pad: 1.2
            }
        },
        legend: {
            show: true,
            location: 'e',
            placement: 'outsideGrid'
        }
    });
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
                var overview = 'overview';
                var sub_dict = data[keys[key]][overview];

                console.log(keys[key] + '_overview_div');
                $('#indicator_' + keys[key] + '_' + overview).hide();

                charts[keys[key]][overview] =
                    overview_bar_chart('Overview of `' + keys[key] + '\' (total: '
                                           + sum_prime(data[keys[key]][overview][1]) + ')',
                                       keys[key] + '_overview_div',
                                       sub_dict[0],
                                       sub_dict[1],
                                       [])
            }
        }
        $('#main').bind('shown', function (e) {
            var series = e.target.href.split('#');
            series = series[1].split('_');
            series.pop();

            if (!charts[series[0]][series[1]]) {
                console.log(series[0] + '_' + series[1] + '_div');
                $('#indicator_' + series[0] + '_' + series[1]).hide();

                var chart = undefined;
                if (!(series[1] === 'overview')) {
                    charts[series[0]][series[1]] = my_bar_chart(make_title(series[0] + '!' + series[1],
                                                                data[series[0]][series[1]]),
                                                                series[0] + '_' + series[1] + '_div',
                                                                [data[series[0]][series[1]]]);
                }
            } else {
                charts[series[0]][series[1]].replot();
            }
        });
    });
};


