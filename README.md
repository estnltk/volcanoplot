# volcanoplot

This script reads two csv files and outputs an html file for interactive work.
The csv files should contain two-element rows in the form "{item},{count}". 
The csv files should be readable with `pandas` default csv dialect settings with an optional header.

For example, two valid input files would be:

```
foo, 1
bar, 10
baz, 2 
```

and

```
foo, 10
bar, 10
baz, 6
```

The resulting html file enables you to select wordlists of words that are overrepresented in either corpus.
Items that are to the left of x-axis 0 are overrepresented in the first file, items to the right are overrepresented in the second.

You can adjust the p-value on the y-axis by entering an appropriate value to the p-value box.
You can adjust overrepresentation biases by using the sliders. When the settings have been adjusted to meet your goals, click on one of the numbers from 1-6 that correspond to the plot regions to see and export the words in that region.

The following is a result of 

`python volcanoplot.py postimees_1999.csv postimees_2000.csv  post_ee.html --filter_below_total_count 200 --header True`

![_static/volcano.png](volcano)

For more help use `python volcanoplot.py --help`
