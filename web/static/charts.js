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
            },
            yaxis: {
                pad: 0
            }
        }
    });
};


var line_chart = function (title, target, series, ticks) {
    return $.jqplot(target, series, {
        title: title,
        axesDefaults: {
            labelRenderer:$.jqplot.CanvasAxisLabelRenderer
        },
        axes: {
            xaxis: {
                renderer:$.jqplot.CategoryAxisRenderer,
                ticks: ticks
            }
        }
    })
};


var with_ticks = function (ticks) {
    return function (title, target, series) {
        return line_chart(title, target, series, ticks);
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

$.jqplot.config.enablePlugins = true;


var charts = {
    stop: {},
    line: {},
    news: {},
    stop2stop: {},
    total: {},
    client: undefined,
    param: undefined
};

var clear_charts = function () {
    $('[id^="indicator"]').show();

    var keys = ['stop', 'line', 'news', 'stop2stop', 'total'];

    for (var key in keys) {
        if (keys.hasOwnProperty(key)) {
            $('#indicator_' + keys[key] + '_overview').show();
            if (!(typeof charts[keys[key]] === "undefined")) {
                for (var sub in charts[keys[key]]) {
                    if (charts[keys[key]].hasOwnProperty(sub)) {
                        $('#indicator_' + keys[key] + '_' + sub).show();
                        if (!(typeof charts[keys[key]][sub] === "undefined")) {
                            console.log(charts[keys[key]][sub]);
                            charts[keys[key]][sub].destroy();
                            console.log(charts[keys[key]][sub]);
                        }
                    }
                }
            }
        }
    }

    var keys_ = ['client', 'param'];
    for (var key_ in keys_) {
        if (keys_.hasOwnProperty(key_)) {
            if (!(typeof charts[keys_[key_]] === "undefined")) {
                charts[keys_[key_]].destroy();
            }
        }
    }
};

var plot_single_data_charts = function (url, data) {
    clear_charts();

    $.post(url, data, function (data) {

        var ticks = data['time_slice_names'];

        var my_bar_chart = with_ticks(ticks);

        $('#indicator_client').hide();
        charts["client"] = my_bar_chart(make_title('client', data['client']),
                                        'client_div',
                                        [data['client']]);
        $('#indicator_param').hide();
        charts["param"] = my_bar_chart(make_title('param!pget', data['param']['pget']),
                                       'param_div',
                                       [data['param']['pget']]);

        var keys = ['total', 'stop', 'line', 'news', 'stop2stop'];
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
    })
};


