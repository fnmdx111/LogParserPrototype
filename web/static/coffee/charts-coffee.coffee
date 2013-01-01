console.log 'charts-coffee.coffee loaded.'


sum = (array) ->
    array.reduce ((acc, x) -> acc + x), 0


sum_prime = (array) ->
    array.reduce ((acc, x) -> acc + x[0]), 0


make_title = (title, array) ->
    "Requests `#{ title }' per Hour (total: #{ sum(array) })"


bar_chart = (title, target, series, ticks) ->
    $.jqplot target, series,
        title: title
        animate: not $.jqplot.use_excanvas
        seriesDefaults:
            renderer: $.jqplot.BarRenderer
            pointLabels:
                show: true
        axes:
            xaxis:
                renderer: $.jqplot.CategoryAxisRenderer
                ticks: ticks
            yaxis:
                pad: 0


line_chart = (title, target, series, ticks) ->
    $.jqplot target, series,
        title: title
        axesDefaults:
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer
        axes:
            xaxis:
                renderer: $.jqplot.CategoryAxisRenderer
                ticks: ticks


overview_bar_chart = (title, target, legend, data, ticks) ->
    $.jqplot target, data,
        title: title
        animate: not $.jqplot.use_excanvas
        stackSeries: false
        showMarker: false
        highlighter:
            show: true
            showTooltip: false
        seriesDefaults:
            renderer: $.jqplot.BarRenderer
            rendererOptions:
                barDirection: 'vertical'
                barMargin: 30
                highlightMouseOver: true
            pointLabels:
                show: true
                edgeTolerance: -15
        series: legend.map (i) -> { label: i }
        axes:
            xaxis:
                renderer: $.jqplot.CategoryAxisRenderer
                ticks: ticks
            yaxis:
                pad: 1.2
        legend:
            show: true
            location: 'e'
            placement: 'outsideGrid'

$.jqplot.config.enablePlugins = true


multiple_main_key = ['stop', 'line', 'news', 'stop2stop', 'total']
singular_main_key = ['client', 'param']

clear_charts = (charts, keys=multiple_main_key, keys_=singular_main_key) ->
    $('[id^="indicator"]').show()

    for key in keys
        $("#indicator_#{ key }_overview").show()
        if charts[key]
            for own sub of charts[key]
                $("#indicator_#{ key }_#{ sub }").show()
                if charts[key][sub]
                    charts[key][sub].destroy()

    for key in keys_
        if charts[key]
            charts[key].destroy()


split_keys = (href) ->
    (([_, series]) -> series.split('_')) href.split('#')


plot_single_data_charts = (url, data, charts) ->
    clear_charts(charts)

    $.post url, data, (data) ->
        ticks = data['time_slice_names']

        $('#indicator_client').hide()
        charts['client'] = line_chart make_title('client', data['client']),
                                      'client_div',
                                      [data['client']],
                                      ticks
        $('#indicator_param').hide()
        charts['param'] = line_chart make_title('param!get', data['param']['pget']),
                                     'param_div',
                                     [data['param']['pget']],
                                     ticks


        keys = ['total', 'stop', 'line', 'news', 'stop2stop']
        for key in keys
            overview = 'overview'
            sub_dict = data[key][overview]

            console.log "#{ key }_overview_div"
            $("#indicator_#{ key }_#{ overview }").hide()
            charts[key][overview] =
                overview_bar_chart "Overview of `#{ key }' (total: #{ sum_prime data[key][overview][1] })",
                                   "#{ key }_overview_div",
                                   sub_dict[0],
                                   sub_dict[1],
                                   []

        $('#main').bind 'shown', (e) ->
            [main, sub, _] = split_keys e.target.href

            if not charts[main][sub]
                console.log "#{ main }_#{ sub }_div"
                $("#indicator_#{ main }_#{ sub }").hide()

                if sub != 'overview'
                    charts[main][sub] = line_chart make_title("#{ main }!#{ sub }", data[main][sub]),
                                                   "#{ main }_#{ sub }_div",
                                                   [data[main][sub]],
                                                   ticks
            else
                charts[main][sub].replot()


plot_weekly_data_charts = (charts) ->
    clear_charts charts,
                 multiple_main_key.concat(['param']),
                 singular_main_key.filter (key) -> key != 'param'

    $.post 'get_weekly_data', {}, (data) ->
        ticks = data['ticks']
        my_line_chart = (title, target, series) ->
            line_chart title, target, series, ticks

        $('#indicator_client').hide()
        charts['client'] = my_line_chart make_title('client', data['client']),
                           'client_div',
                           [data['client']]
        $('#indicator_total_overview').hide()
        charts['total'] = my_line_chart make_title('total_overview', data['total_requests_per_day']),
                                        'total_overview_div',
                                        [data['total_requests_per_day']]

        $('#main').bind 'shown', (e) ->
            [main, sub, _] = split_keys e.target.href

            if not charts[main][sub]
                console.log "#{ main }_#{ sub }"
                $("#indicator_#{ main }_#{ sub }").hide()
                charts[main][sub] = my_line_chart make_title("#{ main }!#{ sub }",
                                                             data[main][sub]),
                                                  "#{ main }_#{ sub }_div",
                                                  [data[main][sub]]
            else
                charts[main][sub].replot()

        $('div[id*="overview"]').each ->
            [main, sub, _] = $(this).attr('id').split('_')
            if $(this).attr('id') != 'total_overview_div'
                $("#indicator_#{ main }_#{ sub }").hide()
                charts[main][sub] = my_line_chart make_title("#{ main }!#{ sub }",
                                                             data[main][sub]),
                                                  $(this).attr('id'),
                                                  [data[main][sub]]


