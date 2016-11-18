import bokeh
import click
import numpy as np
import pandas as pd
import scipy.stats
from bokeh.io import curdoc, save
from bokeh.layouts import widgetbox, column, row
from bokeh.models import Range1d, HoverTool, TextInput
from bokeh.models import WheelZoomTool, PanTool, BoxZoomTool, ResetTool, ColumnDataSource, VBox, Span, CustomJS
from bokeh.models.widgets import Slider
from bokeh.plotting import figure


def save_static(data:pd.DataFrame, filename:str, title:str):

    data['y'] = np.log10(data.y.values)


    diff = data.y.max() - data.y.min()
    scale = abs(data.y.min())
    data['y'] += scale
    data['y'] /= diff
    #kui p väärtus on
    # p = 0.5
    #siis graafikul peab see olema
    # print((np.log10(-np.log10(p))+scale)/diff)



    hover = HoverTool(tooltips=[("value", "@text"),
                                ("count_first", "@count_first"),
                                ("count_second", "@count_second")])
    plot = figure(tools=[
        hover,
        WheelZoomTool(), BoxZoomTool(), PanTool(), ResetTool()],
        webgl=True,
        plot_width=800,
        plot_height=700,
    )

    source = ColumnDataSource(data)
    scatter = plot.scatter(source=source, line_width=0, line_alpha=0, size=10, x="x", y="y", alpha=0.5)
    loc = ((np.log10(-np.log10(0.5))+scale)/diff)
    p_line = Span(location=loc, dimension='width', line_color='red', line_width=3)
    plot.renderers.append(p_line)

    p_value_text = bokeh.models.Paragraph()

    p_value = TextInput(title='p value',
                        value='0.5',
                     callback=CustomJS(
                         args=dict(source=source,
                                   line=p_line,
                                   p_text=p_value_text),
                         code='''
    val = parseFloat(cb_obj.value);

    if (val < 0|| val > 1){{
        alert('p must be between 0 and 1')
    }}

    line.location = (Math.log10(-Math.log10(val)) + {scale})/{diff};
    p_text.text = "p =" + (val).toString()
    p_text.trigger('change')
    line.trigger('change')
    '''.format(scale=float(scale), diff=float(diff))))



    left = Span(location=-0.5, dimension='height', line_color='maroon')
    plot.renderers.append(left)
    right = Span(location=0.5, dimension='height', line_color='maroon')
    plot.renderers.append(right)

    left_limit = Slider(title='left_limit', value=-0.5, start=-1, end=0, step=0.001, orientation='horizontal',
                        callback=CustomJS(
                            args=dict(source=source,
                                      line=left),
                            code='''
    line.location = cb_obj.value;
    line.trigger('change')
    '''

                        ))
    right_limit = Slider(title='right_limit', value=0.5, start=0, end=1, step=0.001, orientation='horizontal',
                         callback=CustomJS(
                             args=dict(source=source,
                                       line=right),
                             code='''
    line.location = cb_obj.value;
    line.trigger('change')
    '''
                         ))

    ###################################################
    ##   Data table      ##############################
    ###################################################

    aux_source = bokeh.models.ColumnDataSource(column_names=['index', 'text'])
    table = bokeh.models.DataTable(
        source=aux_source,
        columns=[
            bokeh.models.TableColumn(field='text', title='text')
        ],
        fit_columns=True,
        width=300
    )

    ###################################################
    ##    Buttons        ##############################
    ###################################################

    button_width = 40
    buttons = [
        bokeh.models.Button(label='1', width=button_width),
        bokeh.models.Button(label='2', width=button_width),
        bokeh.models.Button(label='3', width=button_width),
        bokeh.models.Button(label='4', width=button_width),
        bokeh.models.Button(label='5', width=button_width),
        bokeh.models.Button(label='6', width=button_width)
    ]


    def make_button_callback(label):
        if label in '123':
            v_pred = 'source.data.y[i] > (Math.log10(-Math.log10(parseFloat(p_value.value))) + {scale})/{diff}'.format(scale=float(scale), diff=float(diff))
        elif label in '456':
            v_pred = 'source.data.y[i] <= (Math.log10(-Math.log10(parseFloat(p_value.value))) + {scale})/{diff}'.format(scale=float(scale), diff=float(diff))

        if label in '14':
            h_pred = 'source.data.x[i] <= left_limit.value'
        elif label in '25':
            h_pred = 'source.data.x[i] > left_limit.value && source.data.x[i] < right_limit.value'

        elif label in '36':
            h_pred = 'source.data.x[i] >= right_limit.value'

        condition = '({h_pred} && {v_pred})'.format(h_pred=h_pred, v_pred=v_pred)
        return CustomJS(args=dict(
            source=source,
            left_limit=left_limit,
            right_limit=right_limit,
            p_value=p_value,
            table=table
        ),
            code='''


        table.source.data.index = []
        table.source.data.text = []

        for (var i = 0; i < source.data.x.length; i++){{
            if {condition}{{
                        table.source.data.index.push(source.data.index[i])
                        table.source.data.text.push(source.data.text[i])
                   }}
            }}

        table.trigger('change')

        '''.format(condition=condition)
        )


    for button in buttons:
        button.callback = make_button_callback(button.label)

    # plot.renderers.extend(
    #     [
    #         Span(location=-math.log10(0.05), dimension='width', line_color='blue'),
    #         Span(location=-math.log10(0.05 / len(source.data['index'])), dimension='width',
    #              line_color='darkblue')
    #     ]
    # )

    ## Siin on y-koordinaatide jooned
    # labels = np.arange(10, 100, 10) / 100
    # labels = np.append([0.001, 0.01, 0.05], labels)
    # coords = -np.log10(labels)

    # y_ticker = bokeh.models.tickers.FixedTicker(ticks=coords)
    plot.ygrid[0].ticker = bokeh.models.tickers.FixedTicker(ticks=[])
    plot.yaxis[0].formatter = bokeh.models.formatters.PrintfTickFormatter()
    plot.yaxis[0].formatter.format = ''

    plot.set(x_range=Range1d(-1.1, 1.1),
             y_range=Range1d(-0.05, 1.05)
             )

    sliders = VBox(
        p_value_text,
        p_value,
        left_limit,
        right_limit)


    save_filename = bokeh.models.TextInput(value='filename')
    save_button = bokeh.models.Button(label='Save')


    save_button.callback = CustomJS(
        args = dict(table=table,
                    filename=save_filename,
                    ),
        code = '''

    if (table.source.data.text == undefined){
    alert('No elements selected! Press 1-6');
    }

    var text = table.source.data.text.join('\\n');
    var name = filename.value



    if (name === ''){
    alert('Filename is empty!')
    }

    console.log(name)

    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    func = function (data, fileName) {
    console.log('doing')
        blob = new Blob([data], {type: "text/plain"}),
        url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    }
    func(text, name)
    console.log('done')



     '''
    )

    input_box = widgetbox(
        save_filename,
        save_button
    )

    app = row(column(plot), column(
        row(sliders),
        row(*buttons[:3]),
        row(*buttons[3:]),

        row(input_box),
        row(table),

        responsive=False
    ))


    curdoc().add_root(app)
    save(curdoc(), filename=filename, title=title, resources=bokeh.resources.INLINE)



#####################################################################################
#####################################################################################
                      ## getting coordinates ##
#####################################################################################
#####################################################################################





EPSILON = 1e-70


def files_to_pandas(filename_a, filename_b, header, filters:dict=None):
    first  = pd.read_csv(filename_a, header=1 if header else None, index_col=0)
    second = pd.read_csv(filename_b, header=1 if header else None, index_col=0)

    df = concat_dataframes(first, second)
    df = annotate_x_coordinates(df)

    if filters is not None:
        if 'total_count' in filters.keys():
            goal = int(filters['total_count'])
            df = df[(df.count_first + df.count_second) >= goal]

    p_value = calculate_p_value(df)
    click.echo('')

    df['y'] = -np.log10(p_value)
    df['p'] = p_value
    return df[['x', 'y', 'count_first', 'count_second']]




def annotate_x_coordinates(df):

    total_count_first, total_count_second = np.sum(df.count_first.values), np.sum(df.count_second.values)
    df['relative_first'] = df['count_first'] / total_count_first
    df['relative_second'] = df['count_second'] / total_count_second
    df['x'] = (df.relative_second - df.relative_first) / np.max(np.array([df.relative_first, df.relative_second]).T,
                                                                axis=1)
    return df


def concat_dataframes(first, second):
    df = pd.concat([first, second], join='outer', axis=1)  # type: pd.DataFrame
    df.fillna(0, inplace=True)
    df.index.name = 'text'
    df.columns = ('count_first', 'count_second')
    return df


def calculate_p_value(df):
    nums = df[['count_first', 'count_second']].values.T.sum(axis=1)
    # Smoothing  the counts
    c = (df[['count_first', 'count_second']].values + 1)  # type: np.ndarray
    # Create a tile of absolute counts
    r = np.tile(nums, c.shape[0]).copy()
    r.resize(c.shape)
    r = r - df[['count_first', 'count_second']].values
    x = np.hstack((c, r))  # type: np.ndarray
    x.shape = x.shape[0], 2, 2

    progressbar = click.progressbar(length=x.shape[0])
    out = np.zeros(x.shape[0], dtype=np.float)
    for i in range(x.shape[0]):
        out[i] = scipy.stats.chi2_contingency(x[i])[1]
        progressbar.update(1)


    out[out < EPSILON] = EPSILON
    return out


@click.command()
@click.option('--header', type=click.BOOL, default=False, help='True|False, do the csv files have headers.')
@click.option('--filter_below_total_count', type=click.INT, default=None, help='Exclude items with total count below this value from the output html.')
@click.argument('csv1', type=click.File('r')) #, help='First csv file to compare'
@click.argument('csv2', type=click.File('r')) #, help='Second csv file to compare'
@click.argument('output_file_name', type=click.STRING) #, help='Filename of HTML output'
def files_to_files(csv1, csv2, output_file_name, header, filter_below_total_count):
    '''
    This script reads two csv files and outputs a HTML page.

    The csv files should contain two-element rows in the form "{item},{count}".
    If the files contain column names, specify it with the option "--header True"
    '''
    filters = {}

    if filter_below_total_count:
        filters['total_count'] = filter_below_total_count


    df = files_to_pandas(csv1, csv2, header=header, filters=filters if filters else None
                         ) # type: pd.DataFrame

    df['text']  = df.index
    df['index'] = range(len(df))
    df.set_index(['index'], inplace=True)


    save_static(df, output_file_name, ' '.join(output_file_name.split('.')[:-1]))
    click.echo('Output written to "{filename}"'.format(filename=output_file_name))

if __name__ == '__main__':
    files_to_files()
