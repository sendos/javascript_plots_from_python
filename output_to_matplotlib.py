"""
   Module to be used with matlab_plot_functions.py, to visualize the resulting
   plots using matplotlib.

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


from os import path
from numpy import nan, isnan
import matplotlib.pyplot as plt

from matlab_utils import *
from matlab_plot_functions import db_figIdx, db_figInfo

# --------------------------------------------------------------------------------
def output_to_matplotlib(figIdx):
    global db_figIdx, db_figInfo

    if db_figIdx == -1:
        db_figIdx = 1

    if figIdx > length(db_figInfo):
        error('Figure %i not present', figIdx)


    fmt_color = {'rgb(0, 0, 255)':'b',  'rgb(255, 0, 0)':'r',  'rgb(0, 255, 0)':'g', 
                 'rgb(255, 0, 255)':'m','rgb(0, 255, 255)':'c','rgb(0, 0,   0)':'k'}

    fmt_marker = {'circle':'o', 'square':'s', 'diamond':'d', 'triangle':'^', 'cross':'+'}

    fmt_legend_pos = {'ne':'upper right', 'nw':'upper left', 'se':'lower right', 'sw':'lower left'}
    
    # Start plotting figure figIdx
    plt.figure(figIdx)

    figInfo = db_figInfo[figIdx-1]

    # Data
    for Id in range(0,length(figInfo['data'])):
        if not isempty(figInfo['legend']) and not isempty(figInfo['legend'][Id]):
            label = figInfo['legend'][Id]
        else:
            label = None
            
        if figInfo['linestyles'][Id] == '--':
            linestyle = '--'
        else:
            # For now, everything that isn't a dashed line is a solid line
            linestyle = '-'

        if not isempty(figInfo['markers'][Id]):
            marker = fmt_marker[figInfo['markers'][Id]]
        else:
            marker = None
            
        color = fmt_color[figInfo['colors'][Id]]
  
        # x & y data
        x = figInfo['data'][Id]['x']
        y = figInfo['data'][Id]['y']
        
        plt.plot(x, y, label=label, color=color, linestyle=linestyle, marker=marker)

    # Title
    if not isempty(figInfo['title']):
        plt.title(figInfo['title'])

    # x & y labels
    if not isempty(figInfo['xlabel']):
        plt.xlabel(figInfo['xlabel'])

    if not isempty(figInfo['ylabel']):
        plt.ylabel(figInfo['ylabel'])

    # legend location
    if not isempty(figInfo['legend_pos']) and not isempty(figInfo['legend_pos']['location']):
        legend_pos = fmt_legend_pos[figInfo['legend_pos']['location']]
    else:
        legend_pos = None
    plt.legend(loc=legend_pos)
        
    # axis limits
    if not isnan(figInfo['axislim'][0]): plt.xlim(xmin=figInfo['axislim'][0])
    if not isnan(figInfo['axislim'][1]): plt.xlim(xmax=figInfo['axislim'][1])
    if not isnan(figInfo['axislim'][2]): plt.ylim(ymin=figInfo['axislim'][2])
    if not isnan(figInfo['axislim'][3]): plt.ylim(ymax=figInfo['axislim'][3])
# End output_to_matplotlib()
