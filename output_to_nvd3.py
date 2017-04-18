"""
   Module to be used with matlab_plot_functions.py, to visualize the resulting
   plots using NVD3 (http://nvd3.org), a Javascript plotting library.

   Copyright (c) 2017 Andrew Sendonaris.

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
"""

from os import path, makedirs
from numpy import nan, isnan

from matlab_utils import *
from matlab_plot_functions import db_figIdx, db_figInfo

# --------------------------------------------------------------------------------
def output_to_nvd3(figIdx, html_filename, json_filename='', extra_str=''):
    global db_figIdx, db_figInfo

    if db_figIdx == -1:
        db_figIdx = 1

    if isempty(json_filename):
        if isempty(regexp(html_filename, '^(.+)/([^/]+)\.html$')):
            json_filename = regexprep(html_filename,'^([^/]+)\.html$', 'data/$1.json')
            data_dir = 'data'
        else:
            json_filename = regexprep(html_filename,'^(.+)/([^/]+)\.html$', '$1/data/$2.json')
            data_dir = regexprep(html_filename,'^(.+)/([^/]+)\.html$', '$1/data')

        if not path.exists(data_dir):
            makedirs(data_dir)

    # ----------------------------
    fid = fopen(json_filename,'w')

    fprintf(fid,'{\n')

    if figIdx > length(db_figInfo):
        error('Figure %i not present', figIdx)

    # Helper functions
    num_fmt_array = ['%g', '%i']
    isint         = lambda x: (floor(x)==x)
    num_fmt       = lambda x: num_fmt_array[isint(x)]
    num_str       = lambda x: sprintf(num_fmt(x),x)
    use_comma_if  = lambda test: ', ' if test else ''
    
    # Start printing info about figIdx
    figInfo = db_figInfo[figIdx-1]

    # Title
    if not isempty(figInfo['title']):
        fprintf(fid,'  "title": "%s",\n', figInfo['title'])

    # x & y labels
    if not isempty(figInfo['xlabel']):
        fprintf(fid,'  "xlabel": "%s",\n', figInfo['xlabel'])

    if not isempty(figInfo['ylabel']):
        fprintf(fid,'  "ylabel": "%s",\n', figInfo['ylabel'])

    # legend location
    if not isempty(figInfo['legend_pos']) and not isempty(figInfo['legend_pos']['location']):
        fprintf(fid,'  "legend_pos": "%s",\n', figInfo['legend_pos']['location'])
  
        if not isempty(figInfo['legend_pos']['xy_margin']):
            fprintf(fid,'  "legend_xy_margin": %s,\n', figInfo['legend_pos']['xy_margin'])

    # axis limits
    axis_lim_descr = ["xmin", "xmax", "ymin", "ymax"]
    for I in range(0,length(axis_lim_descr)):
        if not isnan(figInfo['axislim'][I]):
            fprintf(fid,'  "%s": %g,\n', axis_lim_descr[I], figInfo['axislim'][I])

    # Data
    fprintf(fid,'  "all_data": [\n')

    for Id in range(0,length(figInfo['data'])):
        fprintf(fid,'     {\n') 
        if not isempty(figInfo['legend']) and not isempty(figInfo['legend'][Id]):
            fprintf(fid,'       "label": "%s",\n', figInfo['legend'][Id])

        if figInfo['linestyles'][Id] == '--':
            fprintf(fid,'       "dashes": { "show": "true" },\n')
        else:
            # For now, everything that isn't a dashed line is a solid line
            fprintf(fid,'       "lines": { "show": "true" },\n')

        if not isempty(figInfo['markers'][Id]):
            fprintf(fid,'       "points": { "symbol": "%s", "show": "true" },\n',figInfo['markers'][Id])

        fprintf(fid,'       "color": "%s",\n', figInfo['colors'][Id])
  
        # ------------------------------------------------------------------------
        # I^th data
        x = figInfo['data'][Id]['x']
        y = figInfo['data'][Id]['y']
  
        data_str = '['
        for Ix in mrange[1:length(x)]:
            sep_str = ' ' if Ix == 1 else ', '
            try:
                data_str = sprintf('%s%s[%s, %s]',data_str,sep_str, num_str(x[Ix]), num_str(y[Ix]))
            except:
                print('Entering debugging...')
                import pdb; pdb.set_trace()
        data_str = sprintf('%s ]', data_str)

        fprintf(fid,'       "data": %s\n', data_str)
        # ------------------------------------------------------------------------
    
        fprintf(fid,'     }%s\n', use_comma_if(Id != (length(figInfo['data'])-1) ))

    fprintf(fid,'   ]%s\n', use_comma_if(not isempty(extra_str)))

    # Extra info passed in by user
    if not isempty(extra_str):
        fprintf(fid, extra_str)

    fprintf(fid,'}\n')

    fclose(fid)

    # Finished saving to JSON file, now create HTML file for plotting
    #if not path.exists(html_filename):
    create_html_for_nvd3(html_filename, json_filename)
# End output_to_nvd3()
    

# --------------------------------------------------------------------------------    
def create_html_for_nvd3(html_filename, json_filename):
    fid = fopen(html_filename,'w')

    html_str = __get_html_str(json_filename)
    fprintf(fid,'%s\n',html_str)

    fclose(fid)

# --------------------------------------------------------------------------------
def __get_html_str(json_filename):
  
    str_array = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '   <title>Page Title</title>',
        '   <script language="javascript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>',
        '  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.2/d3.min.js" charset="utf-8"></script>',
        '  <script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.5/nv.d3.min.js"></script>',
        '  <link href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.5/nv.d3.css" rel="stylesheet" type="text/css">',
        '  <style>',
        '    .dashed { stroke-dasharray: 5,5; }',
        '  </style>',
        '</head>',
        '',
        '<body>',
        '  <div id="chart" style="max-width:800px;">',
        '    <h3 id="chart_title" style="text-align:center;"></h3>',
        '    <svg style="height:500px"> </svg>',
        '  </div>',
        '',
        '  <script>',
        '    function onDataReceived(data_ext, div_id) {',
        '        var xlabel = (data_ext.xlabel == undefined) ? "" : data_ext.xlabel;',
        '        var ylabel = (data_ext.ylabel == undefined) ? "" : data_ext.ylabel;',
        '        var title = (data_ext.title == undefined) ? "" : data_ext.title;',
        '        var legend_pos = (data_ext.legend_pos == undefined) ? "" : data_ext.legend_pos;',
        '        var xmin = (data_ext.xmin == undefined) ? "" : data_ext.xmin;',
        '        var xmax = (data_ext.xmax == undefined) ? "" : data_ext.xmax;',
        '        var ymin = (data_ext.ymin == undefined) ? "" : data_ext.ymin;',
        '        var ymax = (data_ext.ymax == undefined) ? "" : data_ext.ymax;',
        '',
        '        var data = transform_data_for_nvd3(data_ext.all_data);',
        '        var xval_minmax = calc_xval_minmax(data_ext.all_data);',
        '        ',
        '        nv.addGraph(function() {',
        '            var chart = nv.models.multiChart();',
        '            chart.margin({left: 100});  //Adjust chart margins to give the x-axis some breathing room.',
        '            //chart.useInteractiveGuideline(true);  //Nice looking tooltips and a guideline',
        '            chart.showLegend(true);       //Show the legend, allowing users to turn on/off line series.',
        '            ',
        '            ',
        '            //Chart x-axis settings',
        '            if (xlabel != "") { chart.xAxis.axisLabel(xlabel); }',
        '            //chart.xAxis.tickFormat(d3.format(",r"));',
        '            ',
        '            //Chart y-axis settings',
        '            if (ylabel != "") { chart.yAxis1.axisLabel(ylabel); }',
        '            //chart.yAxis1.tickFormat(d3.format(".02f"));',
        '            ',
        '            // title',
        '            if (title != "") { $("#"+div_id+"_title").text(title); }',
        '            ',
        '            // legend_pos',
        '            // NVD3 does not support legend positioning (minimal options, for a couple of chart types)',
        '',
        '            // xmin, xmax, ymin, ymax',
        '            // Neither of the approaches below work in NVD3',
        '            //chart.forceX([xmin, xmax]);',
        '            //chart.forceY([ymin, ymax]);',
        '            //chart.xAxis.scale().domain([xmin, xmax]);',
        '            //chart.yAxis1.scale().domain([ymin, ymax]);',
        '',
        '            // Add fix for bug in NVD3 which doesnt align the scatter plots correctly on the x-axis',
        '            chart.scatters1.xDomain(xval_minmax);',
        '',
        '            /* Done setting the chart up. Time to render it*/',
        '            var myData = data;',
        '            ',
        '            //d3.select("#chart svg") ',
        '            d3.select("#"+div_id+" svg") //Select the <svg> element you want to render the chart in.   ',
        '                .datum(myData)         //Populate the <svg> element with chart data...',
        '                .call(chart);          //Finally, render the chart!',
        '            ',
        '            // Clean up the legend to remove unwanted entries',
        '            clean_legend();',
        '            ',
        '            //Update the chart when window resizes.',
        '            nv.utils.windowResize(function() { chart.update(); clean_legend(); });',
        '            return chart;',
        '        });',
        '        ',
        '    } // Ends onDataReceived()',
        '',
        '    function transform_data_for_nvd3(data) {',
        '        /*',
        '          Input data is in the format: ',
        '          [',
        '            {',
        '              "label": "Bob",',
        '              "lines": { "show": "true" },',
        '              "points": { "symbol": "triangle", "show": "true" },',
        '              "color": "rgb(0, 0, 255)",',
        '              "data": [ [1, 0.16246], [2, -0.490934], [3, 0.030281], [4, 0.604252], [5, 0.837906], [6, -0.408311], [7, -0.659382], [8, 0.856244], [9, 0.814229], [10, 0.102328] ]',
        '            }, ',
        '            {',
        '              "label": "Mike",',
        '              "lines": { "show": "true" },',
        '              "points": { "symbol": "square", "show": "true" },',
        '              "color": "rgb(255, 0, 0)",',
        '              "data": [ [1, -0.243522], [2, 0.590499], [3, -0.679284], [4, -0.0370529], [5, -1.08272], [6, 0.984992], [7, 0.466757], [8, -1.5899], [9, 0.814412], [10, 0.971441] ]',
        '            }',
        '           ]',
        '           ',
        '           NVD3 expects data in this format:',
        '           [',
        '            {',
        '                values: sin,      //values - represents the array of {x,y} data points',
        '                key: "Sine Wave", //key  - the name of the series.',
        '                color: "#ff7f0e",  //color - optional: choose your own line color.',
        '                type: "line",',
        '                yAxis: 1',
        '            },',
        '            {',
        '                values: cos,',
        '                key: "Cosine Wave",',
        '                color: "#2ca02c",',
        '                type: "line",',
        '                yAxis: 1,',
        '                classed: "dashed"  ',
        '            },',
        '            {',
        '                values: cos,',
        '                key: "Cosine Wave2",',
        '                color: "#2ca02c",',
        '                type: "scatter",',
        '                yAxis: 1,',
        '                classed: "no_legend"  ',
        '            }',
        '           ]',
        '        */',
        '        var results = []',
        '        for (var idx = 0; idx < data.length; idx++)',
        '        {',
        '            var data_k = data[idx];',
        '            var marker_type = "";',
        '            var marker_type_map = {',
        '                circle: "circle",',
        '                square: "square",',
        '                diamond: "diamond",',
        '                cross: "cross",',
        '                triangle: "triangle-up" };',
        '            if(!(data_k.points == undefined))',
        '            {',
        '                marker_type = marker_type_map[data_k.points.symbol];',
        '            }',
        '',
        '            var line_type = "";',
        '            if(!(data_k.lines == undefined))',
        '            {',
        '                line_type = "line";',
        '            }',
        '            if(!(data_k.dashes == undefined))',
        '            {',
        '                line_type = "dashed";',
        '            }',
        '            ',
        '            var data_vals = [];',
        '            for (var i = 0; i < data_k.data.length; i++)',
        '            {',
        '                var d = {x: data_k.data[i][0], y: data_k.data[i][1]};',
        '                if (marker_type != "") { d.shape = marker_type; }',
        '                data_vals.push(d);',
        '            }',
        '            ',
        '            var result = { key: data_k.label,',
        '                           values: data_vals,',
        '                           color: data_k.color,',
        '                           yAxis: 1 };',
        '            if (line_type == "")',
        '            {',
        '                if(marker_type == "")',
        '                {',
        '                    // We should never be here',
        '                    // Maybe give the user an error?',
        '                }',
        '                else',
        '                {',
        '                    // We have a line with only markers',
        '                    result.type = "scatter";',
        '                    results.push(result);',
        '                }',
        '            }',
        '            else',
        '            {',
        '                if (line_type == "dashed")',
        '                {',
        '                    result.classed = "dashed";',
        '                }',
        '                ',
        '                result.type = "line";',
        '                results.push(result);',
        '                ',
        '                if(marker_type != "")',
        '                {',
        '                    // We have a line plus markers',
        '                    result2 = $.extend({}, result);',
        '                    result2.type = "scatter";',
        '                    result2.classed = "no_legend";',
        '                    results.push(result2);',
        '                }',
        '            }',
        '        }',
        '',
        '        return results;',
        '    }',
        '',
        '    function calc_xval_minmax(data)',
        '    {',
        '        var xmin = Infinity;',
        '        var xmax = -Infinity;',
        '        ',
        '        for (var idx = 0; idx < data.length; idx++)',
        '        {',
        '            var data_k = data[idx];',
        '            for (var i = 0; i < data_k.data.length; i++)',
        '            {',
        '                x = data_k.data[i][0];',
        '                xmin = Math.min(xmin, x);',
        '                xmax = Math.max(xmax, x);',
        '            }',
        '        }',
        '        return [xmin, xmax];',
        '    }',
        '',
        '    $.ajax({',
        sprintf('            url: "%s",',json_filename),
        '        method: "GET",',
        '        dataType: "json",',
        '        success: (function(div_id) { return function(response) {onDataReceived(response, div_id);}})("chart")',
        '    });',
        '',
        '    ',
        '    function clean_legend() {',
        '        objs = d3.selectAll(".nv-legend text")[0];',
        '        last_loc = "";',
        '        for (idx = 0; idx < objs.length; idx++)',
        '        {',
        '            d = objs[idx]',
        '            parent_loc = d.parentNode.getAttribute("transform")',
        '            if (d3.select(d).data()[0].classed == "no_legend")',
        '            {',
        '                last_loc = parent_loc;',
        '                //d.parentNode.setAttribute("visibility","hidden")',
        '                node = d.parentNode;',
        '                node.parentNode.removeChild(node);',
        '            }',
        '            else',
        '            {',
        '                if (last_loc != "")',
        '                {',
        '                    d.parentNode.setAttribute("transform", last_loc);',
        '                    last_loc = "";',
        '                }',
        '            }',
        '        }',
        '    }',
        '',
        '</script>',
        '',
        '</body>',
        '</html>'
    ]

    str = ''
    for I in range(0,length(str_array)):
        str += sprintf('%s\n',str_array[I])

    return str



