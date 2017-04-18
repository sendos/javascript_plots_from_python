# Creating javascript plots in Python
This is a library that provides access to Matlab-like functions for easily creating javascript plots from within Python. 

No need to deal with HTML, Javascript, or CSS to get some plots with multiple linestyles, colors, markers, and labels. The currently supported Javascript plotting libraries are Flot and NVD3 (which is a wrapper around D3).

One use case for this library is to have Python scripts running automatically and updating websites that serve Javascript plots to visitors. For example, we used this library to create and update the plots on [prespredict.com](http://prespredict.com). During US presidential election seasons, a cron job calls the plotting script daily, which automatically updates the plots on the website with data from the latest polls.

The currently supported plotting functions are:

    figure, clf, plot, title, xlabel, ylabel, grid, hold, legend, close

These functions are to be used with 
          
    output_to_flot, output_to_nvd3, output_to_matplotlib

in order to visualize your plots.

This library works with the [matlab_utils_for_python](https://github.com/sendos/matlab_utils_for_python) library which also provides access to several Matlab-like functions and syntax, such as:
* Matlab-like arrays, which allow 1-based indexing and also Matlab-like slices
```python
    x = marray(some_list)
    y = x[1:3]
    z = x[1:2:end]
```
* Matlab-like ranges
```python
    for x in mrange[1:3:10]:
        fprintf('%d\n', x)
```

Note: 
* The current code creates plots that can be viewed only in Firefox, because the json files are stored locally, and browsers like Chrome do not allow reading local files.
   * If you put the json files on a web server, then the plots can be viewed in other browsers.
* You can also use output_to_matplotlib to visualize the plots with matplotlib, mainly for use in initial development and debugging.
   

## Installation and Usage

* Download the files from [matlab_utils_for_python](https://github.com/sendos/matlab_utils_for_python) to your current folder or anywhere in Python's load path.
* Download the files of this library to your current folder or anywhere in Python's load path. 
* Make sure you have NumPy installed with your Python.
* If you will use output_to_matplotlib for visualization, make sure matplotlib is installed.

Then, in your Python scripts add the following
```python
from matlab_plot_functions import *
```
and use the functions included in the module. Some sample code is shown below:
```python
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
xlabel('This is the xlabel text')
ylabel('This is the ylabel text')
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
```

### Sample output
Below are the plots you get from the above code, using Flot as the output format.
<img src="https://cloud.githubusercontent.com/assets/1019930/25148414/bc1038a8-2472-11e7-9b13-283fcbcc9eb5.PNG" height="400px">
<img src="https://cloud.githubusercontent.com/assets/1019930/25148412/bc0d9daa-2472-11e7-8953-1867596f619f.PNG" height="400px">
<img src="https://cloud.githubusercontent.com/assets/1019930/25148413/bc0f99fc-2472-11e7-960a-6d9bad85986a.PNG" height="400px">

## Authors

* **Andrew Sendonaris** - [sendos](https://github.com/sendos)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


