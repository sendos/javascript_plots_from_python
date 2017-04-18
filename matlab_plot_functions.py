"""
   Module that provides access to Matlab-like plotting functions, such as
      figure, clf, plot, title, xlabel, ylabel, grid, hold, legend, close

   These functions are to be used with 
          output_to_flot, output_to_nvd3, output_to_matplotlib
   in order to visualize your plots

   The syntax tries to follow Matlab-like syntax as much as possible,
   given the constraints of Python.

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
from numpy import nan, isnan
import matplotlib.pyplot as plt
import subprocess
import platform

db_figIdx  = -1
db_figInfo = []

from matlab_utils import *
from output_to_flot import output_to_flot
from output_to_nvd3 import output_to_nvd3
from output_to_matplotlib import output_to_matplotlib

# --------------------------------------------------------------------------------
def __newfig(enabled=1):  
    if enabled=='disabled':
        enabled = 0

    fig = {'data':[],  'linestyles':[],'colors':[],'markers':[],'xlabel':'','ylabel':'','title':'',
           'legend':[],'legend_pos':[],'hold_on':0,'grid_on':0,'axislim':[nan,nan,nan,nan]}

    if enabled == 0:
        fig['data'] = nan

    return fig


# --------------------------------------------------------------------------------
def figure(figIdx=-1):
    global db_figIdx, db_figInfo

    if (figIdx == -1):
        db_figIdx = len(db_figInfo) + 1
    else:
        db_figIdx = figIdx

    if (db_figIdx > len(db_figInfo)) or (not isinstance(db_figInfo[db_figIdx-1]['data'], list)):
        clf(db_figIdx)        
# End: figure()


# --------------------------------------------------------------------------------
def clf(figIdx=-1):
    global db_figIdx, db_figInfo

    if (figIdx > 0):
        db_figIdx = figIdx
    else:
        if (db_figIdx == -1):
            db_figIdx = 1

    if db_figIdx > len(db_figInfo):
        for I in range(0,db_figIdx-len(db_figInfo)):
            db_figInfo.append(__newfig('disabled'))
            
    db_figInfo[db_figIdx-1] = __newfig()

    
# --------------------------------------------------------------------------------
def close(figs_to_close):
    global db_figIdx, db_figInfo

    if db_figIdx == -1:
        db_figIdx = 1

    if ischar(figs_to_close):
        if figs_to_close=='all':
            db_figIdx  = -1
            db_figInfo = []
        else:
            error('Unsupported value for figs_to_close')
    else:
        # Just mark the figures as 'deleted'
        if isinstance(figs_to_close, int):
            figs_to_close = [figs_to_close]
            
        for figIdx in figs_to_close:
            db_figInfo[figIdx-1]['data'] = nan
# End close()


# --------------------------------------------------------------------------------
def grid(str):
    global db_figIdx, db_figInfo

    if db_figIdx == -1:
        db_figIdx = 1

    if str=='on':
        grid_on = 1
    else:
        grid_on = 0

    db_figInfo[db_figIdx-1]['grid_on'] = grid_on


# --------------------------------------------------------------------------------
def hold(str):
    global db_figIdx, db_figInfo
    
    if db_figIdx == -1:
        db_figIdx = 1

    if str=='on':
        hold_on = 1
    else:
        hold_on = 0

    db_figInfo[db_figIdx-1]['hold_on'] = hold_on



# --------------------------------------------------------------------------------
def legend(*varargin):
    global db_figIdx, db_figInfo
    
    if db_figIdx == -1:
        db_figIdx = 1

    # legend(xxx,'Location','Northwest')
    # or
    # legend(xxx,'Location','Northwest[-20,10]') to include XY margin from that location
    if length(varargin) >= 2  and (varargin[-2] == 'Location'):
        location = varargin[-1]
        varargin = varargin[0:-2]

        srch = regexpi(location,'^(?<pos>northeast|northwest|southeast|southwest)(?<xy_margin>\[[\-\d\.]+,[\-\d\.]+\])?')
        if isempty(srch):
            error('legend location must be one of the following: northeast, northwest, southeast, southwest')
        else:
            pos_translate = {'northeast':'ne', 'northwest':'nw', 'southeast':'se', 'southwest':'sw'}

            location      = pos_translate[srch.group('pos').lower()]
            
            if isempty(srch.group('xy_margin')):
                location_xy_margin = ''
            else:
                location_xy_margin = srch.group('xy_margin')
                
    else:
        location           = ''
        location_xy_margin = ''

    legend_array = db_figInfo[db_figIdx-1]['legend']

    if length(varargin) > length(legend_array):
        for I in range(0,length(varargin) - length(legend_array)):
            legend_array.append('')
            
    for I in range(0,length(varargin)):
        legend_array[I] = varargin[I]

    for I in range( length(varargin), length(legend_array) ):
        legend_array[I] = ''

    db_figInfo[db_figIdx-1]['legend']     = legend_array
    db_figInfo[db_figIdx-1]['legend_pos'] = {'location':location, 'xy_margin':location_xy_margin}


# --------------------------------------------------------------------------------
def plot(x, y, plot_fmt='b'):
    global db_figIdx, db_figInfo
    
    if db_figIdx == -1:
        db_figIdx = 1

    if db_figIdx > len(db_figInfo):
        figure(db_figIdx)


    fmt_color = {'b':'rgb(0, 0, 255)',  'r':'rgb(255, 0, 0)',  'g':'rgb(0, 255, 0)', 
                 'm':'rgb(255, 0, 255)','c':'rgb(0, 255, 255)','k':'rgb(0, 0,   0)'}

    fmt_marker = {'o':'circle', 's':'square', 'd':'diamond', '\^':'triangle', '\+':'cross'}

    srch = regexp(plot_fmt,'(?<color>[brgmck])?(?<linestyle>-{1,2})?(?<marker>[osd\^\+])?(?<alpha>\[alpha:[01]\.[0-9]+\])?')

    if isempty(srch.group('color')):
        color = 'b'
    elif length(srch.group('color')) == 1:
        color = srch.group('color')
    else:
        error('Badly formatted plot_fmt')

    if isempty(srch.group('linestyle')):
        linestyle = '-'
    elif regexp(srch.group('linestyle'),'^-|--$'):
        linestyle = srch.group('linestyle')
    else:
        error('Badly formatted plot_fmt')

    if isempty(srch.group('marker')):
        marker = ''
    elif length(srch.group('marker')) == 1:
        marker = srch.group('marker')

        for marker_shortname, marker_fullname in fmt_marker.iteritems():
            marker = regexprep(marker,marker_shortname,marker_fullname)
    else:
        error('Badly formatted plot_fmt')

    if isempty(srch.group('alpha')):
        alpha = 1
    else:
        alpha = float(regexprep(srch.group('alpha'),'\[alpha:([01]\.[0-9]+)\]','$1'))

    color_str = fmt_color[color]

    if alpha < 1:
        color_str = regexprep(color_str,'rgb\(([^\(]+)\)',sprintf('rgba($1, %g)',alpha))

    if (not db_figInfo[db_figIdx-1]['hold_on']) or (not isinstance(db_figInfo[db_figIdx-1]['data'], list)):
        clf()

    db_figInfo[db_figIdx-1]['data'].append({'x':x,'y':y})
    db_figInfo[db_figIdx-1]['linestyles'].append(linestyle)
    db_figInfo[db_figIdx-1]['colors'].append(color_str)
    db_figInfo[db_figIdx-1]['markers'].append(marker)


# --------------------------------------------------------------------------------
def title(str):
    global db_figIdx, db_figInfo
    
    if db_figIdx == -1:
        db_figIdx = 1

    db_figInfo[db_figIdx-1]['title'] = str


# --------------------------------------------------------------------------------
def xlabel(str):
    global db_figIdx, db_figInfo
    
    if db_figIdx == -1:
        db_figIdx = 1

    db_figInfo[db_figIdx-1]['xlabel'] = str
        

# --------------------------------------------------------------------------------
def ylabel(str):
    global db_figIdx, db_figInfo
    
    if db_figIdx == -1:
        db_figIdx = 1

    db_figInfo[db_figIdx-1]['ylabel'] = str

# --------------------------------------------------------------------------------
def get_active_figures():
    global db_figIdx, db_figInfo
    return filter(
        lambda fig_idx: (isinstance(db_figInfo[fig_idx-1]['data'],(list,tuple))
                         or not isnan(db_figInfo[fig_idx-1]['data'])),
        xrange(1,len(db_figInfo)+1))    
    
# --------------------------------------------------------------------------------
def axisset(axis_idx, axis_vals):
    global db_figIdx, db_figInfo

    if db_figIdx == -1:
        db_figIdx = 1

    if db_figIdx > len(db_figInfo):
        for I in range(0,db_figIdx-len(db_figInfo)):
            db_figInfo.append(__newfig('disabled'))
            
    for I in range(0,len(axis_idx)):
        db_figInfo[db_figIdx-1]['axislim'][axis_idx[I]-1] = axis_vals[I]

# --------------------------------------------------------------------------------
def open_html_file(html_file):
    OS = platform.system()
    cmd_map = { 'Darwin': 'open',
                'Windows': 'start',
                'Linux': 'sensible-browser' }
    if OS in cmd_map:
        cmd_to_open_html = cmd_map[OS]
    else:
        error('OS %s not supported', OS)
        
    subprocess.call(sprintf('%s %s', cmd_to_open_html, html_file), shell=True)

# --------------------------------------------------------------------------------
def debug_print_info():
    print "db_figIdx = %i" % (db_figIdx)
    print "db_figInfo = "
    print db_figInfo




