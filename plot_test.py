"""
   Script with sample usage of the functions in matlab_plot_functions.py

   Copyright (c) 2017 Andrew Sendonaris.
"""

from matlab_plot_functions import *

y1 = marray([99.86 , 95.60 , 104.21, 106.10, 113.05, 113.54, 110.52, 115.82, 121.35, 136.99, 143.66, 141.05]);
y2 = marray([118.81, 114.28, 123.94, 126.12, 128.27, 130.99, 118.42, 115.05, 130.32, 135.54, 142.05, 139.39]);
x1 = mrange[1:length(y1)]
x2 = mrange[1:length(y2)]

figure(1)
clf()
plot(x1,y1,'r')
hold('on')
plot(x2,y2,'b')
grid('on')

legend('AAPL','FB','Location','northwest')
xlabel('Month')
ylabel('Stock price')
title('AAPL vs FB stock')


figure(2)
clf()
plt_str = marray('b^','rs','g--s','m^','c+','k')
for Is in mrange[1:5]:
    y = randn(1,10)
    x = mrange[1:length(y)]
    plot(x,y,plt_str[Is])
    hold('on')
grid('on')
legend('Bob','Mike','Mary','Joanne','Will', 'Location','northwest')
xlabel(sprintf('This is the xlabel text'))
ylabel(sprintf('This is the ylabel text'))
title('The title of the plot')

    
figure(3)
clf()
y1 = randn(1,100)
y2 = randn(1,50) + linspace(0,5,50)
x1 = mrange[1:length(y1)]
x2 = mrange[1:2:length(y1)]
plot(x1,y1,'b-')
hold('on')
plot(x2,y2,'r--^')    
legend('X','Y')
title('Some data')
xlabel('Time')

# To visualize the plots, uncomment one of the following output options
output = 'flot'
# output = 'NVD3'
# output = 'matplotlib'

num_figures = length(get_active_figures())

if output == 'matplotlib':
    plt.ion()
    for fig in mrange[1:num_figures]:
        output_to_matplotlib(fig)
        
    raw_input("Press ENTER to continue")

elif output == 'flot' or output == 'NVD3':
    output_to_html = output_to_flot if output == 'flot' else output_to_nvd3
    
    for fig in mrange[1:num_figures]:
        output_html_file = sprintf('test_plot_%s_%i.html', output, fig)
        
        output_to_html(fig, output_html_file)

        open_html_file(output_html_file)
        
else:
    error('Invalid value for output')
