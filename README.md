# volcanoplot
Visual tool for comparing relative frequencies of corpora
```
Usage: volcanoplot.py [OPTIONS] CSV1 CSV2 OUTPUT_FILE_NAME

  This script reads two csv files and outputs a HTML page.

  The csv files should contain two-element rows in the form
  "{item},{count}". If the files contain column names, specify it with the
  option "--header True"

Options:
  --header BOOLEAN                True|False, do the csv files have headers.
  --filter_below_total_count INTEGER
                                  Exclude items with total count below this
                                  value from the output html.
  --help                          Show this message and exit.
```
