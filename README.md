# volcanoplot

## Purpose

The purpose of volcanoplot is to find overrepresented words or phrases by comparing two corpora. 

For example in [this tutorial](https://github.com/estnltk/estnltk/blob/devel/docs/tutorials/adj_phrase_tagger.ipynb) we compare word usage in positive and negative customer reviews to find positively and negatively charged adjectives.

[Another example](https://github.com/estnltk/volcanoplot/blob/master/docs/postimees_tutorial.ipynb) uses the tool to compare overrepresented words in newspaper articles from 1999 and 2000 to find the most talked-about topics of the respective years.

## Usage

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
Items that are to the left of x-axis 0 are overrepresented in the first file, items to the right are overrepresented in the second. When the hover tool is selected, hovering over a datapoint displays the text value and ocurrence counts in the first and second documents. 

You can adjust the p-value on the y-axis by entering an appropriate value to the p-value box. 
Smaller p-values correspond to higher statistical significance.
You can adjust overrepresentation biases by using the sliders. When the settings have been adjusted to meet your goals, click on one of the numbers from 1-6 that correspond to the plot regions to see and export the words in that region.

The general explanation for the regions would be:

|            LEFT                                    | MIDDLE                     |  RIGHT                                              | 
|----------------------------------------------------|----------------------------|-----------------------------------------------------| 
| often occurring, overrepresented in the first file | often occurring, balanced  | often occurring, overrepresented in the second file | 
| mostly empty                                       | seldom occurring, balanced | mostly empty                                        | 

The following is a result of 

`python volcanoplot.py postimees_1999.csv postimees_2000.csv  post_ee.html --filter_below_total_count 200 --header True`

![volcano](_static/volcano.png)

For more help use `python volcanoplot.py --help`

This tool requires python libraries bokeh 0.12+, click, pandas, scipy and numpy.

## Theoretical background and limitations

x-axis shows overrepresentation in the first or second corpus.

y-axis is computed from the uncorrected pvalue of Chi-square test. Hence the results are meaningful if documents heterogeniously cover example spaces and are independent (so do not share contents). Also the plot is not useful if corpora are not balanced. For instance, the writing style has significantly changed in time and there are more older cases negative cases. Then the plot may characterise changes in style and not in the desired property
