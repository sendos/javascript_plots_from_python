"""
   Module to be used with matlab_plot_functions.py, to visualize the resulting
   plots using Flot (http://www.flotcharts.org), a Javascript plotting library.

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
def output_to_flot(figIdx, html_filename, json_filename='', flot_folder='flot', extra_str=''):
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
    create_html_for_flot(html_filename, json_filename, flot_folder)
# End output_to_flot()
    

# --------------------------------------------------------------------------------    
def create_html_for_flot(html_filename, json_filename, flot_folder='flot'):
    fid = fopen(html_filename,'w')

    html_str = __get_html_str(json_filename, flot_folder)
    fprintf(fid,'%s\n',html_str)

    fclose(fid)

# --------------------------------------------------------------------------------
def __get_html_str(json_filename, flot_folder):
  
    str_array = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '  <head>',
        '    <meta charset="utf-8">',
        '    <title>Page Title</title>',
        '',
        '    <!-- jQuery [Only Google version works] -->',
        '    <script language="javascript" type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>',
        '',
        '    <!-- Flot Plots -->',
        '    <script language="javascript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.min.js"></script>',
        '    <script language="javascript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.symbol.min.js"></script>',
        '    <script language="javascript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.crosshair.min.js"></script>',
        '    <script language="javascript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.fillbetween.min.js"></script>',
        '    <script language="javascript" type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.selection.min.js"></script>',
        '    <script language="javascript" type="text/javascript" src="'+flot_folder+'/jquery.flot.axislabels.js"></script>',
        '    <script language="javascript" type="text/javascript" src="'+flot_folder+'/jquery.flot.dashes.js"></script>',
        '',
        '  </head>',
        '',
        '  <body>',
        '        <div>',
        '            <div class="flot-plot" style="max-width:750px;">',
        '               <h3 id="placeholder2_title" style="text-align:center;"></h3>',
        '               <div id="placeholder2" style="height:450px"></div>',
        '            </div>',
        '',
        '        </div>',
        '  </body>',
        '',
        '<script type="text/javascript">',
        '$(function () {',
        '',
        '   all_plots = [];',
        '',
        '   plot2 = [];',
        '   //options2 = {};',
        '',
        '   function onDataReceived2(data_ext, fig_id) {',
        '       var data2    = data_ext.all_data;',
        '       var options2 = {};',
        '         // Possile options:',
        '           //series:    { lines: { show: true }, points: { show: true }, dashes: { show: true } }, ',
        '           options2.crosshair = { mode: "x" };',
        '           options2.grid = { hoverable: true, clickable: true }; // Puts circles above data point on mouse-over',
        '           //xaxis:  { mode: "time" },',
        '           //yaxis:  { max: 100 },',
        '           //xaxes:  [{ axisLabel: \'X label text\' }],',
        '           //yaxes:  [{ axisLabel: \'Y label text\', position: \'left\' }],',
        '           //legend: { position: "nw", margin: [0, 30] }',
        '',
        '       if(!(data_ext.xlabel == undefined)) { if(options2.xaxes == undefined) { options2.xaxes = [{}]; }; options2.xaxes[0].axisLabel = data_ext.xlabel; }',
        '       if(!(data_ext.ylabel == undefined)) { if(options2.yaxes == undefined) { options2.yaxes = [{}]; }; options2.yaxes[0].axisLabel = data_ext.ylabel; options2.yaxes[0].position = \'left\'; }',
        '',
        '       if(!(data_ext.xmin == undefined)) { if(options2.xaxis == undefined) { options2.xaxis = {};}; options2.xaxis.min = data_ext.xmin; }',
        '       if(!(data_ext.xmax == undefined)) { if(options2.xaxis == undefined) { options2.xaxis = {};}; options2.xaxis.max = data_ext.xmax; }',
        '       if(!(data_ext.ymin == undefined)) { if(options2.yaxis == undefined) { options2.yaxis = {};}; options2.yaxis.min = data_ext.ymin; }',
        '       if(!(data_ext.ymax == undefined)) { if(options2.yaxis == undefined) { options2.yaxis = {};}; options2.yaxis.max = data_ext.ymax; }',
        '',
        '       if(!(data_ext.legend_pos == undefined)) { if(options2.legend == undefined) { options2.legend = {};}; options2.legend.position = data_ext.legend_pos; }',
        '       if(!(data_ext.legend_xy_margin == undefined)) { if(options2.legend == undefined) { options2.legend = {};}; options2.legend.margin = data_ext.legend_xy_margin; }',
        '',
        '       // Enable zoom',
        '       options2.selection = { mode: "xy" };',
        '',
        '       // and plot all we got',
        '       plot2 = $.plot($("#"+fig_id), data2, options2);',
        '',
        '       // add text labels',
        '       add_plot_labels(plot2, data_ext.events);',
        '',
        '       //all_plots.push(plot2);',
        '       //all_plots.push({placeholder: $("#"+fig_id), data: data2, options: options2});',
        '       all_plots.push({plot: plot2, events: data_ext.events});',
        '',
        '       // change title strings',
        '       $("#"+fig_id+"_title").text(data_ext.title);',
        '   }',
        '',
        '   $.ajax({',
        sprintf('            url: "%s",',json_filename),
        '            method: \'GET\',',
        '            dataType: \'json\',',
        '            success: (function(fig_id) { return function(response) {onDataReceived2(response,fig_id);}})(\'placeholder2\')',
        '   });',
        '',
        '',
        '  ',
        '   // Enable zoom in',
        '   $("#placeholder2").bind("plotselected", function (event, ranges) {',
        '        // clamp the zooming to prevent eternal zoom',
        '        if (ranges.xaxis.to - ranges.xaxis.from < 0.00001)',
        '            ranges.xaxis.to = ranges.xaxis.from + 0.00001;',
        '        if (ranges.yaxis.to - ranges.yaxis.from < 0.00001)',
        '            ranges.yaxis.to = ranges.yaxis.from + 0.00001;',
        '        ',
        '        // do the zooming',
        '        plot2 = $.plot($("#placeholder2"), plot2.getData(ranges.xaxis.from, ranges.xaxis.to),',
        '                      $.extend(true, {}, options2, {',
        '                          xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },',
        '                          yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }',
        '                      }));',
        '    });',
        '   // Enable zoom out',
        '    $("#placeholder2").bind("dblclick", function (event) {',
        '	var data2 = plot2.getData();',
        '        var xax_min = data2[0].xaxis.min; var xax_max = data2[0].xaxis.max;',
        '        var yax_min = data2[0].yaxis.min; var yax_max = data2[0].yaxis.max;',
        '						  ',
        '        var zoomout_coeff = 1.5;						 ',
        '        var dx = xax_max-xax_min; var dx2 = zoomout_coeff*dx;',
        '        var dy = yax_max-yax_min; var dy2 = zoomout_coeff*dy;',
        '        var xc = (xax_max+xax_min)/2; var yc = (yax_max+yax_min)/2; ',
        '        var xax_min2 = xc-dx2/2;  var xax_max2 = xc+dx2/2; ',
        '        var yax_min2 = yc-dy2/2;  var yax_max2 = yc+dy2/2; ',
        '',
        '        plot2 = $.plot($("#placeholder2"), plot2.getData(xax_min2, xax_max2),',
        '                      $.extend(true, {}, options2, {',
        '                          xaxis: { min: xax_min2, max: xax_max2 },',
        '                          yaxis: { min: yax_min2, max: yax_max2 }',
        '                      }));',
        '						  });',
        '',
        '',
        '   // -----------------------------------------------------------------------------------------------------',
        '   // Maybe get to this later',
        '   function showTooltip(x, y, contents) {',
        '        $(\'<div id="tooltip">\' + contents + \'</div>\').css( {',
        '            position: \'absolute\',',
        '            display: \'none\',',
        '            top: y + 5,',
        '            left: x + 5,',
        '            border: \'1px solid #fdd\',',
        '            padding: \'2px\',',
        '            \'background-color\': \'#fee\',',
        '            opacity: 0.80',
        '        }).appendTo("body").fadeIn(200);',
        '    }',
        '',
        '',
        '    var previousPoint = null;',
        '    $("#placeholder2").bind("plothover", function (event, pos, item) {',
        '       ////$("#x").text(pos.x.toFixed(2));',
        '       ////$("#y").text(pos.y.toFixed(2));',
        '',
        '        // -----------',
        '        // For hovering',
        '        /*',
        '        var i, j, dataset = plot.getData();',
        '        for (i = 0; i < dataset.length; ++i) {',
        '            var series = dataset[i];',
        '',
        '            // find the nearest points, x-wise',
        '            for (j = 0; j < series.data.length; ++j)',
        '                if (series.data[j][0] > pos.x)',
        '                    break;',
        '            ',
        '            // now interpolate',
        '            var y, p1 = series.data[j - 1], p2 = series.data[j];',
        '            if (p1 == null)',
        '                y = p2[1];',
        '            else if (p2 == null)',
        '                y = p1[1];',
        '            else',
        '                y = p1[1] + (p2[1] - p1[1]) * (pos.x - p1[0]) / (p2[0] - p1[0]);',
        '         }',
        '         */',
        '         // ----------- ',
        '',
        '            if (item) {',
        '                if (previousPoint != item.dataIndex) {',
        '                    previousPoint = item.dataIndex;',
        '                    ',
        '                    $("#tooltip").remove();',
        '                    var x = item.datapoint[0],',
        '                        y = item.datapoint[1];',
        '                    ',
        '                    showTooltip(item.pageX, item.pageY,  "(" + x + ", " + y + ")");',
        '                }',
        '            }',
        '            else {',
        '                $("#tooltip").remove();',
        '                previousPoint = null;            ',
        '            }',
        '        ',
        '    });',
        '',
        '    function add_plot_labels(plot, events, add_vert_lines) ',
        '    {',
        '      if(events == undefined) {return plot;}',
        '      if(add_vert_lines == undefined) { add_vert_lines = 1; }',
        '',
        '      var data        = plot.getData();',
        '      var options     = plot.getOptions();',
        '      var xaxis       = plot.getAxes().xaxis;',
        '      var yaxis       = plot.getAxes().yaxis;',
        '      var placeholder = plot.getPlaceholder();',
        '',
        '      if(add_vert_lines == 1)',
        '      {',
        '        // First, add vertical lines',
        '        for (var idx=0; idx < events.length; idx++ )',
        '        {',
        '           evt = events[idx];',
        '           data.push({ data: [[evt.x, yaxis.min], [evt.x, yaxis.max]], lines: { show: true }, color: "rgba(0, 255, 0, 0.25)" });',
        '        }',
        '        // Plot again, to add the vertical lines, if any',
        '        plot = $.plot(placeholder, data, options);      ',
        '      }',
        '',
        '      // Second, add labels next to the vertical lines',
        '      var y1  = yaxis.min + 0.25*(yaxis.max-yaxis.min); var y2 = yaxis.min + 0.32*(yaxis.max-yaxis.min);',
        '      var y_k = y2; // y1 or y2 ==> y_k = (y1+y2)-y_k to flip',
        '      for (var idx=0; idx < events.length; idx++ )',
        '      {',
        '         evt = events[idx];',
        '         y_k = (evt.y == undefined) ? (y1+y2)-y_k : evt.y;',
        '         var o_k = plot.pointOffset({ x: evt.x, y: y_k});',
        '         placeholder.append(\'<div class="event_labels" style="position:absolute;left:\' + (o_k.left + 4) + \'px;top:\' + o_k.top + \'px;text-align:left;min-width:200px;">\' + evt.descr + \'</div>\');',
        '      }',
        '',
        '      return plot;',
        '    }',
        '',
        '});',
        '</script>',
        '',
        '</html>'
    ]

    str = ''
    for I in range(0,length(str_array)):
        str += sprintf('%s\n',str_array[I])

    return str



